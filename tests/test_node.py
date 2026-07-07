"""Tests for core/node.py — the Node and Flow classes."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.node import Node, Flow


class TestNode:
    """Test the Node class"""

    def test_exec_raises_not_implemented(self):
        """Base Node should raise NotImplementedError"""
        node = Node()
        try:
            node.exec("hello")
            assert False, "Should have raised"
        except NotImplementedError:
            pass

    def test_rshift_sets_successor(self):
        """a >> b should set a.successors['default'] = b"""
        a = Node()
        b = Node()
        a >> b
        assert a.successors["default"] == b

    def test_rshift_returns_other(self):
        """a >> b should return b (for chaining)"""
        a = Node()
        b = Node()
        result = a >> b
        assert result == b

    def test_sub_sets_action(self):
        """a - 'foo' should set a._action to 'foo'"""
        a = Node()
        a - "foo"
        assert a._action == "foo"

    def test_sub_with_default(self):
        """a - 'default' should set a._action to 'default'"""
        a = Node()
        a - "default"
        assert a._action == "default"

    def test_sub_with_empty_string(self):
        """a - '' should fall back to 'default'"""
        a = Node()
        a - ""
        assert a._action == "default"

    def test_sub_rshift_chain(self):
        """a - 'x' >> b should connect via 'x'"""
        a = Node()
        b = Node()
        a - "x" >> b
        assert a.successors["x"] == b
        # _action should reset to 'default' after >>
        assert a._action == "default"

    def test_rshift_resets_action(self):
        """After >>, _action should be 'default'"""
        a = Node()
        b = Node()
        a - "x" >> b
        assert a._action == "default"

    def test_max_retries_default(self):
        """Default max_retries should be 1"""
        node = Node()
        assert node.max_retries == 1

    def test_wait_default(self):
        """Default wait should be 0"""
        node = Node()
        assert node.wait == 0

    def test_custom_max_retries(self):
        """Should accept custom max_retries"""
        node = Node(max_retries=3)
        assert node.max_retries == 3

    def test_custom_wait(self):
        """Should accept custom wait"""
        node = Node(wait=2.5)
        assert node.wait == 2.5


class ConcreteNode(Node):
    """Helper: a Node that returns (action, payload)"""

    def __init__(self, action="default", transform=None):
        super().__init__()
        self._return_action = action
        self._transform = transform or (lambda x: x)

    def exec(self, payload):
        return self._return_action, self._transform(payload)


class TestFlow:
    """Test the Flow class"""

    def test_flow_with_single_node(self):
        """Flow with one node should run and return its result"""
        node = ConcreteNode()
        flow = Flow(node)
        action, result = flow.run("hello")
        assert result == "hello"

    def test_flow_with_chain(self):
        """Flow should chain nodes via default action"""
        a = ConcreteNode(transform=lambda x: x.upper())
        b = ConcreteNode(transform=lambda x: x + "!")
        a >> b
        flow = Flow(a)
        action, result = flow.run("hello")
        assert result == "HELLO!"

    def test_flow_with_custom_action(self):
        """Flow should route by action name"""
        a = ConcreteNode(action="search")
        b = ConcreteNode()
        a - "search" >> b
        flow = Flow(a)
        action, result = flow.run("data")
        assert result == "data"

    def test_flow_ends_when_no_successor(self):
        """Flow should stop when no successor matches"""
        a = ConcreteNode(action="missing")
        b = ConcreteNode()
        a - "other" >> b  # 'missing' doesn't match 'other'
        flow = Flow(a)
        action, result = flow.run("hello")
        # Should stop at 'a' since 'missing' has no successor
        assert action == "missing"

    def test_flow_retry_on_failure(self):
        """Node should retry on exception"""
        call_count = [0]

        class FlakyNode(Node):
            def __init__(self):
                super().__init__(max_retries=3, wait=0)

            def exec(self, payload):
                call_count[0] += 1
                if call_count[0] < 3:
                    raise ValueError("not yet")
                return "default", "success"

        node = FlakyNode()
        flow = Flow(node)
        action, result = flow.run("go")
        assert result == "success"
        assert call_count[0] == 3  # 2 fails + 1 success

    def test_flow_raises_after_all_retries_fail(self):
        """Node should raise after exhausting retries"""

        class AlwaysFailNode(Node):
            def __init__(self):
                super().__init__(max_retries=2, wait=0)

            def exec(self, payload):
                raise ValueError("always fails")

        node = AlwaysFailNode()
        flow = Flow(node)
        try:
            flow.run("go")
            assert False, "Should have raised"
        except ValueError:
            pass

    def test_flow_none_start(self):
        """Flow with no start should return ('default', initial payload)"""
        flow = Flow()
        action, result = flow.run("hello")
        assert action == "default"
        assert result == "hello"

    def test_flow_three_node_pipeline(self):
        """Three nodes chained: upper → exclaim → reverse"""
        a = ConcreteNode(transform=lambda x: x.upper())
        b = ConcreteNode(transform=lambda x: x + "!!!")
        c = ConcreteNode(transform=lambda x: x[::-1])

        a >> b >> c
        flow = Flow(a)
        action, result = flow.run("hello")
        assert result == "!!!OLLEH"

    def test_branching_routes(self):
        """Node can fork based on action"""
        on_success = ConcreteNode(transform=lambda x: f"{x}:ok")
        on_error = ConcreteNode(transform=lambda x: f"{x}:err")

        router = ConcreteNode(action="success")
        router - "success" >> on_success
        router - "error" >> on_error

        flow = Flow(router)
        action, result = flow.run("data")
        assert result == "data:ok"
