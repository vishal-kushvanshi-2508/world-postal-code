

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

    cunt_count = 0 
    ## operation perfome one by one country data after fetch data form data base
    for dict_data in country_data_list:
        cunt_count += 1 
        country_id = dict_data.get("id")
        country_name = dict_data.get("country_name")
        country_url = dict_data.get("country_url")
        status = dict_data.get("status")
        print(country_id, country_name, country_url, status)

        
        folder_path = os.path.join(folder_path, (country_name+"/") )
        print(folder_path)
        

        os.makedirs(folder_path, exist_ok=True)

        response = requests.get(
                    country_url,
                    headers=headers
                )
        

        file_path =  os.path.join(folder_path, f"{country_name}.html.gz")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        tree_country = html.fromstring(response.text)

        # region_or_postal = tree_country.xpath("//div[@class='content short']//div[@class='warn']//b/text()")
        # country_code_name = tree_country.xpath("//div[@class='content short']//div[@class='warn']//b/text()")

        # print("region_or_postal : ",region_or_postal)
        # print(type(region_or_postal))
        # print(country_url)
        # print(country_url.strip("/").split("/")[-1].strip().replace("-", " ").title() + " does not use zip or postal codes")
        not_postal_massage = country_url.strip("/").split("/")[-1].strip().replace("-", " ").title() + " does not use zip or postal codes"
        if not_postal_massage in tree_country.xpath("//div[@class='content short']//div[@class='warn']//b/text()"):
            # this xpath retun does not exist postal. 
            # if xpath not exist in html content then retun empty list = [] then this condition not execute.

            ## not_postal_massage 
            # print("not value exitst")

        # if country_code_name and country_code_name.strip() == "Post Codes":
            # if not postal code
            # print("skip this url and not postal code exist ")
            folder_path = folder_path.replace( (country_name+"/") , "")
            # print("enter folder name ")
            print(folder_path)
            # return None

            ## updata table detail country_detail here
            update_country_url_status(country_id)

            continue

        region_or_code_list = tree_country.xpath("//div[@class='content short']//h2/text()")
        # country_code_name = tree_country.xpath("//div[@class='content short']//div[@class='warn']//b/text()")

        # print("now region is : ", region_or_code_list)
        # print(type(region_or_code_list))

        # if country_code_name and country_code_name.strip().split(":")[0] == "Zip Codes": 
        #     ## if region 
        #     region_or_code = tree_country.xpath("string(.//div[@class='content short']//h2/text())")
        #     print("ragion : ", region_or_code)
            
        if 'Regions' in region_or_code_list:
            # print("enter region ")
            region_url_list = []

            region_urls = tree_country.xpath("(//div[@class='regions'])[1]//a//@href")      
            # print(region_urls)
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
            # print("region_data_list : ", len(region_data_list))

            ## operation perfome one by one region data after fetch data form data base
            # print("\n\nregion data after fetch")
            for dict_data in region_data_list:
                # count += 1 
                region_id = dict_data.get("id")
                country_name = dict_data.get("country_name")
                region_name = dict_data.get("region_name")
                region_url = dict_data.get("region_url")
                status = dict_data.get("status")
                # print(region_id, country_name, region_name, region_url, status)


                folder_path = os.path.join(folder_path, (region_name+"/") )
                print(folder_path)
                

                os.makedirs(folder_path, exist_ok=True)

                response = requests.get(
                            region_url,
                            headers=headers
                        )
                

                file_path =  os.path.join(folder_path, f"{region_name}.html.gz")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(response.text)

                tree_region = html.fromstring(response.text)

                # country_code_name = tree_region.xpath("string(.//div[@class='content short']//h1/text())")

                # print(country_code_name)
                # print(type(country_code_name))

                
                not_postal_massage = region_url.strip("/").split("/")[-1].strip().replace("-", " ").title() + " does not use zip or postal codes"
                if not_postal_massage in tree_region.xpath("//div[@class='content short']//div[@class='warn']//b/text()"):

                # if country_code_name and country_code_name.strip() == "Post Codes":
                    # if not postal code
                    # print("skip this url and not postal code exist ")
                    # folder_path = folder_path.replace( (region_name+"/"), "")
                    # print(folder_path)
                    # return None

                    ## updata table detail region_detail here
                    update_region_status(region_id)

                    continue


                # if country_code_name and country_code_name.strip().split(":")[0] == "Zip Codes": 
                #     ## if region 
                #     region_or_code = tree_region.xpath("//div[@class='content short']//h2/text()")[0].strip()
                #     print("ragion : ", region_or_code)
                    
                area_or_code_list = tree_region.xpath("//div[@class='content short']//h2/text()")
                # country_code_name = tree_country.xpath("//div[@class='content short']//div[@class='warn']//b/text()")

                # print("now region is : ", area_or_code_list)
                # print(type(area_or_code_list))


                ### check only this part after lunch .... this is remain for chaking ..
                if 'Regions' in area_or_code_list:
                #     # print("enter region ")
                #     region_url_list = []

                # # # this is right but chaching comement
                # if region_or_code == "Regions":
                    # print("enter region ")
                    area_url_list = []

                    region_urls = tree_region.xpath("(//div[@class='regions'])[1]//a/@href")   
                        
                    # print("url : ", region_urls)
                    for url in region_urls:
                        # print(url)
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

                    # print(len(area_url_list))

                    area_data_insert(list_data=area_url_list)
                    
                    # featch one by one area data
                    area_data_list = fetch_area_table_data()
                    # print(area_data_list)
                    # print(len(area_data_list))


                    ## operation perfome one by one area data after fetch data form data base
                    # print("\n\narea data after fetch")
                    count_postal = 0
                    # c_val = 0
                    for dict_data in area_data_list:
                        # c_val += 1
                        # count += 1 
                        area_id = dict_data.get("id")
                        country_name = dict_data.get("country_name")
                        region_name = dict_data.get("region_name")
                        area_name = dict_data.get("area_name")
                        area_url = dict_data.get("area_url")
                        status = dict_data.get("status")
                        # print(area_id, country_name, region_name, area_name, area_url, status)

                        folder_path = os.path.join(folder_path, (area_name+"/"))
                        # print(folder_path)
                        

                        os.makedirs(folder_path, exist_ok=True)

                        response = requests.get(
                                    area_url,
                                    headers=headers
                                )
                        

                        file_path =  os.path.join(folder_path, f"{area_name}.html.gz")
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(response.text)

                        tree_area = html.fromstring(response.text)

                        # country_code_name = tree_area.xpath("string(.//div[@class='content short']//h2/text())")
                        sub_area_code_list = tree_area.xpath("//div[@class='content short']//h2/text()")


                        # print(country_code_name)
                        # print(type(country_code_name))
                        if 'Codes List' in sub_area_code_list :


                        # if country_code_name and country_code_name.strip() == "Codes List":
                        #     # if not Codes List
                            # print("this is codes list and insert data into database.")
                            code_list = tree_area.xpath("//div[@class='units noletters']//div[@class='container']")

                            if not code_list:
                                # if code_list is not in first xpath then choose another xpath.
                                code_list = tree_country.xpath("//div[@class='container']")

                            # print(code_list)
                            # print(area_url)
                            # a = area_url.split("/")[-1]
                            # print(a)
                            # print("are name : ", area_name)
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

                        folder_path = folder_path.replace( (area_name+"/") , "")
                        print(folder_path)


                        
                        ## updata table detail area_detail here
                        update_area_status(area_id)
                        
                        # if c_val == 2 :
                        # break
                    # print("total area inside postal code : ", count_postal )


                # region_or_code = tree_region.xpath("//div[@class='content short']//h2/text()")
                region_postal_name = region_name.replace("-", " ").title() + " " + "Codes"


                ## if region_or_code = Alberta Codes
                # print("haaa resion is : ", area_or_code_list)
                # print("haaa resion is : ", region_postal_name)
                # print(region_url)

                if region_postal_name in area_or_code_list or 'Codes List' in area_or_code_list :
                    # print("inside of region postal ...")

                    code_list = tree_region.xpath("//div[@class='units noletters']//div[@class='container']")

                    if not code_list:
                        # if code_list is not in first xpath then choose another xpath.
                        code_list = tree_region.xpath("//div[@class='container']")

                    postal_code_list = []
                    # print("code+ list : ", code_list)
                    for postal_data in code_list:
                        
                        sub_area_name = postal_data.xpath("string(.//div[@class='place']/text())")
                        # print("sub area ; ", sub_area_name)
                        if not sub_area_name:
                            sub_area_name = postal_data.xpath("string(.//div[@class='place red']/text())")
                        sub_area_name = sub_area_name.lower().replace(" ", "-")

                        postal_code = postal_data.xpath(".//div[@class='code']//span/text()")
                        if len(postal_code) == 1:
                            postal_code = postal_code[0]


                        postal_code_list.append( {
                            "country_name" : country_name,
                            "region_name" : region_name,
                            "area_name" : sub_area_name,
                            "area_url" : region_url,
                            "postal_code" : json.dumps(postal_code)   # convert list → JSON string
                        })
                    # print(postal_code_list)
                    postal_data_insert(list_data=postal_code_list)

                folder_path = folder_path.replace( (region_name+"/"), "")

                ## updata table detail region_detail here
                update_region_status(region_id)
                
                # folder_path = os.path.join(folder_path, region_name)
                # print(folder_path)





                # break


        if 'Codes List' in region_or_code_list: 
            ## https://worldpostalcode.com/dominican-republic/
            ## https://worldpostalcode.com/greenland/
            ## if country_code_name = Codes List

            # print("enter in donimal postal code only ")

            code_list = tree_country.xpath("//div[@class='units noletters']//div[@class='container']")
            
            if not code_list:
                # if code_list is not in first xpath then choose another xpath.
                code_list = tree_country.xpath("//div[@class='container']")

            postal_code_list = []

            for postal_data in code_list:
                
                sub_area_name = postal_data.xpath("string(.//div[@class='place']/text())")

                if not sub_area_name:
                    sub_area_name = postal_data.xpath("string(.//div[@class='place red']/text())")
                sub_area_name = sub_area_name.lower().replace(" ", "-")

                postal_code = postal_data.xpath(".//div[@class='code']//span/text()")
                if len(postal_code) == 1:
                    # if only one postal code then that single element.
                    postal_code = postal_code[0]


                postal_code_list.append( {
                    "country_name" : country_name,
                    "region_name" : sub_area_name,
                    "area_name" : None,
                    "area_url" : country_url,
                    "postal_code" : json.dumps(postal_code)   # convert list → JSON string
                })

            postal_data_insert(list_data=postal_code_list)

            print(folder_path)

            # pass
        # folder_path = os.path.join(folder_path, country_name)

        folder_path = folder_path.replace( (country_name+"/"), "")

        ## updata table detail country_detail here

        update_country_url_status(country_id)
        
        



        # if cunt_count == 3:
        #     break
    print("count total : ", cunt_count)
    print(folder_path)











































