"""第1课练习：变量、字典、类"""

# 1. 创建一个字典，存一个学生的信息
#    键：name, age, city
student = {
    "name": "小明",
    "age": 18,
    "city": "上海"
}
print("学生姓名：", student["name"])

# 2. 把 student 的 age + 1
student["age"] = student["age"] + 1
# 也可以简写：student["age"] += 1
print("明年年龄：", student["age"])


# 3. 定义一个 Animal 类
#    有名字和叫声两个属性
class Animal:
    def __init__(self, name, sound):
        self.name = name     # 名字
        self.sound = sound   # 叫声

    def speak(self):
        """打印叫声"""
        print(f"{self.name}说：{self.sound}")


# 4. 用 Animal 类造两个实例
cat = Animal("猫", "喵喵")
dog = Animal("狗", "汪汪")

cat.speak()  # 猫说：喵喵
dog.speak()  # 狗说：汪汪
