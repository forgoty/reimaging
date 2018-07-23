import vk_requests as vk


SERVICE_TOKEN = '66619e0066619e0066d3e34c266634f6666666' \
                                            '166619e003ea8d033c12d1a3d08e6fd55'


def auth():
    api = vk.create_api(service_token=SERVICE_TOKEN, scope='photo')
    return api


if __name__ == '__main__':
    api = auth()
    print(api.users.get(user_ids=1))