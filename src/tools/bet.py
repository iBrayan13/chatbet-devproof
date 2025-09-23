from typing_extensions import List, Dict, Any

from langchain_core.tools import tool
from langchain_core.tools.base import BaseToolkit, BaseTool

from src.core.settings import Settings
from src.models.agent_tools_schemas import PlaceBetArgs
from src.services.chatbet_mock_service import ChatBetMockService, session_data

settings = Settings()
chatbet_service = ChatBetMockService(settings=settings)

@tool(
    "bet",
    description="Place a bet on a fixture. Extract the bet data from the get_odds tool.",
    args_schema=PlaceBetArgs
)
def bet(
    bet_amount: float,
    bet_id: str,
    fixture_id: str,
    sport_id: int,
    tournament_id: str,
    odd: float = 2.1,
    source: int = 1101,
) -> bool:
    
    if session_data is None:
        return False

    return chatbet_service.bet(
        user_id=session_data.user_id,
        user_key=session_data.user_key,
        token=session_data.token,
        bet_amount=bet_amount,
        bet_id=bet_id,
        fixture_id=fixture_id,
        sport_id=sport_id,
        tournament_id=tournament_id,
        odd=odd,
        source=source
    )

class BetToolkit(BaseToolkit):

    def get_tools(self) -> List[BaseTool]:
        return [bet]