# from lxml import html
# import requests
# import os
# from store_data_database import *
# import json

# # get html content using url

# def generate_url(base_url):

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

#     response = requests.get(
#                 base_url,
#                 headers=headers
#             )
    
#     folder_path = "D:/vishal_kushvanshi/world_postal_code/"

#     file_path =  os.path.join(folder_path, "world.html.gz")
#     with open(file_path, "w", encoding="utf-8") as f:
#         f.write(response.text)

#     tree = html.fromstring(response.text)

#     country_end_url = tree.xpath("//div[@class='content long']//div[@class='regions']//a/@href")

#     country_url_list = []
#     for page in country_end_url:

#         country_url_list.append( {
#             "country_name" : page.replace("/", "").strip(),
#             "country_url" : base_url + f"{page}",
#             "status" : "pending"
#         })
#     return country_url_list



# def fetch_region_data(country_data_list, base_url):

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

#     folder_path = "D:/vishal_kushvanshi/world_postal_code/"

#     count = 0 
#     ## operation perfome one by one country data after fetch data form data base
#     for dict_data in country_data_list:
#         count += 1 
#         country_id = dict_data.get("id")
#         country_name = dict_data.get("country_name")
#         country_url = dict_data.get("country_url")
#         status = dict_data.get("status")
#         print(country_id, country_name, country_url, status)

        
#         folder_path = os.path.join(folder_path, (country_name+"/") )
#         print(folder_path)
        

