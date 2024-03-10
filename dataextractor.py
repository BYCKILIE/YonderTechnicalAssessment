import requests
from datetime import datetime


class DataExtractor:
    TAG_ID = 0
    TAG_NAME = 1

    __drivers_licenses = None

    def __init__(self, url, endpoint):
        self.__url = url
        self.__endpoint = endpoint

    # custom decorator function to set nametags for methods
    @staticmethod
    def nametag(number, tag):
        def decorator(func):
            func.__nametag__ = (number, tag)
            return func

        return decorator

    def extract(self, count=None):
        params = {
            'length': str(count) if count is not None else '30',
        }

        try:
            response = requests.get(url=self.__url + self.__endpoint, params=params)
            if response.status_code == 200:
                self.__drivers_licenses = response.json()
            else:
                print(f"Error in GET method: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error to query the data: {e}")

    # nametags are added before methods that will be present in the application console menu
    @nametag(1, "Suspended Drivers Licenses")
    def find_suspended_licenses(self):
        return [
            driver_license
            for driver_license in self.__drivers_licenses
            if driver_license['suspendat']
        ]

    @nametag(2, "Available Drivers Licenses")
    def find_available_licenses(self):
        today = datetime.today()
        return [
            driver_license
            for driver_license in self.__drivers_licenses
            if datetime.strptime(driver_license['dataDeExpirare'], '%d/%m/%Y') > today
        ]

    @nametag(3, "Drivers Licenses Count by Category")
    def find_count_based_on_category(self):
        license_categories = {i['categorie'] for i in self.__drivers_licenses}
        return sorted([
            {
                'categorie': category,
                'total': sum(
                    1 for driver_license in self.__drivers_licenses if driver_license['categorie'] == category
                )
            }
            for category in license_categories
        ], key=lambda ref: ref['categorie'])
