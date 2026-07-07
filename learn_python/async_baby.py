"""async 从头保姆式教学
一步一步来，每一步只学一个概念，跑通了再下一步
"""

# ═══════════════════════════════════════════
# 第一步：先搞懂"程序是顺序执行的"
# ═══════════════════════════════════════════

print("=" * 55)
print("第一步：程序是顺序执行的")
print("=" * 55)

import time

def step1_make_coffee():
    print("  泡咖啡...")
    time.sleep(2)
    print("  咖啡好了")

def step1_toast_bread():
    print("  烤面包...")
    time.sleep(3)
    print("  面包好了")

print("做早餐（顺序执行）:")
start = time.time()
step1_make_coffee()     # 先做咖啡，等 2 秒
step1_toast_bread()     # 再做面包，等 3 秒
print(f"总耗时: {time.time() - start:.1f} 秒")
print("问题：等咖啡的 2 秒里什么也没干")
print("如果等咖啡的时候同时烤面包，就只需要 3 秒")


# ═══════════════════════════════════════════
# 第二步：一个最简单的 async 函数
# ═══════════════════════════════════════════

print("\n" + "=" * 55)
print("第二步：写第一个 async 函数")
print("=" * 55)

import asyncio

# 定义一个 async 函数
async def hello():
    print("  hello 函数开始执行")
    return "你好，世界！"

# ==========================================
# 第二步和第二步后半合并：一个 async main 搞定
# ==========================================

async def step2_main():
    await hello()
    # 演示直接调用的返回类型
    coro = hello()
    print(f"\n直接调用 async 函数返回的是: {coro}")
    print(f"类型是: {type(coro)}")
    print("注意：并没有第一次打印'hello 函数开始执行'")
    print("因为 async 函数不会自己执行，返回的是'协程对象'")

    # await 它
    result = await coro
    print(f"\nawait 后的返回值: {result}")

asyncio.run(step2_main())


# ═══════════════════════════════════════════
# 第三步：await — 等结果但不阻塞
# ═══════════════════════════════════════════

print("\n" + "=" * 55)
print("第三步：await — 等结果")
print("=" * 55)

async def async_make_coffee():
    print("  开始泡咖啡...")
    await asyncio.sleep(2)  # 等咖啡好的 2 秒
    print("  咖啡好了")
    return "一杯热咖啡"

async def step3_main():
    # await = 等它完成
    result = await async_make_coffee()
    print(f"  拿到结果: {result}")

asyncio.run(step3_main())

print("\n对比同步和异步的区别:")
print("  time.sleep(2)  = 干等 2 秒，什么也不做")
print("  await asyncio.sleep(2) = 等 2 秒，但这期间别人可以做别的事")


# ═══════════════════════════════════════════
# 第四步：并发 — 同时做两件事
# ═══════════════════════════════════════════

print("\n" + "=" * 55)
print("第四步：同时做两件事")
print("=" * 55)

async def make_coffee():
    print("  ☕ 开始泡咖啡...")
    await asyncio.sleep(2)
    print("  ☕ 咖啡好了")
    return "咖啡"

async def toast_bread():
    print("  🍞 开始烤面包...")
    await asyncio.sleep(3)
    print("  🍞 面包好了")
    return "面包"

async def step4_main():
    print("做早餐（异步并发了！）")

    # 创建两个 "任务"（task = 让函数开始跑，但不等它完成）
    task_coffee = asyncio.create_task(make_coffee())
    task_bread = asyncio.create_task(toast_bread())

    print("  两个任务都开始跑了，我可以干别的...")

    # 等两个都完成
    c = await task_coffee
    b = await task_bread

    print(f"  早餐完成: {c} + {b}")

start = time.time()
asyncio.run(step4_main())
print(f"并发耗时: {time.time() - start:.1f} 秒")
print("不再需要 5 秒，只需要 3 秒（最长的那个任务）")


# ═══════════════════════════════════════════
# 第五步：gather — 更简单的"等全部完成"
# ═══════════════════════════════════════════

