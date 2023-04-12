from dataclasses import dataclass
from random import choice


@dataclass
class User:
    id_: int
    first_name: str
    last_name: str
    avatar_link: str
    gamescore: float


users = list()
brackets = dict()


class DataBase:
    async def fill_users():
        users.append(User(123456789, 'John', 'Doe',
                     'AgACAgIAAxkDAAPLZCxQQeV668Tl_px_LRHoQ5wVF4sAArKpMRtb5loF96cyWNT12NsBAAMCAANjAAMvBA', 0))
        users.append(User(987654321, 'Ivan', 'Ivanov',
                     'AgACAgIAAxkDAAPLZCxQQeV668Tl_px_LRHoQ5wVF4sAArKpMRtb5loF96cyWNT12NsBAAMCAANjAAMvBA', 0))
        users.append(User(123987456, 'Trover', 'Universe',
                     'AgACAgIAAxkDAAPLZCxQQeV668Tl_px_LRHoQ5wVF4sAArKpMRtb5loF96cyWNT12NsBAAMCAANjAAMvBA', 0))

    async def check_users_amount():
        return True if len(users) > 2 else False
    
    # Functions for working with users
    async def add_user(id_: int, first_name: str, last_name: str, score: float, avatar_link: str):
        users.append(User(id_, first_name, last_name, avatar_link, score))
        # print(users)

    async def get_user(id_: int):
        for user in users:
            if user.id_ == id_:
                return user

    async def get_user_name(id_: int):
        for user in users:
            if user.id_ == id_:
                return f'{user.first_name} {user.last_name}'

    async def update_user(id_: int, first_name: str, last_name: str, score: float, avatar_link: str):
        for user in users:
            if user.id_ == id_:
                user.first_name = first_name
                user.last_name = last_name
                user.gamescore = score
                user.avatar_link = avatar_link

    async def delete_user(id_: int):
        for user in users:
            if user.id_ == id_:
                users.remove(user)

    async def update_user_score(id_: int, score: float):
        for user in users:
            if user.id_ == id_:
                user.gamescore = score

    async def reset_score(id_: int):
        for user in users:
            if user.id_ == id_:
                user.gamescore = 0

    async def clear_users():
        users.clear()

    async def get_users():
        return users

    async def get_users_names():
        names = []
        for user in users:
            name = f'{user.first_name} {user.last_name}'
            names.append(name)
        return names

    async def save_bracket(id_: int, bracket: list):
        brackets.setdefault(id_, bracket)

    async def get_bracket(user_id: int):
        return brackets.get(user_id)
