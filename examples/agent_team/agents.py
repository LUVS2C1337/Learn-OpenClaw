class Agent:
    def __init__(self, name, llm, system_prompt):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt

    def run(self, task):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": task},
        ]

        response = self.llm.chat(messages)
        return {
            "agent": self.name,
            "task": task,
            "result": response,
        }