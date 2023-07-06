from abc import ABC, abstractmethod

class Filter(ABC):
    # Side effect: modify house_list
    @abstractmethod
    def filter_address(self, house_list, filter_str):
        pass

class Filter51(Filter):
    # Side effect: modify house_list
    def filter_address(self, house_list, filter_str):
        addresses = house_list["addresses"]

        # Reversely pop unwanted result to prevent list suppressing issue
        for i in reversed(range(len(addresses))):
            if filter_str not in addresses[i]:
                # Remove the ith element for each list in house_list dictionary
                for value in house_list.values():
                    value.pop(i)

        return house_list