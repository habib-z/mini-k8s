from app.entity.user import User
from app.repository.database import Database


class DuplicateUserNameException(Exception):
    def __init__(self,msg:str=""):
        super().__init__(msg)

class UserNameNotFoundException(Exception):
    def __init__(self,msg:str=""):
        super().__init__(msg)
class UserRepository:
    @staticmethod
    def create_user(user_name: str,database:Database) -> User:
        with database:
            result=database.create_user_name(user_name)
            if(result):
                return User(user_name)
            raise DuplicateUserNameException(f'duplicate. user_name {user_name} is already exist.')

    @staticmethod
    def find_user(user_name: str,database:Database) -> User:
        with database:
            user=database.get_user_by_name(user_name)
            # if not user:
            #     raise UserNameNotFoundException(f"user with user name {user_name} not found.")
            return user
