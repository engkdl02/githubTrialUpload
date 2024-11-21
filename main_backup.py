from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List

#variable pointer to the FastApi class
app = FastAPI()



# #users basic information
# # a class that inherits from the BaseModel class
# # variables that are initialized with specific types
# class ProfileInfo(BaseModel):
#     short_description: str
#     long_bio: str

#Another class called User that inherits from the Basemodel
# username is a variable that should have a value string or None by using optional
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

#----------------------------------------------
# a dictionary
# the 0 is a unique user id and maps to its user info
profile_infos = {
    0: {
        "short_description": "My bio description",
        "long_bio": "this is our longer bio"
    }
}


users_content = {
    0: {
        "name": "default_user",
        "liked_posts": [1] * 9,
    },

}
#----------------------------------------------


#this is a function that has a parameter of type integer
#= 0 means that if user_id is not provided when the function is called, it defaults to 0
#FullUserProfile is a return type hint that this function will return and instance of this
async def get_user_info(user_id: int = 0) -> FullUserProfile:

    #currently reading from the dictionary
    #retrieves the profile_info data and then store it into a variable
    profile_info = profile_infos[user_id]
    #get returns a value for key if key is a dictionary
    user_content = users_content.get(user_id)

    #later read from database
    #db case here we can await
    #await db read ... user_id


    #the User class is used and the value of user_content is passed
    user = User(**user_content)

    #
    full_user_profile_data = {
        **profile_info,
        **user.model_dump()
    }

    return FullUserProfile(**full_user_profile_data)


async def get_all_users_with_pagination(start: int, limit: int) -> (list[FullUserProfile], int):
    list_of_users = []
    keys = list(profile_infos.keys())
    total = len(keys)
    for index in range(0, len(keys), 1):
        if index < start:
            continue
        current_key = keys[index]
        user = await get_user_info(current_key)
        list_of_users.append(user)
        if len(list_of_users) >= limit:
            break
    return list_of_users, total




async def create_update_user(full_profile_info: FullUserProfile, user_id: Optional[int] = None) -> int:
    global profile_infos
    global users_content

    if user_id is None:
        user_id = len(profile_infos)
    liked_posts = full_profile_info.liked_posts
    short_description = full_profile_info.short_description
    long_bio = full_profile_info.long_bio

    users_content[user_id] = {"liked_posts": liked_posts}
    profile_infos[user_id] = {"short_description": short_description, "long_bio": long_bio}

    return user_id

#
async def delete_user(user_id: int) -> None:
    global profile_infos
    global users_content

    del profile_infos[user_id]
    del users_content[user_id]




@app.get("/user/me", response_model=FullUserProfile)
async def test_endpoint():
    full_user_profile = await get_user_info()
    return full_user_profile

@app.get("/user/{user_id}", response_model=FullUserProfile)
async def get_user_by_id(user_id: int):
    full_user_profile = await get_user_info(user_id)
    return full_user_profile

@app.post("/users")
async def update_user(user_id: int, full_profile_info: FullUserProfile):
    await create_update_user(full_profile_info, user_id)
    return None

@app.delete("/users/{user_id}")
async def remove_user(user_id: int):
    await delete_user(user_id)

@app.get("/users", response_model=MultipleUsersResponse)
async def get_all_users_paginated(start: int = 0, limit: int = 2):
    users, total = await get_all_users_with_pagination(start, limit)
    formatted_users = MultipleUsersResponse(users=users, total=total)
    return  formatted_users

@app.post("/users", response_model=CreateUserResponse)
async def add_user(full_profile_info: FullUserProfile):
    user_id = await create_update_user(full_profile_info)
    create_user = CreateUserResponse(user_id=user_id)
    return create_user










#
#
# #app is the variable assigned to FastAPI and so this is the endpoint
# # that returns the full profile information of a user
# #@app.get(...): This decorator defines a GET endpoint in FastAPI, a\
# # accessible at the URL path "/user/me".
# @app.get("/user/me", response_model=FullUserProfile)
# def test_endpoint():
#     full_user_profile = get_user_info()
#     return full_user_profile
#
#
# @app.get("/user/{user_id}", response_model=FullUserProfile)
# def get_user_by_id(user_id: int):
#
# """
# Endpoint for retrieving a FullUserProfile by the users's unique integer id.
# :param user_id: int - unique monotonically increasing integer id
# :return: FullUserProfile
# """
#
#
#
#
#     full_user_profile = get_user_info(user_id)
#     return full_user_profile
#
# # @app.post("/users")
# # def add_user():
# #     pass