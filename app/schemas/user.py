from pydantic import BaseModel, Field
from typing import Optional, List


class User(BaseModel):
    #field is used to add metadata and validation rules to username
    username: Optional[str] = Field(
        alias="name",
        title="The username",
        description="This is the username of the user",
        min_length=1,
        default=None
    )

    # liked post is a list of integers
    liked_posts: List[int] = Field(
        description="Array of post ids the user liked"
    )

#this is another class that inherits from the users class that has 2 variables specified
class FullUserProfile(User):
    short_description: str
    long_bio: str

class MultipleUsersResponse(BaseModel):
    users: List[FullUserProfile]
    total: int

class CreateUserResponse(BaseModel):
    user_id: int