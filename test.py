# import requests
# from lxml import html

# base_url = "https://worldpostalcode.com"

# headers = {
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

# # response = requests.get(
# #             base_url,
# #             headers=headers
# #         )

# # with open("html_content.html", "w", encoding="utf-8") as f:
# #             f.write(response.text)


# ## gz file of country..
# # with open("country.html.gz", "w", encoding="utf-8") as f:
# #             f.write(response.text)

# print("process start ...")
# with open("html_content.html", "r", encoding="utf-8") as f:
#     # f.write(response.text)
#     data = f.read()
#     # print(data)
#     tree = html.fromstring(data)
#     url_list = tree.xpath("//div[@class='content long']//div[@class='regions']//div//a/@href")
    
#     # last_page_number = int(last_page_url.split("page=")[1])
#     # print(url_list)
#     print(len(url_list), "\n\n")
#     quotes_url_list = []
#     for url in url_list:
#             quotes_url_list.append( {
#                 "country_link" : base_url + f"{url}",
#                 "status" : "pending"
#             })
#             # break
#     print(quotes_url_list)


#     first_url = quotes_url_list[0].get("country_link")            ## india 
#     print("first_url : ",first_url)  #  https://worldpostalcode.com/bahamas/
#     # response = requests.get(
#     #         first_url,
#     #         headers=headers
#     #     )
#     ## check if html content avalabel in ragion then 
#     #  

#     country_name  = first_url.replace(base_url, "").replace("/", "").strip()
#     print(country_name)
    


    

    









import requests
from lxml import html
import os

def country_data(country_url, folder_path, base_url ):
    # country_url = dict_data.get("country_url")
    print(country_url)

    # region = country_url.strip("/").split("/")[-1]
    # print(region)
    country_region_name = country_url.strip("/").split("/")[-1]
    print(country_region_name)

    folder_path = os.path.join(folder_path, country_region_name)
    os.makedirs(folder_path, exist_ok=True)

    print(folder_path)
    response = requests.get(
                    country_url,
                    headers=headers
                )

    file_path =  os.path.join(folder_path, f"{country_region_name}.html.gz")
    # file_path = "/home/vishal/Development/CompanyProject/Actowiz/world_postal_code/world_D_drive_folder/country.html.gz"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    tree = html.fromstring(response.text)

    country_code_name = tree.xpath("string(.//div[@class='content short']//h1/text())")

    print(country_code_name)
    print(type(country_code_name))

    if country_code_name and country_code_name.strip() == "Post Codes":
        print("skip this url and not postal code exist ")
        return None


    elif country_code_name and country_code_name.strip().split(":")[0] == "Zip Codes": 
        region_or_code = tree.xpath("string(.//div[@class='content short']//h2/text())")
        print("ragion : ", region_or_code)
        region_end_url_list = tree.xpath("//div[@class='regions']//a/@href")
        print(region_end_url_list)
        for end_url in region_end_url_list:
            region_url = base_url + end_url
            print(region_url)
            country_data(region_url, folder_path, base_url)
            break
        # pass



def country_operation(country_url_list, folder_path, base_url):
    ## here is loop... 

    ## get first url and send request....
    count = 0 
    for dict_data in country_url_list:
        country_url = dict_data.get("country_url")

        if count == 3:
            break

        print("\n\nnew data")
        country_data(country_url, folder_path, base_url)

        count += 1





base_url = "https://worldpostalcode.com"

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

print("start :: ")

response = requests.get(
                base_url,
                headers=headers
            )

folder_path = "D:/vishal_kushvanshi/world_postal_code/"
file_path =  os.path.join(folder_path, "world.html.gz")
# file_path = "/home/vishal/Development/CompanyProject/Actowiz/world_postal_code/world_D_drive_folder/country.html.gz"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(response.text)


tree = html.fromstring(response.text)

country_end_url = tree.xpath("//div[@class='content long']//div[@class='regions']//a/@href")
# print(country_end_url)

country_url_list = []

for page in country_end_url:
    country_url_list.append( {
            "country_url" : base_url + f"{page}",
            "status" : "pending"
    })
        
# print("\n\ndata : ", country_url_list)
print("data : ", len(country_url_list))

country_operation(country_url_list, folder_path, base_url)

