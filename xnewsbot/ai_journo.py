from xnewsbot.agents import create_agents

class AIJourno:
    def __init__(self, x_username, x_password, api_key: str):
        self.api_key = api_key
        self.main_agent, self.x_agent, self.research_agent, self.writer_agent = create_agents(api_key)
        self.x_username = x_username
        self.x_password = x_password
        self.main_agent.prompt_templates["system_prompt"] += f"\n\nX.com Credentials:\nUsername: {self.x_username}\nPassword: {self.x_password}\n"
    def run(self, task: str):
        self.main_agent.run(task)