from pydantic import BaseModel

class UserBalance(BaseModel):
    user_id: int
    flag: int
    money: float
    playableBalance: float
    withdrawableBalance: float
    bonusBalance: float
    redeemedBonus: int

class UserInfo(UserBalance):
    token: str
    user_key: str