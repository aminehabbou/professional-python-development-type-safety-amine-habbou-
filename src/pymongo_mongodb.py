from datetime import datetime
from typing import Any, Dict, Optional

from pymongo import MongoClient

MONGO_URL = "mongodb://amineh:secret2@localhost:27017/"

client: MongoClient[Any] = MongoClient(MONGO_URL)
users_collection = client.pythonde.users
football_players_collection = client.pythonde.football_players

# r = client.pythonde.command("ping")
# print("MongoDB connection:", r)

# r = client.pythonde.command("listCollections")
# print("Collections:", r)


# Define a function to insert a new user (nested profile documents exist)
def insert_new_user(
    username: str,
    email: str,
    age: int,
    city: str,
    interests: list[str],
    sports: list[str],
    salary: int,
) -> None:
    new_user = {
        "username": username,
        "email": email,
        "profile": {"age": age, "city": city, "interests": interests},
        "created_at": datetime.now(),
        "sports": sports,
        "salary": salary,
    }
    insert_result = users_collection.insert_one(new_user)
    print("inserted user ID:", insert_result.inserted_id)


# insert_new_user(
# "Jack",
# "Jack@example.com",
# 20,
# "Lille",
# ["StreetDance", "Art"],
# ["Boxing", "Handball"],
# 10000,
# )
# r_Jack = users_collection.find_one({"username": "Jack"})
# print(r_Jack["username"], r_Jack["email"])
# print(f"Jack's salary: {r_Jack['salary']}")


# Create functions to retrieve users by document filtering
# filter by username
def retrieve_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    fetched_user = users_collection.find_one({"username": username})
    if fetched_user is None:
        return None
    if "_id" in fetched_user:
        fetched_user["_id"] = str(fetched_user["_id"])
    return fetched_user  # type: ignore[no-any-return]


# Oscar = retrieve_user_by_username("oscar")
# print(Oscar)


# filter by nested field
def retrieve_user_by_age(age: int) -> list[Dict[str, Any]]:
    users_age = users_collection.find({"profile.age": age})
    users_age_list = list(users_age)
    for user in users_age_list:
        if user and "_id" in user:
            user["_id"] = str(user["_id"])  # Handle ObjectID conversion
    return users_age_list


# users_age_27 = retrieve_user_by_age(27)
# print(users_age_27)  #print the list of all dict of users aged 27


# filter by array element
def retrieve_user_by_element_of_sports(sport: str) -> list[Dict[str, Any]]:
    users_sport = users_collection.find({"sports": sport})
    users_sport_list = list(users_sport)
    for user in users_sport_list:
        if user and "_id" in user:
            user["_id"] = str(user["_id"])
    return users_sport_list


# karate_users = retrieve_user_by_element_of_sports("karate")
# for karate_user in karate_users:
# print(karate_user["username"], karate_user["email"])


# functions to update user info by MongoDB operators


# $set
def update_set_user_email(username: str, new_email: str) -> None:
    users_collection.update_one({"username": username}, {"$set": {"email": new_email}})


# $push
def update_push_interest(username: str, add_interest: str) -> None:
    users_collection.update_one(
        {"username": username}, {"$push": {"profile.interests": add_interest}}
    )


# $pull
def update_pull_sport(username: str, del_sport: str) -> None:
    users_collection.update_one(
        {"username": username}, {"$pull": {"sports": del_sport}}
    )


# update email and fetch the user with the modified email
# update_set_user_email("alice", "alice-new@example.com")
# r_alice = users_collection.find_one({"username": "alice"})
# print(r_alice["username"], r_alice["email"])

# push an additional interest to a user and fetch the user
# update_push_interest("Loe", "Skyscraping")
# r_Loe = users_collection.find_one({"username": "Loe"})
# print(r_Loe["username"], r_Loe["email"], r_Loe["profile"]["interests"])

# pull a sport from list of sports of a user and fetch the user
# update_pull_sport("oscar", "judo")
# r_oscar = users_collection.find_one({"username": "oscar"})
# print(r_oscar["username"], r_oscar["sports"])
