from browser_use import Agent, SystemPrompt, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import json

config = BrowserConfig(
    headless=True,
    disable_security=True
)

browser = Browser(config=config)

async def run_agent(api_key: str, task: str):
    try:
        llm = ChatOpenAI(
            model="gpt-4o",
            openai_api_key=api_key
        )
        planner = ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=api_key
        )
        agent = Agent(
            task=task,
            llm=llm,
            planner_llm=planner,
            system_prompt_class=MySystemPrompt,
            max_failures=20,
            browser=browser
        )
        
        history = await agent.run()
        result = history.final_result()
        
        return json.dumps(result)
    except Exception as e:
        print(f"Error in run_agent: {str(e)}")
        raise

class MySystemPrompt(SystemPrompt):
    def important_rules(self) -> str:
        # Get existing rules from parent class
        existing_rules = super().important_rules()

        # Add your custom rules
        new_rules = """
            1 - Don't hallucinate.
            2 - If you can't find the information after the max number of steps, say "I don't know".
            3 - If you are stuck after repeating the action many times, try something different.
            4 - Accept cookies when necessary.
        """

        # Make sure to use this pattern otherwise the exiting rules will be lost
        return f'{existing_rules}\n{new_rules}'