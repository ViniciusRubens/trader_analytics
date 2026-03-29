import re
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

class AITradingTeam:
    """
    Class responsible for managing and executing AI agents for financial analysis.
    """
    
    def __init__(
        self, 
        primary_model_id: str = "llama-3.3-70b-versatile", 
        worker_model_id: str = "llama-3.1-8b-instant"
):
        """
        Initializes the AI agents with their specific roles, tools, and models.
        """
        self.web_search_agent = Agent(
            name = "Web Search Agent",
            role = "Perform web searches for latest news and context",
            model = Groq(id = worker_model_id),
            tools = [DuckDuckGo()],
            instructions = ["Always include the sources for your information."],
            show_tool_calls = True, 
            markdown = True
        )

        self.financial_agent = Agent(
            name = "Financial Agent",
            role = "Retrieve financial data and analyst recommendations",
            model = Groq(id = worker_model_id),
            tools = [YFinanceTools(
                stock_price = False,
                analyst_recommendations = True,
                stock_fundamentals = False,
                company_news = True
            )],
            instructions = ["Use tables to display the financial data clearly."],
            show_tool_calls = True, 
            markdown = True
        )

        self.multi_ai_agent = Agent(
            team = [self.web_search_agent, self.financial_agent],
            model = Groq(id = primary_model_id),
            instructions = [
                "Always include sources.", 
                "Use tables to display the data."
            ],
            show_tool_calls = True, 
            markdown = True
        )

    def analyze_ticker(self, ticker: str) -> str:
        """
        Runs the AI agent team to analyze a specific stock ticker.
        
        Args:
            ticker (str): The stock ticker symbol (e.g., 'AAPL', 'PETR4.SA').
            
        Returns:
            str: The cleaned markdown response from the AI agents.
        """
        prompt = f"Summarize the analyst recommendations and share the latest news for {ticker}."
        
        # Execute the multi-agent team
        ai_response = self.multi_ai_agent.run(prompt)
        
        # Return the cleaned text, removing internal tool logs
        return self._clean_response(ai_response.content)

    def _clean_response(self, text: str) -> str:
        """
        Cleans the raw response from the agent, removing internal tool call logs.
        """
        # Removes blocks starting with "Running:" and lines with "transfer_task_to_finance_ai_agent"
        clean_text = re.sub(
            r"(Running:[\s\S]*?\n\n)|(^transfer_task_to_finance_ai_agent.*\n?)",
            "", 
            text, 
            flags = re.MULTILINE
        ).strip()
        
        return clean_text