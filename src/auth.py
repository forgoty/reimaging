from pyvk import ClientAuth, API


SERVICE_TOKEN = '66619e0066619e0066d3e34c266634f6666666' \
                                            '166619e003ea8d033c12d1a3d08e6fd55'
APP_ID = 5597286
API_VERSION = 5.80
PHOTO_SCOPE = 4


def get_service_api():
    api = API(token=SERVICE_TOKEN, scope=PHOTO_SCOPE, version=API_VERSION)
    return api


def get_user_api():
    auth = ClientAuth(app_id=APP_ID, scope=PHOTO_SCOPE)
    auth.auth()
    api = auth.api(version=API_VERSION, lang='en')

    print("Authorization successful.")
    return api


if __name__ == '__main__':
    api = get_user_api()
    print(api.users.get(user_ids=1))