from datetime import datetime
from typing import Any, Optional

from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    ListField,
    StringField,
    connect,
)

MONGO_URL = "mongodb://amineh:secret2@localhost:27017/"

connect("pythonde", host=MONGO_URL)


class Profile(EmbeddedDocument):  # type: ignore[misc]
    age = IntField(min_value=0, max_value=120)
    city = StringField(max_length=100)
    interests = ListField(StringField(max_length=70))


class User(Document):  # type: ignore[misc]
    username = StringField(required=True, unique=True, max_length=50)
    email = StringField(required=True)
    profile = EmbeddedDocumentField(Profile)
    created_at = DateTimeField(default=datetime.utcnow)
    sports = ListField(StringField(max_length=40))
    salary = IntField(min_value=2000, max_value=70000)

    meta = {"collection": "users"}


class Player(Document):  # type: ignore[misc]
    name = StringField(required=True, unique=True, max_length=90)
    nationality = StringField(max_length=50)
    position = StringField(max_length=100)
    titles_won = IntField()
    previous_clubs = ListField(StringField(max_length=70))

    meta = {"collection": "footbal_players"}


def list_all_users() -> list[User]:
    return list(User.objects.all())


# list_users = list_all_users()
# for user in list_users:
#    print(user.username, user.email)


def find_user_by_username(username: str) -> User | None:
    try:
        return User.objects.get(username=username)  # type: ignore[no-any-return]
    except User.DoesNotExist:
        return None


# r_Jack = find_user_by_username("Jack")
# print(r_Jack["username"], r_Jack["email"], r_Jack["salary"])


def retrieve_user_by_age(age: int) -> list[User]:
    try:
        return list(User.objects(profile__age=age))
    except Exception:
        return []


# r_age_21 = retrieve_user_by_age(21)
# for user in r_age_21:
# print(user.username, user.email, user.profile.age)


def retrieve_user_by_element_of_sports(sport: str) -> list[User]:
    try:
        return list(User.objects(sports=sport))
    except Exception:
        return []


# r_sport_basketball = retrieve_user_by_element_of_sports("basketball")
# for user in r_sport_basketball:
# print(user.username, user.email, user.profile.age, user.sports)


def create_user(
    username: str,
    email: str,
    age: Optional[int] = None,
    city: Optional[str] = None,
    interests: Optional[list[str]] = None,
    sports: Optional[list[str]] = None,
    salary: Optional[int] = None,
) -> User:
    user = User(username=username, email=email)
    if age or city or interests:
        profile = Profile()
        if age:
            profile.age = age
        if city:
            profile.city = city
        if interests:
            profile.interests = interests
        user.profile = profile
    if sports or salary:
        if sports:
            user.sports = sports
        if salary:
            user.salary = salary
    user.save()
    return user


# r_insert_Leva =create_user("Leva", "Leva@example.com", 21, "Chicago", ["Watching TV"])
# print(r_insert_Leva.username, r_insert_Leva.email, r_insert_Leva.profile.age)


def update_user(username: str, **updates: Any) -> bool:
    try:
        user = User.objects.get(username=username)
        profile_updates = {}
        user_updates = {}

        for key, value in updates.items():
            if key in [
                "age",
                "city",
                "interests",
            ]:
                profile_updates[key] = value
            elif key in ["sports", "salary", "email"]:
                user_updates[key] = value
        if profile_updates:
            if not user.profile:
                user.profile = Profile()
            for key, value in profile_updates.items():
                setattr(user.profile, key, value)
        if user_updates:
            for key, value in user_updates.items():
                setattr(user, key, value)

        user.save()
        return True

    except User.DoesNotExist:
        return False


# update_user("alice", salary=6000, age=31, interests=["Boxing", "Swimming"])
# r_alice = find_user_by_username("alice")
# print(
# r_alice.username,
# r_alice.email,
# r_alice.salary,
# r_alice.profile.interests,
# r_alice.profile.age,
# )


users_list = list_all_users()
print("LIST OF ALL USERS:")
for user in users_list:
    print(
        f"username:'{user.username}', "
        f"email:'{user.email}', "
        f"age:{user.profile.age}, "
        f"city: '{user.profile.city}', "
        f"interests:'{user.profile.interests}', "
        f"sports:'{user.sports}', "
        f"salary: {user.salary}"
    )
