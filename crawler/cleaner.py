from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

class Cleaner(ABC):
    def __init__(self, html):
        self.html = html

    @abstractmethod
    def get_cleaned_house_list(self):
        pass

class Cleaner51(Cleaner):
    def __append_cleaned_house(self, house, house_list):
        raw_title = house.find("span", {"class": "title"})
        raw_address = house.find("span", {"class": "address"})
        raw_price = house.find("div", {"class": "pricing"}).find('b')
        raw_available_time = house.find("span", {"class", "available-time"})
        raw_requirement = house.find("div", {"class": "requirements-wrap"})
        raw_package = house.find("span", {"class": "package"})
        raw_tag = house.find("div",  {"class": "listing-tags"})

        # remove advertisements
        if ((raw_title is None) or (raw_address is None) or 
            (raw_price is None) or (raw_available_time is None)):
            return

        # convert infos in html to normal strings and store in house_list 
        title = raw_title.contents[0].replace("\n", "").strip()
        house_list["titles"].append(title)
        
        address = raw_address.contents[0].replace(" ", "").replace("\n", "")
        house_list["addresses"].append(address)
        
        price = raw_price.contents[0]
        house_list["prices"].append(price)
        
        available_time = raw_available_time.contents[0].strip()
        house_list["available_times"].append(available_time)
        
        requirement_list = []  # a house can have many requirements
        if raw_requirement is not None:
            for requirement in raw_requirement.find_all("span"):
                requirement_list.append(requirement.contents[0])
        house_list["requirements"].append(requirement_list)

        package = ""
        if raw_package is not None:
            package = raw_package.contents[0].strip()
        house_list["packages"].append(package)

        tag_list = []  # a house can have many tags
        if raw_tag is not None:
            for tag in raw_tag.find_all("b"):
                tag_list.append(tag.contents[0])
        house_list["tags"].append(tag_list)

        link = "https://house.51.ca/" + house.get("href")
        house_list["links"].append(link)

    def get_cleaned_house_list(self):
        house_list = {
            "titles": [],
            "addresses": [],
            "prices": [],
            "available_times": [],
            "requirements": [],
            "packages": [],
            "tags": [],
            "links": []
        }

        soup = BeautifulSoup(self.html)

        # recommended houses (info in html format)
        raw_list_recommended = soup.find_all("a", {"class": "recommend-item"})
        for house in raw_list_recommended:
            self.__append_cleaned_house(house, house_list)

        # normal houses (info in html format)
        raw_list_normal = soup.find_all("a", {"class": "wg51__rental-list-item"})
        for house in raw_list_normal:
            self.__append_cleaned_house(house, house_list)

        return house_list