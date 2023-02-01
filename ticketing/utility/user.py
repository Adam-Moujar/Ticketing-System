from ticketing.models import User

def get_user(id):
    try:
        user = User.objects.get(id = id)

    except  User.DoesNotExist:

        return None

    return user


def get_user_by_email(email):
    try:
        user = User.objects.get(email = email)

    except  User.DoesNotExist:
        return None

    return user

def user_exists_by_email(email):
    if get_user_by_email(email):
        return True
    else:
        return False