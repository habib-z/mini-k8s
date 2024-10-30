from app.entity.user import User
from app.repository.database import Database
from app.repository.user_repository import UserRepository






class UserService:

    @staticmethod
    def create_user(user_name:str, database:Database)->User:
        return UserRepository.create_user(user_name,database)

    @staticmethod
    def find_user(user_name:str, database:Database)->User:
        return UserRepository.find_user(user_name,database)