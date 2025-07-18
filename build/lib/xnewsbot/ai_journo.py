from xnewsbot.agents import create_agents

class AIJourno:
    def __init__(self, x_username, x_password, api_key: str):
        self.api_key = api_key
        self.main_agent, self.x_agent, self.research_agent, self.writer_agent = create_agents(api_key)
        self.x_username = x_username
        self.x_password = x_password

    def run(self, task: str):
        task += f"For tasks requiring X.com interaction, use the account with username {self.x_username} and password {self.x_password}. For summarizer tasks, use the following Gemini API key {self.api_key}."
        self.main_agent.run(task)