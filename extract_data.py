

from lxml import html
import requests
import os
from store_data_database import *
import json

# get html content using url

def generate_url(base_url):

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

    response = requests.get(
                base_url,
                headers=headers
            )
    
    folder_path = "D:/vishal_kushvanshi/world_postal_code/"

    file_path =  os.path.join(folder_path, "world.html.gz")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    tree = html.fromstring(response.text)

    country_end_url = tree.xpath("//div[@class='content long']//div[@class='regions']//a/@href")

    country_url_list = []
    for page in country_end_url:

        country_url_list.append( {
            "country_name" : page.replace("/", "").strip(),
            "country_url" : base_url + f"{page}",
            "status" : "pending"
        })
    return country_url_list



def fetch_region_data(country_data_list, base_url):

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

    folder_path = "D:/vishal_kushvanshi/world_postal_code/"
    count = 0 
    ## operation perfome one by one country data after fetch data form data base
    for dict_data in country_data_list:
        count += 1 
        country_id = dict_data.get("id")
        country_name = dict_data.get("country_name")
        country_url = dict_data.get("country_url")
        status = dict_data.get("status")
        print(country_id, country_name, country_url, status)

        
        folder_path = os.path.join(folder_path, country_name)
        print(folder_path)
        

        os.makedirs(folder_path, exist_ok=True)

        response = requests.get(
                    country_url,
                    headers=headers
                )
        

        file_path =  os.path.join(folder_path, f"{country_name}.html.gz")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        tree = html.fromstring(response.text)

        country_code_name = tree.xpath("string(.//div[@class='content short']//h1/text())")

        print(country_code_name)
        print(type(country_code_name))

        if country_code_name and country_code_name.strip() == "Post Codes":
            # if not postal code
            print("skip this url and not postal code exist ")
            folder_path = folder_path.replace(country_name, "")
            print(folder_path)
            # return None
            continue
        elif country_code_name and country_code_name.strip().split(":")[0] == "Zip Codes": 
            ## if region 
            region_or_code = tree.xpath("string(.//div[@class='content short']//h2/text())")
            print("ragion : ", region_or_code)
            
            if region_or_code == "Regions":
                print("enter region ")
                region_url_list = []

                region_urls = tree.xpath("(//div[@class='regions'])[1]//a//@href")      
                print(region_urls)
                for url in region_urls:

                    region_url_list.append( {
                        "country_name" : url.strip("/").split("/")[0],
                        "region_name" : url.strip("/").split("/")[1],
                        "region_url" : base_url + f"{url}",
                        "status" : "pending"
                    })

                #store data in databse ..
                region_data_insert(list_data=region_url_list)

                # featch one by one region data
                region_data_list = fetch_region_table_data()
                print(region_data_list)

                ## operation perfome one by one region data after fetch data form data base
                print("\n\nregion data after fetch")
                for dict_data in region_data_list:
                    count += 1 
                    region_id = dict_data.get("id")
                    country_name = dict_data.get("country_name")
                    region_name = dict_data.get("region_name")
                    region_url = dict_data.get("region_url")
                    status = dict_data.get("status")
                    print(region_id, country_name, region_name, region_url, status)


                    folder_path = os.path.join(folder_path, region_name)
                    print(folder_path)
                    

                    os.makedirs(folder_path, exist_ok=True)

                    response = requests.get(
                                region_url,
                                headers=headers
                            )
                    

                    file_path =  os.path.join(folder_path, f"{region_name}.html.gz")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(response.text)

                    tree = html.fromstring(response.text)

                    country_code_name = tree.xpath("string(.//div[@class='content short']//h1/text())")

                    print(country_code_name)
                    print(type(country_code_name))

                    if country_code_name and country_code_name.strip() == "Post Codes":
                        # if not postal code
                        print("skip this url and not postal code exist ")
                        folder_path = folder_path.replace(region_name, "")
                        print(folder_path)
                        # return None
                        continue
                    elif country_code_name and country_code_name.strip().split(":")[0] == "Zip Codes": 
                        ## if region 
                        region_or_code = tree.xpath("string(.//div[@class='content short']//h2/text())")
                        print("ragion : ", region_or_code)
                        
                        if region_or_code == "Regions":
                            print("enter region ")
                            area_url_list = []

                            region_urls = tree.xpath("(//div[@class='regions'])[1]//a/@href")   
                               
                            print("url : ", region_urls)
                            for url in region_urls:
                                print(url)
                                area_url_list.append( {
                                    "country_name" : url.strip("/").split("/")[0],
                                    "region_name" : url.strip("/").split("/")[1],
                                    "area_name" : url.strip("/").split("/")[2],
                                    "area_url" : base_url + f"{url}",
                                    "status" : "pending"
                                })
                                # print(region_url_list)
                                # break

                            #store data in databse ..
                            # print(region_url_list)

                            print(len(area_url_list))

                            area_data_insert(list_data=area_url_list)
                            
                            # featch one by one area data
                            area_data_list = fetch_area_table_data()
                            print(area_data_list)
                            print(len(area_data_list))


                            ## operation perfome one by one area data after fetch data form data base
                            print("\n\narea data after fetch")
                            count_postal = 0
                            # c_val = 0
                            for dict_data in area_data_list:
                                # c_val += 1
                                count += 1 
                                region_id = dict_data.get("id")
                                country_name = dict_data.get("country_name")
                                region_name = dict_data.get("region_name")
                                area_name = dict_data.get("area_name")
                                area_url = dict_data.get("area_url")
                                status = dict_data.get("status")
                                print(region_id, country_name, region_name, area_name, area_url, status)

                                folder_path = os.path.join(folder_path, area_name)
                                print(folder_path)
                                

                                os.makedirs(folder_path, exist_ok=True)

                                response = requests.get(
                                            area_url,
                                            headers=headers
                                        )
                                

                                file_path =  os.path.join(folder_path, f"{area_name}.html.gz")
                                with open(file_path, "w", encoding="utf-8") as f:
                                    f.write(response.text)

                                tree = html.fromstring(response.text)

                                country_code_name = tree.xpath("string(.//div[@class='content short']//h2/text())")

                                print(country_code_name)
                                print(type(country_code_name))

                                if country_code_name and country_code_name.strip() == "Codes List":
                                #     # if not Codes List
                                    print("this is codes list and insert data into database.")
                                    code_list = tree.xpath("//div[@class='units noletters']//div[@class='container']")
                                    print(code_list)
                                    # print(area_url)
                                    # a = area_url.split("/")[-1]
                                    # print(a)
                                    print("are name : ", area_name)
                                    postal_code_list = []
                                    for postal_data in code_list:
                                        
                                        sub_area_name = postal_data.xpath("string(.//div[@class='place']/text())")
                                        # print(sub_area_name)
                                        if not sub_area_name:
                                            sub_area_name = postal_data.xpath("string(.//div[@class='place red']/text())")
                                        sub_area_name = sub_area_name.lower().replace(" ", "-")

                                        postal_code = postal_data.xpath(".//div[@class='code']//span/text()")
                                        if len(postal_code) == 1:
                                            postal_code = postal_code[0]


                                        postal_code_list.append( {
                                            "country_name" : country_name,
                                            "region_name" : region_name,
                                            "area_name" : area_name + "/" + sub_area_name,
                                            "area_url" : area_url,
                                            "postal_code" : json.dumps(postal_code)   # convert list → JSON string
                                        })
                                    # print(postal_code_list)
                                    count_postal += len(postal_code_list)
                                    postal_data_insert(list_data=postal_code_list)

                                # if c_val == 2 :
                                #     break
                            print("total area inside postal code : ", count_postal )





                        elif region_or_code == "Alberta Codes":
                            ## insert data in data base
                            pass



                    break





        break
    # print(region_url_list)
    print("count total : ", count)
