from database import UserQ, users_table


def create_user(new_user_dict: dict):
    return users_table.insert(new_user_dict)


def search_user(email: str):
    results = users_table.search(UserQ.email == email)
    if results:
        return results[0]
