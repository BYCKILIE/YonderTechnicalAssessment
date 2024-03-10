import os
import inspect
import time

from dataextractor import DataExtractor
from excelcreator import ExcelCreator

URL = 'http://localhost:30000'

ENDPOINT_DRIVER_LICENSE = '/drivers-licenses/list'

LICENSE_COUNT = 150


class Application:

    def __init__(self, url, endpoint):
        self.__driving_licenses = DataExtractor(url, endpoint)
        self.__driving_licenses.extract(LICENSE_COUNT)

        self.__options = self.__build_options_list()

    # extracts from the class specified all the methods in the class and filters them based on
    # what method has the decorator "nametag"
    @staticmethod
    def __build_options_list():
        return {
            method.__nametag__[DataExtractor.TAG_ID]: method
            for _, method in inspect.getmembers(DataExtractor, inspect.isfunction)
            if hasattr(method, '__nametag__')
        }

    # printing format for the menu
    @staticmethod
    def __print_options(options: dict):
        os.system('cls')
        for i in range(1, len(options) + 1):
            if i in options.keys():
                print(f"{i}. {options[i].__nametag__[DataExtractor.TAG_NAME]}")
        print('Type "0" to exit the program', end='\n\n')

    def running_loop(self):
        while True:
            self.__print_options(self.__options)
            op = int(input('Select Option: '))
            if op == 0:
                break
            if op not in self.__options.keys():
                continue

            os.system('cls')
            print(f'Executing {self.__options[op].__nametag__[DataExtractor.TAG_NAME]}')

            data = self.__options[op](self.__driving_licenses)
            print('Building Excel File...')

            # try-except block for not crashing the application in special cases ex:
            # if you try to write an exel at a path where it already exists (that's not the problem)
            # and it is also opened
            try:
                ex = ExcelCreator(data)
                ex.create_file(f'{self.__options[op].__nametag__[DataExtractor.TAG_NAME]} Report')

                if ex.fail():
                    print('Exel File Failed to Build!')
                else:
                    print('Excel File Built Successfully!')
            except:
                print('An error occurred\nExcel file may be opened')
                time.sleep(1)
            # sleep added to give the user time to receive the app feedback
            time.sleep(1)


def main():
    app = Application(URL, ENDPOINT_DRIVER_LICENSE)
    app.running_loop()


if __name__ == '__main__':
    main()
