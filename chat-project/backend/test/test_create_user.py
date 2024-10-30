from unittest import TestCase

from app.db import create_default_db

from app.entity.user import User
from app.repository.user_repository import DuplicateUserNameException, UserNameNotFoundException
from app.services.user_service import UserService


class TestCreateAndFindUser(TestCase):

    def test_create_user_with_name(self):
        database=create_default_db()
        database.remove()
        user=UserService.create_user("sara", database)
        self.assertIsInstance(user,User)


    def __create_duplicate_user_name(self):
        database = create_default_db()
        database.remove()
        user = UserService.create_user("sara", database)
        user = UserService.create_user("sara", database)

    def test_raise_duplicate_exception_if_user_name_exist(self):
        with self.assertRaises(DuplicateUserNameException) as context:
            self.__create_duplicate_user_name()


    def test_find_user_name(self):
        database = create_default_db()
        database.remove()
        _ = UserService.create_user("sara", database)
        user=UserService.find_user("sara", database)
        self.assertIsInstance(user,User)

    def test_raise_user_name_not_found_exception_if_user_name_not_found(self):
        with self.assertRaises(UserNameNotFoundException) as context:
            database = create_default_db()
            database.remove()
            _ = UserService.create_user("sara", database)
            user=UserService.find_user("ali", database)

