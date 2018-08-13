from getpass import getpass
from pyvk import ClientAuth, API
from pyvk.exceptions import APIError


SERVICE_TOKEN = '66619e0066619e0066d3e34c266634f6666666' \
                                            '166619e003ea8d033c12d1a3d08e6fd55'

APP_ID = 5597286
API_VERSION = 5.80
p_photo = 4

def get_service_api():
    api = API(token=SERVICE_TOKEN, scope=p_photo, version=API_VERSION)

    return api


def get_user_api():
    user_login = input("Enter your vk.com login: ")

    try:
        auth = ClientAuth(app_id=APP_ID, username=user_login,
                                        scope=p_photo)
        auth.auth()
        api = auth.api(version=API_VERSION, lang='en')
    except APIError as exc:
        print('Error %d: %s' % (exc.error_code, exc.error_msg))
        exit(1)

    print("Authorization successful.")
    return api


if __name__ == '__main__':
    api = get_service_api()
    print(api.users.get(user_ids=1))