from typing_extensions import List

from langchain_core.tools import tool
from langchain_core.tools.base import BaseToolkit, BaseTool

from src.core.settings import Settings
from src.services.chatbet_mock_service import ChatBetMockService
from src.models.sports import Sport, TournamentBySport, Fixture, FixtureBySport
from src.models.agent_tools_schemas import (
    GetTournamentsArgs,
    GetFixturesByTournamentArgs,
    GetFixturesBySportArgs,
    GetOddsArgs
)

settings = Settings()
chatbet_service = ChatBetMockService(settings=settings)

@tool(
    "get_sports",
    description="Get all sports data.",
)
def get_all_sports() -> List[Sport]:
    return chatbet_service.get_sports()

@tool(
    "get_tournaments_by_sport_id",
    description="Get all tournaments by sport id.",
    args_schema=GetTournamentsArgs
)
def get_tournaments_by_sport_id(sport_id: str) -> List[TournamentBySport]:
    return chatbet_service.get_tournaments_by_sport_id(sport_id)

@tool(
    "get_fixtures_by_tournament_id",
    description="Get all fixtures by tournament id.",
    args_schema=GetFixturesByTournamentArgs
)
def get_fixtures_by_tournament_id(tournament_id: str) -> List[Fixture]:
    return chatbet_service.get_fixtures_by_tournament_id(tournament_id)

@tool(
    "get_fixtures_by_sport_id",
    description="Get all fixtures by sport id.",
    args_schema=GetFixturesBySportArgs
)
def get_fixtures_by_sport_id(sport_id: str) -> List[FixtureBySport]:
    return chatbet_service.get_fixtures_by_sport_id(sport_id)

@tool(
    "get_odds",
    description="Get all odds by fixture id.",
    args_schema=GetOddsArgs
)
def get_odds(sport_id: str, tournament_id: str, fixture_id: str):
    return chatbet_service.get_odds(sport_id, tournament_id, fixture_id)


class SportsToolkit(BaseToolkit):

    def get_tools(self) -> List[BaseTool]:
        return [get_all_sports, get_tournaments_by_sport_id, get_fixtures_by_tournament_id]
    