#         os.makedirs(folder_path, exist_ok=True)

#         response = requests.get(
#                     country_url,
#                     headers=headers
#                 )
        

#         file_path =  os.path.join(folder_path, f"{country_name}.html.gz")
#         with open(file_path, "w", encoding="utf-8") as f:
#             f.write(response.text)

#         tree_country = html.fromstring(response.text)

#         # region_or_postal = tree_country.xpath("//div[@class='content short']//h2/text()")
#         # country_code_name = tree_country.xpath("//div[@class='content short']//div[@class='warn']//b/text()")

#         # print(region_or_postal)
#         # print(type(region_or_postal))
#         print(country_url)
#         print(country_url.strip("/").split("/")[-1].strip().replace("-", " ").title() + " does not use zip or postal codes")
#         not_postal_massage = country_url.strip("/").split("/")[-1].strip().replace("-", " ").title() + " does not use zip or postal codes"
#         if not_postal_massage in tree_country.xpath("//div[@class='content short']//div[@class='warn']//b/text()"):
#             ## not_postal_massage 
#             # print("not value exitst")

#         # if country_code_name and country_code_name.strip() == "Post Codes":
#             # if not postal code
#             print("skip this url and not postal code exist ")
#             folder_path = folder_path.replace( (country_name+"/") , "")
#             print("enter folder name ")
#             print(folder_path)
#             # return None
#             continue

