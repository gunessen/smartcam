from db_models.base import Session
from db_models.models import User


def authenticate_user(username: str, password: str):
    """
    Authenticate user by username and password

    :param username: str
    :param password: str
    :return: bool
    """
    session = Session()
    user = (
        session.query(User).filter(User.username == username and User.password == password).first()
    )
    session.close()
    if user:
        return True

    return False


def get_emails():
    """
    Get emails of all users

    :return: list
    """
    session = Session()
    users = session.query(User).all()
    session.close()
    return [user.email for user in users]
