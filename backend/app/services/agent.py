

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
            system_prompt_class=MySystemPrompt
        )
        result = await agent.run()
        return result
    except Exception as e:
        print(f"Error in run_agent: {str(e)}")
        raise

from browser_use import Agent, SystemPrompt

class MySystemPrompt(SystemPrompt):
    def important_rules(self) -> str:
        # Get existing rules from parent class
        existing_rules = super().important_rules()

        # Add your custom rules
        new_rules = """
            2 - Don't hallucinate.
            3 - MOST IMPORTANT RULE:
                Always try to limit the number of requests you make, otherwise, the website will block us!
        """

        # Make sure to use this pattern otherwise the exiting rules will be lost
        return f'{existing_rules}\n{new_rules}'