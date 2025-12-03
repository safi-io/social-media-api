from pydantic import BaseModel


class FollowMinimal(BaseModel):
    id: int
    username: str
    avatar_url: str | None = None

    class Config:
        from_attributes = True


class FollowRequest(BaseModel):
    beta_user_id: int