#         region_or_code_list = tree_country.xpath("//div[@class='content short']//h2/text()")
#         # country_code_name = tree_country.xpath("//div[@class='content short']//div[@class='warn']//b/text()")

#         print("now region is : ", region_or_code_list)
#         print(type(region_or_code_list))

#         # if country_code_name and country_code_name.strip().split(":")[0] == "Zip Codes": 
#         #     ## if region 
#         #     region_or_code = tree_country.xpath("string(.//div[@class='content short']//h2/text())")
#         #     print("ragion : ", region_or_code)
            
#         if 'Regions' in region_or_code_list:
#             # print("enter region ")
#             region_url_list = []

#             region_urls = tree_country.xpath("(//div[@class='regions'])[1]//a//@href")      
#             # print(region_urls)
#             for url in region_urls:

#                 region_url_list.append( {
#                     "country_name" : url.strip("/").split("/")[0],
#                     "region_name" : url.strip("/").split("/")[1],
#                     "region_url" : base_url + f"{url}",
#                     "status" : "pending"
#                 })

#             #store data in databse ..
#             region_data_insert(list_data=region_url_list)

#             # featch one by one region data
#             region_data_list = fetch_region_table_data()
#             print("region_data_list : ", region_data_list)

#             ## operation perfome one by one region data after fetch data form data base
#             # print("\n\nregion data after fetch")
#             for dict_data in region_data_list:
#                 count += 1 
#                 region_id = dict_data.get("id")
#                 country_name = dict_data.get("country_name")
#                 region_name = dict_data.get("region_name")
#                 region_url = dict_data.get("region_url")
#                 status = dict_data.get("status")
#                 print(region_id, country_name, region_name, region_url, status)


#                 folder_path = os.path.join(folder_path, (region_name+"/") )
#                 print(folder_path)
                

#                 os.makedirs(folder_path, exist_ok=True)

#                 response = requests.get(
#                             region_url,
#                             headers=headers
#                         )
                

#                 file_path =  os.path.join(folder_path, f"{region_name}.html.gz")
#                 with open(file_path, "w", encoding="utf-8") as f:
#                     f.write(response.text)

#                 tree_region = html.fromstring(response.text)

#                 country_code_name = tree_region.xpath("string(.//div[@class='content short']//h1/text())")

#                 # print(country_code_name)
#                 # print(type(country_code_name))

                

