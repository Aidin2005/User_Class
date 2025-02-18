from datetime import datetime
import random
import string
import re

class User:
    def __init__(self, user_id, name, surname, email, password, birthday):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.birthday = datetime.strptime(birthday, "%Y-%m-%d")

    def get_details(self):
        return (f"ID: {self.user_id}\n"
                f"Name: {self.name}\n"
                f"Surname: {self.surname}\n"
                f"Email: {self.email}\n"
                f"Password: {self.password}\n"
                f"Birthday: {self.birthday.date()}")

    def get_age(self):
        today = datetime.now()
        age = today.year - self.birthday.year
        if today < datetime(today.year, self.birthday.month, self.birthday.day):
            age -= 1
        return age

class UserService:
    users = {}

    @classmethod
    def add_user(cls, user):
        cls.users[user.user_id] = user

class UserUtil:
    @staticmethod
    def generate_user_id():
        year = str(datetime.now().year)[-2:]  
        random_digits = ''.join(random.choices(string.digits, k=7))
        return year + random_digits

    @staticmethod
    def generate_password():
        while True:
            password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=10))
            if UserUtil.is_strong_password(password):
                return password

    @staticmethod
    def is_strong_password(password):
        return (len(password) >= 8 and
                any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in "!@#$%^&*" for c in password))

    @staticmethod
    def generate_email(name, surname, domain="gmail.com"):
        return f"{name.lower()}.{surname.lower()}@{domain}"

    @staticmethod
    def validate_email(email):
        return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))

if __name__ == "__main__":
    print("Создание нового пользователя:")
    user_id = UserUtil.generate_user_id()
    name = input("Введите имя: ")
    surname = input("Введите фамилию: ")
    email = UserUtil.generate_email(name, surname)
    password = UserUtil.generate_password()
    birthday = input("Введите дату рождения (YYYY-MM-DD): ")

    if not UserUtil.validate_email(email):
        print("Ошибка: Некорректный email.")
    else:
        user = User(user_id, name, surname, email, password, birthday)
        UserService.add_user(user)

        print("\nUser added successfully!")
        print(user.get_details())
        print(f"\nUser age: {user.get_age()}")
        print(f"\nEmail validation: {email} is valid email")
        print(f"Password strength: {password} is strong.")