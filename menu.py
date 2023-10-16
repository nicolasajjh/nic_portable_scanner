import os
from country_info import country_code_to_name

def country_list():#print all country
    countries=os.listdir(r"/country")
    a=1
    for country in countries:
        # print(country)
        print(a,country,country_code_to_name(country))
        a+=1

if __name__ == "__main__":
    country_list()

# print(os.path.dirname(os.path.abspath(__file__)))