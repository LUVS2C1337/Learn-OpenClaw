"""第3课练习：if、while、try/except"""

# 1. if 判断
print("=== if 判断 ===")
def check_score(score):
    if score >= 90:
        return "优秀"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"

scores = [95, 72, 45]
for s in scores:
    print(f"{s}分：{check_score(s)}")


# 2. while 循环（模仿 Flow）
print("\n=== while 循环 ===")
nodes = ["QueryNode", "SearchNode", "SummarizeNode", None]
index = 0
curr = nodes[index]

while curr:   # 只要 curr 不是 None
    print(f"执行: {curr}")
    index = index + 1
    curr = nodes[index]  # 找下一个，变 None 时结束

print("执行完毕")


# 3. try/except 重试机制
print("\n=== try/except 重试 ===")
import time

def unstable_task():
    """模拟一个偶尔会失败的任务"""
    import random
    if random.random() < 0.7:  # 70% 概率失败
        raise ConnectionError("网络连接失败！")
    return "任务成功！"

def run_with_retry(max_retries=3, wait=1):
    for cur_retry in range(max_retries):
        try:
            result = unstable_task()
            print(f"第{cur_retry+1}次尝试：{result}")
            return result
        except Exception as e:
            print(f"第{cur_retry+1}次尝试失败：{e}")
            if cur_retry == max_retries - 1:
                raise e  # 最后一次仍失败，抛出
            print(f"等待{wait}秒后重试...")
            time.sleep(wait)

try:
    run_with_retry(max_retries=3, wait=0.5)
except:
    print("全部重试都失败了")