#                 if country_code_name and country_code_name.strip() == "Post Codes":
#                     # if not postal code
#                     print("skip this url and not postal code exist ")
#                     folder_path = folder_path.replace( (region_name+"/"), "")
#                     print(folder_path)
#                     # return None
#                     continue
#                 if country_code_name and country_code_name.strip().split(":")[0] == "Zip Codes": 
#                     ## if region 
#                     region_or_code = tree_region.xpath("//div[@class='content short']//h2/text()")[0].strip()
#                     print("ragion : ", region_or_code)
                    

#                     # # this is right but chaching comement
#                     if region_or_code == "Regions":
#                         # print("enter region ")
#                         area_url_list = []

#                         region_urls = tree_region.xpath("(//div[@class='regions'])[1]//a/@href")   
                            
#                         # print("url : ", region_urls)
#                         for url in region_urls:
#                             # print(url)
#                             area_url_list.append( {
#                                 "country_name" : url.strip("/").split("/")[0],
#                                 "region_name" : url.strip("/").split("/")[1],
#                                 "area_name" : url.strip("/").split("/")[2],
#                                 "area_url" : base_url + f"{url}",
#                                 "status" : "pending"
#                             })
#                             # print(region_url_list)
#                             # break

#                         #store data in databse ..
#                         # print(region_url_list)

#                         print(len(area_url_list))

#                         area_data_insert(list_data=area_url_list)
                        
#                         # featch one by one area data
#                         area_data_list = fetch_area_table_data()
#                         # print(area_data_list)
#                         print(len(area_data_list))


#                         ## operation perfome one by one area data after fetch data form data base
#                         # print("\n\narea data after fetch")
#                         count_postal = 0
#                         # c_val = 0
#                         for dict_data in area_data_list:
#                             # c_val += 1
#                             count += 1 
#                             region_id = dict_data.get("id")
#                             country_name = dict_data.get("country_name")
#                             region_name = dict_data.get("region_name")
#                             area_name = dict_data.get("area_name")
#                             area_url = dict_data.get("area_url")
#                             status = dict_data.get("status")
#                             print(region_id, country_name, region_name, area_name, area_url, status)

#                             folder_path = os.path.join(folder_path, (area_name+"/"))
#                             print(folder_path)
                            

#                             os.makedirs(folder_path, exist_ok=True)

#                             response = requests.get(
#                                         area_url,
#                                         headers=headers
#                                     )
                            

#                             file_path =  os.path.join(folder_path, f"{area_name}.html.gz")
#                             with open(file_path, "w", encoding="utf-8") as f:
#                                 f.write(response.text)

#                             tree_area = html.fromstring(response.text)

#                             country_code_name = tree_area.xpath("string(.//div[@class='content short']//h2/text())")

#                             # print(country_code_name)
#                             # print(type(country_code_name))

#                             if country_code_name and country_code_name.strip() == "Codes List":
#                             #     # if not Codes List
#                                 print("this is codes list and insert data into database.")
#                                 code_list = tree_area.xpath("//div[@class='units noletters']//div[@class='container']")
#                                 # print(code_list)
#                                 # print(area_url)
#                                 # a = area_url.split("/")[-1]
#                                 # print(a)
#                                 print("are name : ", area_name)
#                                 postal_code_list = []
#                                 for postal_data in code_list:
                                    
#                                     sub_area_name = postal_data.xpath("string(.//div[@class='place']/text())")
#                                     # print(sub_area_name)
#                                     if not sub_area_name:
#                                         sub_area_name = postal_data.xpath("string(.//div[@class='place red']/text())")
#                                     sub_area_name = sub_area_name.lower().replace(" ", "-")

#                                     postal_code = postal_data.xpath(".//div[@class='code']//span/text()")
#                                     if len(postal_code) == 1:
#                                         postal_code = postal_code[0]


#                                     postal_code_list.append( {
#                                         "country_name" : country_name,
#                                         "region_name" : region_name,
#                                         "area_name" : area_name + "/" + sub_area_name,
#                                         "area_url" : area_url,
#                                         "postal_code" : json.dumps(postal_code)   # convert list → JSON string
#                                     })
#                                 # print(postal_code_list)
#                                 count_postal += len(postal_code_list)
#                                 postal_data_insert(list_data=postal_code_list)

#                                 folder_path = folder_path.replace( (area_name+"/") , "")
#                                 print(folder_path)

