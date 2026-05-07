1. 实现 Node / Workflow / Agent 
   - 我们最终的目标是造一个Agent，能够联网搜索、运行命令行、文件编辑。
   - Agent底层可以使用Node来抽象，我已经准备好了一个极简的实现，可以看[`core/node.py`](./core/node.py)，不到60行就实现了一个Agent的轻框架，实在是太容易理解了！如果没有py基础看不懂，可以把代码复制给ai让它来解释。
   - 但我们应该怎么去用Node呢，我们可以新建3个Node并把它们串起来实现功能`接收输入->上网搜索->大模型生成总结`，恭喜你已经实现了workflow，相关实现已经在[`examples/workflow`](./examples/workflow)
   - 现在新建个workflow，实现功能`接收用户输入->大模型回复`，并且loop反复调用这个workflow，恭喜你已经实现了chatbot，相关实现已经在[`examples/chatbot`](./examples/chatbot)
   - 现在尝试给chatbot一些tools(下文会详细讲tool)，让它能够上网搜索东西、编辑文件、运行命令行，恭喜你已经实现了agent，相关实现已经在[`examples/chatbot_with_tools`](./examples/chatbot_with_tools)
   - 总结：**workflow = node + node**、**chatbot = workflow + loop**、 **agent = chatbot + tools = workflow + loop + tools**

2. 实现 RAG 
   - 选择 [Chroma](https://docs.trychroma.com/docs/overview/getting-started) 而不是Milvus、LanceDB、pgvector等等，因为Chroma部署简单、api简洁使用成本低
   - 注意，你可能需要一个 embedding model api 而不是 llm api，你可以在Kimi、智谱等官网找到对应的 embedding 模型
   - 恭喜你已经学会了rag！！！
   - 为什么这就是全部了，真有这么简单？是的这就是全部，当初提出 RAG(Retrieval-Augmented Generation) 概念时，可能觉得得有 检索-增强-生成 这三个功能。
   - 但实际上大伙最终只用到了检索，VectorDB 就能很完美执行这个任务
   - 所以 RAG 是个很过时的概念，大伙只想要一个 VectorDB 而已，或者说 RAG=VectorDB

3. 实现 Tool、MCP、Skill 
   - Tool: process call (function call)，也就是调用了一个函数
   - MCP: remote process call 也就是后端里面的 RPC 概念，调用了服务器上的一个函数
   - Skill: local process call 也就是调用了本地的一个函数
   - 它们其实本质上都是 Tool
   - 为什么Tool会有这么多形式？这就不得不说Tool的发展历程。
   - Tool来源：在早期大伙为了chatbot不只是chat，而是实际做些事所以出现了Tool，实现Tool的形式各不一样，最常见的就是输入llm的prompt中里面加入function（等同于tool）的name、parameters、description并且要求llm输出json格式，最后再调用对应的function。
   - MCP来源：为了解决Tool实现参差不齐的现象，anthropic定了一个Tool的标准，也就是[MCP(Model Context Protocol)](https://modelcontextprotocol.io/docs/getting-started/intro)（感觉不如叫Remote Tool Protocol更易读），让各个Tool能够远程“即插即用”，看起来非常棒只要提供了MCP服务就能实现ai从just chat到do something的转变，于是2025年各个公司疯狂都在推行自己的MCP服务
   - Skill来源：但人们渐渐发现了MCP的弊端：每次调用llm时候，都会把在prompt额外加上MCP的所有Tool的信息（包括name、parameters、description等等），发现大部分MCP服务并没有想象的那么有用，以及导致性能变差以及token浪费，anthropic在blog描述了这件事 [Code execution with MCP: Building more efficient agents](https://www.anthropic.com/engineering/code-execution-with-mcp)，并分享了它们的解决方案，就是**渐进式加载**和**多用代码执行**，后来anthropic发布了[skill](https://support.claude.com/en/articles/12512176-what-are-skills)就和这个差不多，重点就是**渐进式加载**和**多用代码执行**。
   - 设计Tool：实际Agent并不需要那么多五花八门的Tool，最重要的是linux中的bash、edit、find、grep、ls、read、write命令，这些就已经能做很多事且做得非常好，Vercel[通过移除大部分的Tool反而提高了text-to-sql从80%到100%](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools)，以及pi-mono极简coding-agent作者提到[这四个工具就是构建有效 Coding Agent 所需的全部：read、write、edit、bash](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/)
   - 实践：可以阅读[`tools`](./tools)和[`examples/chatbot_with_tools`](./examples/chatbot_with_tools)文件夹里的实现
   - 总结: MCP是Remote Tool，Skill是Local Tool，尽量不要设计Tool并且优先用linux的bash来解决问题

4. 实现 Context / Memory
   - 短期 Context：最近几轮的完整对话
   - 长期 Context：更早的对话，会"总结一次"进行压缩
   - Memory = 短期 Context + 长期 Context

5. 实现 Multi-Agent / Subagent / Agent Teams 
   - multi-agent最初设想用google制定的A2A(agent to agent)协议，让不同地方的Agent进行交互，但这个设想失败了，multi-agent效果复杂且大部分性能还不如简单的single agent，且现实中没看到过agent用A2A协议进行交互
   - 但大伙发现有些场景可以用multi-agent来实现上下文隔离、只回传压缩结果、避免主上下文被工具细节污染，这样能提高agent的效果，可以看这个blog了解multi-agent到底是什么[How we built our multi-agent research system](https://www.anthropic.com/engineering/built-multi-agent-research-system)
   - subagent概念由此发展出来，甚至推出了[自定义subagent](https://code.claude.com/docs/zh-CN/sub-agents)。但我并不推荐自定义subagent，毕竟由master agent来自动生成subagent总是个简单高效的选择
   - Agent Teams则是目前最前沿的发展方向，摒弃了主从的agent结构，而采用并行的方式，能够成倍效率且agent间不冲突地开发项目，这是十分有价值的，大伙都在研究，可以参考claude的[agent-teams](https://code.claude.com/docs/zh-CN/agent-teams)以及blog [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) 还有cursor的blog [扩展长时间运行的自主编码能力](https://cursor.com/cn/blog/scaling-agents) 和 [迈向自动驾驶代码库](https://cursor.com/cn/blog/self-driving-codebases)
