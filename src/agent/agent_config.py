from langchain_google_genai import ChatGoogleGenerativeAI

from src.core.settings import Settings
from src.tools.bet import BetToolkit
from src.tools.sports import SportsToolkit

settings = Settings()

system_prompt = (
    "You are a Sports Betting Assistant. You are able to answer questions about sports betting",
    "You can also place bets on behalf of the user if they ask you to do so"
)

bet_tools = BetToolkit()
sport_tools = SportsToolkit()
agent_tools = bet_tools.get_tools() + sport_tools.get_tools()

agent_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    api_key=settings.GEMINI_API_KEY
)