#                             # if c_val == 2 :
#                             break
#                         print("total area inside postal code : ", count_postal )


#                 region_or_code = tree_region.xpath("//div[@class='content short']//h2/text()")
#                 region_postal_name = region_name.replace("-", " ").title() + " " + "Codes"


#                 ## if region_or_code = Alberta Codes
#                 print("haaa resion is : ", region_or_code)
#                 print("haaa resion is : ", region_postal_name)
#                 print(region_url)

#                 if region_postal_name in region_or_code or 'Codes List' in region_or_code :
#                     print("inside of region postal ...")

#                     code_list = tree_region.xpath("//div[@class='units noletters']//div[@class='container']")

#                     postal_code_list = []
#                     # print("code+ list : ", code_list)
#                     for postal_data in code_list:
                        
#                         sub_area_name = postal_data.xpath("string(.//div[@class='place']/text())")
#                         # print("sub area ; ", sub_area_name)
#                         if not sub_area_name:
#                             sub_area_name = postal_data.xpath("string(.//div[@class='place red']/text())")
#                         sub_area_name = sub_area_name.lower().replace(" ", "-")

#                         postal_code = postal_data.xpath(".//div[@class='code']//span/text()")
#                         if len(postal_code) == 1:
#                             postal_code = postal_code[0]


#                         postal_code_list.append( {
#                             "country_name" : country_name,
#                             "region_name" : region_name,
#                             "area_name" : sub_area_name,
#                             "area_url" : region_url,
#                             "postal_code" : json.dumps(postal_code)   # convert list → JSON string
#                         })
#                     # print(postal_code_list)
#                     postal_data_insert(list_data=postal_code_list)

#                 folder_path = folder_path.replace( (region_name+"/"), "")
                
#                 # folder_path = os.path.join(folder_path, region_name)
#                 print(folder_path)





#                 break


#         if 'Codes List' in region_or_code_list: 
#             ## https://worldpostalcode.com/dominican-republic/
#             ## https://worldpostalcode.com/greenland/
#             ## if country_code_name = Codes List

#             print("enter in donimal postal code only ")
#             # region_or_code = tree_country.xpath("//div[@class='content short']//h2/text()")
            
#             # region_postal_name = region_name.replace("-", " ").title() + " " + "Codes"
#             # # print("now 1 : ", region_or_code)
#             # # print("now 2 : ", region_postal_name)
#             # # print(region_url)

#             # ## if region_or_code = Alberta Codes
#             # print("haaa resion is : ", region_or_code)
#             # print("haaa resion is : ", region_postal_name)
#             # print(region_url)

#             # if region_postal_name in region_or_code or 'Codes List' in region_or_code :

#             # print("inside of region postal ...")

#             code_list = tree_country.xpath("//div[@class='units noletters']//div[@class='container']")
            
#             if not code_list:
#                 code_list = tree_country.xpath("//div[@class='container']")

#             postal_code_list = []
#             # print("code+ list : ", code_list)
#             # print("code+ list : ", len(code_list))
#             for postal_data in code_list:
                
#                 sub_area_name = postal_data.xpath("string(.//div[@class='place']/text())")
#                 # print("sub area ; ", sub_area_name)
#                 if not sub_area_name:
#                     sub_area_name = postal_data.xpath("string(.//div[@class='place red']/text())")
#                 sub_area_name = sub_area_name.lower().replace(" ", "-")

#                 postal_code = postal_data.xpath(".//div[@class='code']//span/text()")
#                 if len(postal_code) == 1:
#                     postal_code = postal_code[0]


#                 postal_code_list.append( {
#                     "country_name" : country_name,
#                     "region_name" : sub_area_name,
#                     "area_name" : None,
#                     "area_url" : country_url,
#                     "postal_code" : json.dumps(postal_code)   # convert list → JSON string
#                 })

#             postal_data_insert(list_data=postal_code_list)

#             print(folder_path)

#             # pass
#         # folder_path = os.path.join(folder_path, country_name)
#         folder_path = folder_path.replace( (country_name+"/"), "")
        
        




#         break
#     # print(region_url_list)
#     print("count total : ", count)
