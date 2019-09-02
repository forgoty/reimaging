from getpass import getpass

from aiovk import TokenSession, API, ImplicitSession, drivers
from aiovk.mixins import SimpleImplicitSessionMixin


SERVICE_TOKEN = '66619e0066619e0066d3e34c266634f6666666' \
                                            '166619e003ea8d033c12d1a3d08e6fd55'
APP_ID = 5597286


class SimpleImplicitSession(SimpleImplicitSessionMixin, ImplicitSession):
    pass


def get_service_api():
    session = TokenSession(access_token=SERVICE_TOKEN,)
    api = API(session)
    return api


def get_user_api(driver=drivers.HttpDriver()):
    user = input('Login: ')
    password = getpass()

    session = SimpleImplicitSession(
        login=user,
        password=password,
        app_id=APP_ID,
        scope='photos',
        driver=driver
    )
    api = API(session)

    return api
