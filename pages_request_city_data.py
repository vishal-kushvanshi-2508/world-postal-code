
import os
import requests

from lxml import html
from urllib.parse import urljoin



from store_data_database import *



def extract_data_from_html(html_data):
    tree = html.fromstring(html_data)

    data_list = []

    paths_for_loop = tree.xpath("//div[contains(@class,'quoteDetails')]")

    for path_data in paths_for_loop:
        quote_data = {}

        quote_data["quote"] = path_data.xpath(".//div[@class='quoteText']//text()")[0].replace("\n", "").strip()

        author_list = path_data.xpath(".//span[@class=\"authorOrTitle\"]/text()")#[0].replace("\n", "").strip()
        quote_data["author"] = author_list[0].strip() if author_list else ""


        author_url_list = path_data.xpath("//div[contains(@class,'quoteDetails')]/a/@href")
        quote_data["author_url"] = urljoin("https://www.goodreads.com", author_url_list[0]) if author_url_list else ""

        likes_list = path_data.xpath('.//a[@class="smallText"]/text()')
        quote_data["likes"] = likes_list[0].strip() if likes_list else ""


        tags_list = path_data.xpath(".//div[contains(@class,'greyText')]/a/text()")
        quote_data["tag"] = ",".join([tag.strip() for tag in tags_list if tag.strip()])

        data_list.append(quote_data)

    return data_list



import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


# # ---------- WORKER FUNCTION ----------
def process_book(book, headers, folder_path):
    book_id = book["id"]
    book_url = book["website_link"]

    try:
        response = requests.get(book_url, headers=headers)

        if response.status_code != 200:
            print(f"Failed: {book_url} ({response.status_code})")
            return []

        # safe filename
        file_path = os.path.join(folder_path, f"{book_id}.html.gz")

        # save html
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        # extract data
        book_list = extract_data_from_html(response.text)

        # update book url table status column 
        update_book_url_status(book_id)

        return book_list

    except Exception as e:
        print(f"Error for {book_url}: {e}")
        return []




# ---------- MAIN FUNCTION ----------
def create_html_files(book_data_list):

    folder_path = r"D:/vishal_kushvanshi/quotes/"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://stores.burgerking.in/location/haryana',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
    }

    books_all_data_list = []

    # Thread pool
    with ThreadPoolExecutor(max_workers=10) as executor:

        futures = [
            executor.submit(process_book, book, headers, folder_path)
            for book in book_data_list
        ]
        
        for future in as_completed(futures):
            
            result = future.result()   # list from each thread
            books_all_data_list.extend(result)

    # insert after all threads complete
    if books_all_data_list:
        product_data_insert(list_data=books_all_data_list)

    print("Total records add :", len(books_all_data_list))
















### without threading code 



# def create_html_files(book_data_list):

#     folder_name = "city_html_files"
#     os.makedirs(folder_name, exist_ok=True)

#     headers = {
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#         'accept-language': 'en-US,en;q=0.9',
#         'cache-control': 'no-cache',
#         'pragma': 'no-cache',
#         'priority': 'u=0, i',
#         'referer': 'https://stores.burgerking.in/location/haryana',
#         'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'document',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-site': 'same-origin',
#         'sec-fetch-user': '?1',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
#     }

#     dominos_all_data_list = []
#     # count = 0
#     request_count = 0 
#     for city in city_data_list:
#         city_name = city["city_name"]
#         city_url = city["city_url"]

#         # if count == 1 :
#         #     break
#         # count += 1

#         try:
#             response = requests.get(city_url, headers=headers, timeout=10)

#             if response.status_code != 200:
#                 print(f"Failed: {city_name} ({response.status_code})")
#                 continue

#             # safe filename
#             # safe_city_name = re.sub(r'[^a-zA-Z0-9_]', '', city_name.replace(" ", "_")).lower()
#             safe_city_name = city_name.replace(" ", "_").lower()

#             file_path = os.path.join(folder_name, f"{safe_city_name}.html.gz")


#             dominos_data = extract_data_from_html(response.text)
#             # dominos_list.append(dominos_data_dict)
#             dominos_all_data_list.extend(dominos_data)
            

#             with open(file_path, "w", encoding="utf-8") as f:
#                 f.write(response.text)

#             print(f"Saved: {file_path}")

#         except Exception as e:
#             print(f"Error for {city_name}: {e}")

#         if request_count >= 100:
#                 product_data_insert(list_data=dominos_all_data_list)
#                 dominos_all_data_list.clear()
#                 request_count = 0
#         request_count += 1
#     if dominos_all_data_list:
#         product_data_insert(list_data=dominos_all_data_list)


#     # print("total dominos : ", dominos_list)
#     # print("total dominos : ", len(dominos_list))
#     return 





