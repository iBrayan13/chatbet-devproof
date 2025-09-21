from typing_extensions import List, Dict, Any

from pydantic import BaseModel

class Sport(BaseModel):
    alias: str
    profit: Dict[Any, Any]
    id: str
    name: str
    name_es: str
    name_en: str
    name_pt_br: str

class TournamentBySport(BaseModel):
    sport_name: Dict[str, str]
    tournament_name: str
    tournament_id: str
    profit: Dict[Any, Any]

class Tournament(BaseModel):
    name: str
    tournamentId: str
    order: float | int

class SportTournaments(BaseModel):
    id: str
    name: str
    tournaments: List[Tournament]

class Competitor(BaseModel):
    id: str
    name: str
    jerseyIcon: str

class Fixture(BaseModel):
    source: int
    id: str
    startTime: str
    tournament: Dict[str, str]
    sportId: str
    homeCompetitor: Competitor
    awayCompetitor: Competitor

class FixtureBySport(BaseModel):
    source: int
    tournament_id: str
    id: str
    startTime: str
    startTimeIndex: str
    tournament_name: Dict[str, str]
    home_team_data: Dict[str, Any]
    away_team_data: Dict[str, Any]
    homeCompetitorName: Dict[str, str]
    homeCompetitorId: Dict[str, str]
    awayCompetitorName: Dict[str, str]
    awayCompetitorId: Dict[str, str]