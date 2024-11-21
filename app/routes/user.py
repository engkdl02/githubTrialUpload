import time
from http.client import responses
from pipenv.cli.options import pass_state
from telnetlib import STATUS

from fastapi import APIRouter, HTTPException, Response, Depends


from fastapi import APIRouter, HTTPException


from app.schemas.user import (
    CreateUserResponse,
    FullUserProfile,
    MultipleUsersResponse,
)
from app.services.user import UserService
import logging
from app.dependencies import rate_limit


logger = logging.getLogger(__name__)
# logging.basicConfig(
#     format="%(levelname) %(name) %(asctime) %(message)s",
#     datefmt="%y-%m-%d",
#     filename="log.txt",
# )
# logger.setLevel(logging.INFO) #debug -> info -> warning -> error -> critical
#
# console = logging.StreamHandler()
# logger.addHandler(console)



def create_user_router(profile_infos: dict, users_content: dict) -> APIRouter():
    user_router = APIRouter(
        prefix="/user",
        tags=["user"],
        dependencies = [Depends(rate_limit)]
    )
    user_service = UserService(profile_infos, users_content)

    @user_router.get("/all", response_model=MultipleUsersResponse)
    async def get_all_users_paginated(start: int = 0, limit: int = 2):
        users, total = await user_service.get_all_users_with_pagination(start, limit)
        formatted_users = MultipleUsersResponse(users=users, total=total)
        return formatted_users

    # @user_router.get("/user/me", response_model=FullUserProfile)
    # async def test_endpoint():
    #     full_user_profile = await user_service.get_user_info()
    #     return full_user_profile

    @user_router.get("/{user_id}", response_model=FullUserProfile)
    async def get_user_by_id(user_id: int):  #, response: Response = Depends(rate_limit)
        # try:
        # rate_limit(response)
        full_user_profile = await user_service.get_user_info(user_id)
        # response.headers["test-additional-header-value"] = "this is just something i'm adding"
        return full_user_profile

        # except KeyError:
        #     logger.error(f"Non-existent user_id{user_id} was requested")
        #     raise HTTPException(status_code=404, detail="User doesn't exist")
        #     return full_user_profile
        # try:
        #     full_user_profile = await user_service.get_user_info(user_id)
        # except KeyError:
        #     logger.error(f"Non-existent user_id{user_id} was requested")
        #     raise HTTPException(status_code=404, detail="User doesn't exist")
        #     return full_user_profile

    @user_router.post("/users")
    async def update_user(user_id: int, full_profile_info: FullUserProfile):
        await user_service.create_update_user(full_profile_info, user_id)
        return None

    @user_router.delete("/{user_id}")
    async def remove_user(user_id: int):
        await user_service.delete_user(user_id)
        # logger.debug("this is a debug log")
        # logger.info(f"Invalid uder id {user_id}")
        # try:
        #     await user_service.delete_user(user_id)
        # except KeyError:
        #
        #     raise  HTTPException(status_code=404 , detail ={"msg": f"User doesn't exist", "user_id": user_id} )


    @user_router.post("/", response_model=CreateUserResponse,status_code=201)
    async def add_user(full_profile_info: FullUserProfile):
        user_id = await user_service.create_update_user(full_profile_info)
        create_user = CreateUserResponse(user_id=user_id)
        return create_user

    return user_router