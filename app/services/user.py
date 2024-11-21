from typing import Optional, Tuple, List
from app.schemas.user import (
    CreateUserResponse,
    FullUserProfile,
    MultipleUsersResponse,
    User
)


from app.exceptions import UserNotFound
# ----------------------------------------------
# a dictionary
# the 0 is a unique user id and maps to its user info

# profile_infos = {
#     0: {
#         "short_description": "My bio description",
#         "long_bio": "this is our longer bio"
#     }
# }
#
# users_content = {
#     0: {
#         "name": "default_user",
#         "liked_posts": [1] * 9,
#     },
#
# }

# ----------------------------------------------

class UserService:

    def __init__(self, profile_infos: dict, user_content:dict):
        self.profile_infos = profile_infos
        self.users_content = user_content

    async def get_all_users_with_pagination(self, start: int, limit: int) -> Tuple[List[FullUserProfile], int]:
        list_of_users = []
        keys = list(self.profile_infos.keys())
        total = len(keys)
        for index in range(0, len(keys), 1):
            if index < start:
                continue
            current_key = keys[index]
            user = await self.get_user_info(current_key)
            list_of_users.append(user)
            if len(list_of_users) >= limit:
                break
        return list_of_users, total


    async def get_user_info(self, user_id: int = 0) -> FullUserProfile:

        if user_id not in self.profile_infos:
            raise UserNotFound(user_id=user_id)
        # currently reading from the dictionary
        # retrieves the profile_info data and then store it into a variable
        profile_info = self.profile_infos[user_id]
        # get returns a value for key if key is a dictionary
        user_content = self.users_content.get(user_id)

        # later read from database
        # db case here we can await
        # await db read ... user_id

        # the User class is used and the value of user_content is passed
        user = User(**user_content)

        #
        full_user_profile_data = {
            **profile_info,
            **user.model_dump()
        }

        return FullUserProfile(**full_user_profile_data)

    async def create_update_user(self,full_profile_info: FullUserProfile, user_id: Optional[int] = None) -> int:
        # global profile_infos
        # global users_content

        if user_id is None:
            user_id = len(self.profile_infos)
        liked_posts = full_profile_info.liked_posts
        short_description = full_profile_info.short_description
        long_bio = full_profile_info.long_bio

        self.users_content[user_id] = {"liked_posts": liked_posts}
        self.profile_infos[user_id] = {"short_description": short_description, "long_bio": long_bio}

        return user_id

    async def delete_user(self,user_id: int) -> None:
        # global profile_infos
        # global users_content

        if user_id not in self.profile_infos:
            raise UserNotFound(user_id=user_id)

        del self.profile_infos[user_id]
        del self.users_content[user_id]
