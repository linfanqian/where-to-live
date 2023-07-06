from abc import ABC, abstractmethod

from .request import Request51
from .cleaner import Cleaner51
from .filter import Filter51

class Crawler(ABC):
    @abstractmethod
    def get_house_list(self, filters):
        pass

class Crawler51(Crawler):
    def get_house_list(self, filters):
        request = Request51()
        request_url = request.construct_url(1, filters)
        response_text = request.make_request(request_url)
        crawler_cleaner = Cleaner51(response_text)
        house_list = crawler_cleaner.get_cleaned_house_list()
        crawler_filter = Filter51()
        house_list = crawler_filter.filter_address(house_list, filters['location'])

        result_list = []
        for i in range(len(house_list['titles'])):
            title = house_list['titles'][i]
            address = house_list['addresses'][i]
            price = house_list['prices'][i]
            available_time = house_list['available_times'][i]
            requirement = ' '.join(house_list['requirements'][i])
            package = house_list['packages'][i]
            tag = ' '.join(house_list['tags'][i])
            link = house_list['links'][i]
            house_info = f'Title: {title}\n' + \
                         f'Address: {address}\n' + \
                         f'Price: {price}\n' + \
                         f'Available Time: {available_time}\n' + \
                         f'Requirement: {requirement}\n' + \
                         f'Package: {package}\n' + \
                         f'Tag: {tag}\n' + \
                         f'Link: {link}\n'
            result_list.append(house_info)

        return result_list