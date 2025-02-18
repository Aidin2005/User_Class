from datetime import datetime
import uuid
import re
import unittest

class User:
    def __init__(self, user_id, name, surname, email, password, birthday):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.birthday = datetime.strptime(birthday, "%Y-%m-%d")

    def get_details(self):
        return f"User ID: {self.user_id}, Name: {self.name}, Surname: {self.surname}, Email: {self.email}, Birthday: {self.birthday}"

    def get_age(self):
        today = datetime.now()
        age = today.year - self.birthday.year
        if today < datetime(today.year, self.birthday.month, self.birthday.day):
            age -= 1
        return age

class UserService:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def find_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def delete_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                self.users.remove(user)
                return True
        return False

    def update_user(self, user_id, new_user):
        for i, user in enumerate(self.users):
            if user.user_id == user_id:
                self.users[i] = new_user
                return True
        return False

    def get_number(self):
        return len(self.users)

class UserUtil:
    @staticmethod
    def generate_user_id():
        return str(uuid.uuid4())[:8]

    @staticmethod
    def generate_password():
        return str(uuid.uuid4())[:8]

    @staticmethod
    def generate_email(name, surname):
        return f"{name.lower()}.{surname.lower()}@example.com"

    @staticmethod
    def validate_email(email):
        return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))

    @staticmethod
    def is_strong_password(password):
        return (len(password) >= 8 and
                any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in "!@#$%^&*" for c in password))

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("1", "John", "Doe", "john.doe@gmail.com", "Password1!", "1990-01-01")

    def test_get_details(self):
        expected = "User ID: 1, Name: John, Surname: Doe, Email: john.doe@gmail.com, Birthday: 1990-01-01 00:00:00"
        self.assertEqual(self.user.get_details(), expected)
        print("Test_get_details ... ok")

    def test_get_age(self):
        today = datetime.now()
        expected_age = today.year - 1990
        if today < datetime(today.year, 1, 1):
            expected_age -= 1
        self.assertEqual(self.user.get_age(), expected_age)
        print("Test_get_age ... ok")

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()
        self.user = User("1", "John", "Doe", "john.doe@gmail.com", "Password1!", "1990-01-01")
        self.user_service.add_user(self.user)

    def test_add_user(self):
        self.assertEqual(self.user_service.get_number(), 1)
        print("Test_add_User ... ok")

    def test_find_user(self):
        user = self.user_service.find_user("1")
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "John")
        print("Test_find_User ... ok")

    def test_delete_user(self):
        self.assertTrue(self.user_service.delete_user("1"))
        self.assertEqual(self.user_service.get_number(), 0)
        print("Test_delete_User ... ok")

    def test_update_user(self):
        new_user = User("1", "Jane", "Doe", "jane.doe@gmail.com", "NewPassword1!", "1992-02-02")
        self.assertTrue(self.user_service.update_user("1", new_user))
        updated_user = self.user_service.find_user("1")
        self.assertEqual(updated_user.name, "Jane")
        print("Test_Update ... ok")

class TestUserUtil(unittest.TestCase):
    def test_generate_user_id(self):
        user_id = UserUtil.generate_user_id()
        self.assertEqual(len(user_id), 8)
        print("Test_Generate_id ... ok")

    def test_generate_password(self):
        password = UserUtil.generate_password()
        self.assertEqual(len(password), 8)
        print("Test_Generate_Password ... ok")

    def test_generate_email(self):
        email = UserUtil.generate_email("John", "Doe")
        self.assertEqual(email, "john.doe@example.com")
        print("Test_Generate_email ... ok")

    def test_validate_email(self):
        self.assertTrue(UserUtil.validate_email("test@example.com"))
        self.assertFalse(UserUtil.validate_email("testexample.com"))
        print("Test_email ... ok")

    def test_is_strong_password(self):
        self.assertTrue(UserUtil.is_strong_password("Password1!"))
        self.assertFalse(UserUtil.is_strong_password("weak"))
        print("Test_password ... ok")

if __name__ == "__main__":
    unittest.main()
