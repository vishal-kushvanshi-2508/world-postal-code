
from extract_data import *
import time
from store_data_database import *
from pages_request_city_data import *

# file_name = "Domino's Pizza Restaurants in Mumbai _ Nearby Pizza Shops in Mumbai – Domino’s India.html"
base_url = "https://worldpostalcode.com"


def main():
    ## city name and url for table crate
    create_table_country_url()
    print("table created")
    
    # create url list and status default pending
    country_url_list = generate_url(base_url)

    # insert url data in table
    country_url_insert(list_data=country_url_list)

    # fetch book url data
    country_data_list = fetch_country_table_data()
    print(len(country_data_list))

    # # print(book_data_list)

    # # create table for product.    
    # create_table_product()
    
    # create table region
    create_table_region()

    create_table_area()

    create_table_postal()

    fetch_region_data(country_data_list, base_url)

    # # create html file and extract pages data.
    # create_html_files(book_data_list)


if __name__ == "__main__":
    start = time.time()
    main()

    end = time.time()
    print("time different  : ", end - start)


