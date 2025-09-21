import requests
import traceback
from functools import wraps
from typing_extensions import List, Dict, Any, Optional

from pydantic import ValidationError

from src.core.settings import Settings
from src.models.auth_chatbet import UserBalance, UserInfo
from src.models.sports import Sport, TournamentBySport, SportTournaments, Fixture, FixtureBySport

def handle_exceptions(default_return: Any = None, model_validate: str = "UnknownModel"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            except ValidationError as ve:
                cls_name = args[0].__class__.__name__ if args else "UnknownClass"
                method_name = func.__name__
                traceback_err = traceback.format_exc()
                print(
                    f"{cls_name}.{method_name}: Validation error "
                    f"(creating {model_validate} models): {ve}. Traceback: {traceback_err}"
                )
                return default_return
            
            except Exception as e:
                cls_name = args[0].__class__.__name__ if args else "UnknownClass"
                method_name = func.__name__
                traceback_err = traceback.format_exc()
                print(f"{cls_name}.{method_name}: {e}. Traceback: {traceback_err}")
                return default_return
            
        return wrapper
    return decorator

class ChatBetMockService:
    def __init__(self, settings: Settings):
        self.base_url = settings.CHATBET_BASE_URL

    @handle_exceptions(default_return=None)
    def _generate_token(self) -> Optional[str]:
        response = requests.post(
            url=f"{self.base_url}/auth/generate_token"
        )
        response.raise_for_status()

        return response.json().get("token")
    
    def _validate_token(self, token: str) -> bool:
        response = requests.get(
            url=f"{self.base_url}/auth/validate_token",
            headers={"token": token}
        )
        if response.status_code != 200:
            return False

        return True
    
    @handle_exceptions(default_return=None)
    def _validate_user(self, user_key: str) -> Optional[int]:
        response = requests.get(
            url=f"{self.base_url}/auth/validate_user",
            params={"userKey": user_key}
        )
        response.raise_for_status()

        return response.json().get("userId")
    
    @handle_exceptions(default_return=None, model_validate="UserBalance")
    def _get_user_balance(self, user_id: int, user_key: str, token: str) -> Optional[UserBalance]:
        response = requests.get(
            url=f"{self.base_url}/user/get_balance",
            params={
                "userId": user_id,
                "userKey": user_key
            },
            headers={"token": token}
        )
        response.raise_for_status()

        balance_data = response.json()
        if not balance_data:
            raise Exception("No user balance data found")
        return UserBalance(user_id=user_id, **balance_data)

    @handle_exceptions(default_return=None, model_validate="UserInfo")
    def auth_new_session(self) -> Optional[UserInfo]:
        token = self._generate_token()
        if not token or not self._validate_token(token):
            raise Exception("Failed to generate or validate token")
        
        user_key = token # Assuming token is used as user_key
        user_id = self._validate_user(user_key)
        if not user_id:
            raise Exception("Failed to validate user")
        
        user_balance = self._get_user_balance(user_id, user_key, token)
        return UserInfo.model_validate({
            "token": token,
            "user_key": user_key,
            **user_balance.model_dump()
        })
        
    @handle_exceptions(default_return=[], model_validate="Sport")
    def get_sports(self) -> List[Sport]:
        response = requests.get(
            url=f"{self.base_url}/sports"
        )
        response.raise_for_status()

        return [Sport.model_validate(sport) for sport in response.json()]
        
    @handle_exceptions(default_return=[], model_validate="TournamentBySport")
    def get_tournaments_by_sport_id(self, sport_id: int) -> List[TournamentBySport]:
        response = requests.get(
            url=f"{self.base_url}/sports/tournaments",
            params={"sport_id": sport_id}
        )
        response.raise_for_status()

        return [TournamentBySport.model_validate(tournament) for tournament in response.json()]

    @handle_exceptions(default_return=[], model_validate="SportTournaments")
    def get_all_tournaments(self) -> List[SportTournaments]:
        response = requests.get(
            url=f"{self.base_url}/sports/all-tournaments"
        )
        response.raise_for_status()

        return [SportTournaments.model_validate(sport_tournaments) for sport_tournaments in response.json()]
        
    @handle_exceptions(default_return=[], model_validate="Fixture")
    def get_fixtures_by_tournament_id(self, tournament_id: str) -> List[Fixture]:
        response = requests.get(
            url=f"{self.base_url}/sports/fixtures",
            params={"tournamentId": tournament_id}
        )
        response.raise_for_status()

        return [Fixture.model_validate(fixture) for fixture in response.json()[1:]]
        
    @handle_exceptions(default_return=[], model_validate="Fixture")
    def get_fixtures_by_sport_id(self, sport_id: str) -> List[FixtureBySport]:
        response = requests.get(
            url=f"{self.base_url}/sports/sports-fixtures",
            params={"sportId": sport_id}
        )
        response.raise_for_status()

        return [FixtureBySport.model_validate(fixture) for fixture in response.json()]
        
    @handle_exceptions(default_return=None)
    def get_odds(self, sport_id: str, tournament_id: str, fixture_id: str) -> Optional[Dict[str, Any]]:
        response = requests.get(
            url=f"{self.base_url}/sports/odds",
            params={
                "sportId": sport_id,
                "tournamentId": tournament_id,
                "fixtureId": fixture_id
            }
        )
        response.raise_for_status()

        return response.json()
    
    def bet(
            self,
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
        response = requests.post(
            url=f"{self.base_url}/place-bet",
            headers={"token": token},
            json={
                "user": {
                    "userKey": user_key,
                    "id": str(user_id)
                },
                "betInfo": {
                    "amount": str(bet_amount),
                    "betId": [
                    {
                        "betId": bet_id,
                        "fixtureId": fixture_id,
                        "odd": str(odd),
                        "sportId": str(sport_id),
                        "tournamentId": tournament_id
                    }
                    ],
                    "source": str(source)
                }
            }
        )

        if response.json().get("message", "failed").lower() == "bet accepted":
            return True
        
        return False
        