from typing_extensions import List

from langchain_core.tools import tool
from langchain_core.tools.base import BaseToolkit, BaseTool

from src.core.settings import Settings
from src.models.agent_tools_schemas import PlaceBetArgs
from src.services.chatbet_mock_service import ChatBetMockService

settings = Settings()
chatbet_service = ChatBetMockService(settings=settings)

@tool(
    "bet",
    description="Place a bet on a fixture.",
    args_schema=PlaceBetArgs
)
def bet(
    user_id: int,
    user_key: str,
    token: str,
    bet_amount: int | float,
    bet_id: str,
    fixture_id: str,
    sport_id: int,
    tournament_id: str,
    odd: float = 2.1,
    source: int = 1101
) -> bool:
    return chatbet_service.bet(
        user_id=user_id,
        user_key=user_key,
        token=token,
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