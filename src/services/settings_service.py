from db_models.base import Session
from db_models.models import Settings


def get_settings():
    """
    Get all events from the database.

    :return: a dictionary of settings
    """
    session = Session()
    settings = session.query(Settings).all()
    session.close()

    # Map the settings to a dictionary
    settings_dict = {setting.setting_name: setting.setting_value for setting in settings}

    return settings_dict


def update_setting(setting_name: str, setting_value: str):
    """
    Update a setting in the database.

    :param setting_name: the name of the setting to update
    :param setting_value: the value of the setting
    """
    session = Session()
    setting = session.query(Settings).filter_by(setting_name=setting_name).first()
    setting.setting_value = setting_value
    session.commit()
    session.close()
