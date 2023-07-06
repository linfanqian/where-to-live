from abc import ABC, abstractmethod
import random
import requests

class Request(ABC):
    def __init__(self, ):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        self.ip_pool = [
            # TODO: fulfill ip pool
        ]

    def set_proxies(self):
        proxy = random.choice(self.ip_pool)
        proxies = {"http": proxy, "https": proxy}
        return proxies

    def make_request(self, url):
        response = requests.get(url, headers=self.headers)
        return response.text

    @abstractmethod
    def construct_url(self, page, filters):
        pass

class Request51(Request):
    def construct_url(self, page, filters):
        base_url = 'https://house.51.ca/rental'
        page_str = f'?page={page}'
        price_str = ''
        building_type_str = ''
        include_water_str = ''
        include_hydro_str = ''
        include_internet_str = ''
        independent_kitchen_str = ''
        independent_bathroom_str = ''

        lowest_price = filters['lowest_price']
        highest_price = filters['highest_price']
        building_types = filters['building_types']
        include_water = filters['include_water']
        include_hydro = filters['include_hydro']
        include_internet = filters['include_internet']
        independent_kitchen = filters['independent_kitchen']
        independent_bathroom = filters['independent_bathroom']

        if lowest_price or highest_price:
            lowest_price_str = ''
            highest_price_str = ''

            if lowest_price:
                lowest_price_str = f'[{lowest_price}'
            else:
                lowest_price_str = '('

            if highest_price:
                highest_price_str = f'{highest_price}]'
            else:
                highest_price_str = ')'
            price_str = f'&priceRange={lowest_price_str}%2C{highest_price_str}'
        
        if building_types:
            building_type_dict = building_types.split(", ")
            building_type_map = {
                'CONDO': 'apartment',
                'TOWNHOUSE': 'townhouse',
                'SEMI-DETACHED': 'semi-detached',
                'DETACHED': 'detached'
            }
            building_type_str += f'&buildingTypes={building_type_map[building_type_dict[0]]}'
            for i in range(1, len(building_type_dict)):
                building_type_str += f'%2C{building_type_map[building_type_dict[i]]}'

        if include_water:
            include_water_str = '&includesWater=1'

        if include_hydro:
            include_hydro_str = '&includesHydro=1'

        if include_internet:
            include_internet_str = '&includesInternet=1'

        if independent_kitchen:
            independent_kitchen_str = '&independentKitchen=1'

        if independent_bathroom:
            independent_bathroom_str = '&independentBathroom=1'

        url = base_url + page_str + price_str + building_type_str + \
              include_water_str + include_hydro_str + include_internet_str + \
              independent_kitchen_str + independent_bathroom_str
        return url