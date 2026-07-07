"""异步编程入门（async/await）
为什么需要 async：让程序在等待的时候做别的事

你点了一杯咖啡：
  同步 = 站在柜台前干等 3 分钟，什么也不做
  异步 = 等的过程中刷手机，咖啡好了店员叫你

项目里的例子：
  read() → 等文件读完 → 才能做下一步              ← 同步
  调API → 网络请求要 2 秒 → 干等                ← 浪费
  调API → 等的时候去干别的 → 响应回来了再处理      ← 异步
"""

import time
import asyncio


print("=" * 55)
print("1. 同步 vs 异步——感受区别")
print("=" * 55)

def sync_wait(name, seconds):
    """同步等待：什么也不干，干等"""
    print(f"  {name} 开始，需要 {seconds} 秒")
    time.sleep(seconds)   # 阻塞：程序停在这里
    print(f"  {name} 完成")
    return f"{name} 的结果"

print("\n同步执行（总共 6 秒）:")
start = time.time()
r1 = sync_wait("任务A", 2)
r2 = sync_wait("任务B", 4)
print(f"  耗时: {time.time() - start:.1f} 秒")


# 异步版本
async def async_wait(name, seconds):
    """异步等待：等待的时候可以干别的"""
    print(f"  {name} 开始，需要 {seconds} 秒")
    await asyncio.sleep(seconds)  # 非阻塞：交还控制权
    print(f"  {name} 完成")
    return f"{name} 的结果"

async def run_async():
    print("\n异步执行（总共 4 秒，不是 6 秒）:")
    start = time.time()

    # 创建两个任务，同时开始
    task_a = asyncio.create_task(async_wait("任务A", 2))
    task_b = asyncio.create_task(async_wait("任务B", 4))

    # await 等结果
    ra = await task_a
    rb = await task_b
    print(f"  耗时: {time.time() - start:.1f} 秒")
    print(f"  结果: {ra}, {rb}")

# 运行异步函数
asyncio.run(run_async())


print("\n" + "=" * 55)
print("2. async/await 语法拆解")
print("=" * 55)

print("""
  async def 函数名():     ← async 声明"这是一个异步函数"
      await 其他异步函数()  ← await 表示"等它完成，但等的时候别人可以干别的"

  类比：
    函数定义：  def hello():       → 普通函数
    异步定义：  async def hello(): → 异步函数（返回协程对象）

    函数调用：  result = hello()           → 直接拿结果
    异步调用：  result = await hello()     → 等结果但不阻塞

    启动异步：  asyncio.run(main())        → 入口点
""")

async def say_hello():
    await asyncio.sleep(0.5)  # 模拟半秒的异步操作
    return "你好，世界！"

# 正确调用方式
async def main():
    result = await say_hello()
    print(f"  async 函数返回: {result}")

asyncio.run(main())


print("\n" + "=" * 55)
print("3. 并发执行多个任务")
print("=" * 55)

async def fetch_data(name, seconds):
    """模拟网络请求（比如调 DeepSeek API）"""
    print(f"  请求 {name} 开始...")
    await asyncio.sleep(seconds)  # 模拟网络延迟
    print(f"  请求 {name} 完成！")
    return f"{name} 的数据"

async def main_multi():
    # 方式一：用 create_task（推荐）
    task1 = asyncio.create_task(fetch_data("DeepSeek", 2))
    task2 = asyncio.create_task(fetch_data("SiliconFlow", 3))

    # 做其他事情...
    print("  等待的时候我可以干别的...")

    # 等所有任务完成
    r1 = await task1
    r2 = await task2
    print(f"  全部完成: {r1}, {r2}")

    # 方式二：用 gather（更简洁）
    print("\n  用 gather 同时请求:")
    results = await asyncio.gather(
        fetch_data("API-A", 1.5),
        fetch_data("API-B", 2.5),
    )
    print(f"  gather 结果: {results}")

asyncio.run(main_multi())


print("\n" + "=" * 55)
print("4. 异步中的同步阻塞——陷阱")
print("=" * 55)

async def demo_trap():
    print("""
    陷阱：在异步函数中用了 time.sleep() 而不是 await asyncio.sleep()

    # ❌ 错误：会阻塞整个事件循环
    async def bad():
        time.sleep(3)  # 所有人等你 3 秒

    # ✅ 正确：把控制权交还给事件循环
    async def good():
        await asyncio.sleep(3)  # 大家都可以干别的
    """)

    print("验证：")
    async def task(name, use_sleep):
        print(f"  {name} 开始")
        if use_sleep:
            time.sleep(2)  # 阻塞！其他任务一起等
        else:
            await asyncio.sleep(2)  # 不阻塞
        print(f"  {name} 结束")

    async def test():
        # 用 time.sleep：总耗时 4 秒
        start = time.time()
        t1 = asyncio.create_task(task("阻塞任务A", True))
        t2 = asyncio.create_task(task("阻塞任务B", True))
        await asyncio.gather(t1, t2)
        print(f"    阻塞版本耗时: {time.time() - start:.1f} 秒")

        print()
        # 用 await asyncio.sleep：总耗时 2 秒
        start = time.time()
        t1 = asyncio.create_task(task("异步任务A", False))
        t2 = asyncio.create_task(task("异步任务B", False))
        await asyncio.gather(t1, t2)
        print(f"    异步版本耗时: {time.time() - start:.1f} 秒")

    await test()

asyncio.run(demo_trap())


print("\n" + "=" * 55)
print("5. 综合：模拟并发调 API 的 Agent")
print("=" * 55)

async def call_llm(messages, delay=1):
    """模拟调 LLM（XingClaw 里的真实逻辑）"""
    await asyncio.sleep(delay)
    return f"LLM 回复: 处理了 {len(messages)} 条消息"

async def call_tool(name, args, delay=0.5):
    """模拟调工具"""
    print(f"   工具 {name}({args}) 调用中...")
    await asyncio.sleep(delay)
    return f"{name} 返回: 执行完成"

async def agent_workflow(user_input):
    """模拟 Agent 执行过程"""
    print(f"\n  用户输入: {user_input}")

    # 第一步：调 LLM
    llm_result = await call_llm([{"role": "user", "content": user_input}])
    print(f"  {llm_result}")

    # 第二步：LLM 说要调工具，并发调
    print("  LLM 决定调两个工具:")
    tool_results = await asyncio.gather(
        call_tool("search", "query=Python"),
        call_tool("read", "path=test.py"),
    )
    for r in tool_results:
        print(f"  {r}")

    # 第三步：把工具结果发给 LLM 生成最终回复
    final = await call_llm([{"role": "user", "content": user_input}, {"role": "tool", "content": str(tool_results)}])
    print(f"  {final}")

    return final

# 运行 Agent
start = time.time()
asyncio.run(agent_workflow("Python 异步编程入门"))
print(f"\n  Agent 总耗时: {time.time() - start:.1f} 秒")

print("\n")
print("=" * 55)
print("知识总结")
print("=" * 55)
print("""
  async def    → 定义异步函数
  await        → 等待异步结果（不阻塞）
  asyncio.run() → 异步入口点
  create_task() → 创建并发任务
  asyncio.gather() → 并发等所有任务完成

  ❌ 不要在 async 函数里用 time.sleep()
  ✅ 用 await asyncio.sleep()
""")