print("\n" + "=" * 55)
print("第五步：gather — 等全部完成")
print("=" * 55)

async def step5_main():
    # create_task + await 的简化写法
    results = await asyncio.gather(
        make_coffee(),
        toast_bread(),
    )
    print(f"  gather 返回: {results}")
    c, b = results  # 拆包
    print(f"  早餐: {c} + {b}")

asyncio.run(step5_main())


# ═══════════════════════════════════════════
# 第六步：模拟真实 API 调用
# ═══════════════════════════════════════════

print("\n" + "=" * 55)
print("第六步：模拟真实 API 调用")
print("=" * 55)

# 模拟调 DeepSeek API（网络请求）
async def call_deepseek(prompt):
    print(f"  [请求] 发送给 DeepSeek: {prompt[:20]}...")
    # 模拟网络延迟
    await asyncio.sleep(1.5)
    # 模拟返回结果
    return f"DeepSeek 回复: {prompt} 的答案是..."

# 模拟调 SiliconFlow Embedding API
async def call_embedding(text):
    print(f"  [请求] 发送给 Embedding: {text[:20]}...")
    await asyncio.sleep(1)
    return f"[向量: 0.1, 0.2, 0.3...]"

async def step6_main():
    # 顺序调用（慢）
    start = time.time()
    r1 = await call_deepseek("什么是 Agent？")
    r2 = await call_embedding("Agent 是一种...")
    print(f"顺序调用耗时: {time.time() - start:.1f} 秒")

    # 并发调用（快）
    start = time.time()
    r1, r2 = await asyncio.gather(
        call_deepseek("什么是 Agent？"),
        call_embedding("Agent 是一种..."),
    )
    print(f"并发调用耗时: {time.time() - start:.1f} 秒")
    print(f"结果1: {r1}")
    print(f"结果2: {r2}")

asyncio.run(step6_main())


# ═══════════════════════════════════════════
# 第七步：async 函数的"返回值"
# ═══════════════════════════════════════════

print("\n" + "=" * 55)
print("第七步：async 函数的返回值")
print("=" * 55)

# async 函数的返回值 = 普通函数的返回值
# 区别只是调用方式不同

def normal_add(a, b):
    return a + b

async def async_add(a, b):
    await asyncio.sleep(0.1)  # 模拟异步操作
    return a + b

# 同步
print(f"同步加法: {normal_add(3, 5)}")

# 异步
async def step7_main():
    result = await async_add(3, 5)
    print(f"异步加法: {result}")

    # 也可以用 gather 做并发计算
    results = await asyncio.gather(
        async_add(1, 2),
        async_add(10, 20),
        async_add(100, 200),
    )
    print(f"并发加法: {results}")

asyncio.run(step7_main())


# ═══════════════════════════════════════════
# 第八步：总结 + 一句话记住
# ═══════════════════════════════════════════

print("\n" + "=" * 55)
print("一句话总结")
print("=" * 55)

print("""
  async def → 定义"可以等"的函数
  await     → 等它但不干等
  asyncio.run() → 启动 async 程序的入口

  两段式：
    1. asyncio.create_task(异步函数())  → 说"开始跑"
    2. await task                       → 说"等它完成"

  同事发：
    await asyncio.gather(任务A, 任务B)  → 同时跑，都完成再继续

  两个不能：
    ❌ async 函数里用 time.sleep()     → 阻塞所有人
    ✅ async 函数里用 await asyncio.sleep()  → 不阻塞
""")


print("=" * 55)
print("下一步：自己动手改一个")
print("=" * 55)
print("""
试着改这段代码，让它并发执行：

  async def search_web(query):
      await asyncio.sleep(2)
      return f"{query} 的搜索结果"

  async def search_db(query):
      await asyncio.sleep(1)
      return f"{query} 的数据库结果"

  # 现在改成并发执行
  r1 = await search_web("Python")
  r2 = await search_db("Python")
""")
