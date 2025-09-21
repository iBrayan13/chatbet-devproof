from pydantic import BaseModel, Field


# Sports-related tool schemas
class GetTournamentsArgs(BaseModel):
    sport_id: str = Field(..., description="The ID of the sport to get tournaments for.")

class GetFixturesByTournamentArgs(BaseModel):
    tournament_id: str = Field(..., description="The ID of the tournament to get fixtures for.")

class GetFixturesBySportArgs(BaseModel):
    sport_id: str = Field(..., description="The ID of the sport to get fixtures for.")

class GetOddsArgs(BaseModel):
    fixture_id: str = Field(..., description="The ID of the fixture to get odds for.")
    sport_id: str = Field(..., description="The ID of the sport.")
    tournament_id: str = Field(..., description="The ID of the tournament.")

# Bet-related tool schema
class PlaceBetArgs(BaseModel):
    user_id: str = Field(..., description="The ID of the user placing the bet.")
    user_key: str = Field(..., description="The authentication key of the user.")
    token: str = Field(..., description="The session token of the user.")
    bet_amount: float = Field(..., description="The amount of money to bet.")
    bet_id: str = Field(..., description="The ID of the bet to place.")
    fixture_id: str = Field(..., description="The ID of the fixture to place a bet on.")
    sport_id: str = Field(..., description="The ID of the sport.")
    tournament_id: str = Field(..., description="The ID of the tournament.")
    odd: float = Field(2.1, description="The odds for the bet, default is 2.1.")
    source: int = Field(1101, description="The source of the bet, default is 'api'.")