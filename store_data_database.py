

from typing import List, Tuple

import mysql.connector # Must include .connector


country_url_table_name = "country_url_detail"


DB_CONFIG = {
    "host" : "localhost",
    "user" : "root",
    "password" : "actowiz",
    "port" : "3306",
    "database" : "world_postal_code_db"
}

def get_connection():
    try:
        ## here ** is unpacking DB_CONFIG dictionary.
        connection = mysql.connector.connect(**DB_CONFIG)
        ## it is protect to autocommit
        connection.autocommit = False
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

def create_db():
    connection = get_connection()
    # connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS world_postal_code_db;")
    connection.commit()
    connection.close()
# create_db()


def create_table_country_url():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query =  f"""
                CREATE TABLE IF NOT EXISTS {country_url_table_name}(
                id INT AUTO_INCREMENT PRIMARY KEY,
                country_name VARCHAR(100),
                country_url TEXT,
                status VARCHAR(100),
                country_error TEXT
        ); """
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Table creation failed")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


batch_size_length = 100
def data_commit_batches_wise(connection, cursor, sql_query : str, sql_query_value: List[Tuple], batch_size: int = batch_size_length ):
    ## this is save data in database batches wise.
    batch_count = 0
    for index in range(0, len(sql_query_value), batch_size):
        batch = sql_query_value[index: index + batch_size]
        cursor.executemany(sql_query, batch)
        batch_count += 1
        connection.commit()
    return batch_count


def country_url_insert(list_data : list):
    connection = get_connection()
    cursor = connection.cursor()
    if not list_data:
        return
    dict_data = list_data[0]
    columns = ", ".join(list(dict_data.keys()))
    values = "".join([len(dict_data.keys()) * '%s,']).strip(',')
    parent_sql = f"""INSERT INTO {country_url_table_name} ({columns}) VALUES ({values})"""
    try:

        cursor.execute(f"SELECT COUNT(*) FROM {country_url_table_name}")
        total_contry_rows = cursor.fetchone()[0]
        if total_contry_rows == 0:

            product_values = []
            for dict_data in list_data:
                product_values.append( (
                    dict_data.get("country_name") ,
                    dict_data.get("country_url"), 
                    dict_data.get("status"),
                    dict_data.get("country_error")

                ))

            try:
                batch_count = data_commit_batches_wise(connection, cursor, parent_sql, product_values)
                # print(f"Parent batches executed count={batch_count}")
            except Exception as e:
                print(f"batch can not. Error : {e} ")
        else:
            print(f"not {country_url_table_name} table in data inserted ..")

        cursor.close()
        connection.close()

    except Exception as e:
        ## this exception execute when error occur in try block and rollback until last save on database .
        connection.rollback()
        # print(f"Transaction failed, rolled back. Error: {e}")
        print("Transaction failed. Rolling back")
    except:
        print("except error raise ")
    finally:
        connection.close()


def fetch_country_table_data():
    connection = get_connection()
    cursor = connection.cursor()
    query = f"SELECT id, country_name, country_url, status FROM {country_url_table_name} WHERE status = 'pending' and country_error = '' ;"
    # query = f"SELECT id, country_name, country_url, status FROM {country_url_table_name} WHERE status = 'pending' and country_error = '' and country_name = 'united-states';"
    # query = f"SELECT id, country_name, country_url, status FROM {country_url_table_name} WHERE country_name = 'dominican-republic';"
    # query = f"SELECT id, country_name, country_url, status FROM {country_url_table_name} WHERE country_name = 'bahamas';"
    # query = f"SELECT id, country_name, country_url, status FROM {country_url_table_name} WHERE country_name = 'barbados' and status = 'pending';"
    # query = f"SELECT id, country_name, country_url, status FROM {country_url_table_name} WHERE (country_name = 'canada' or country_name = 'barbados')  and status = 'pending';"
    
    cursor.execute(query)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        data = {
            "id": row[0],
            "country_name": row[1],
            "country_url": row[2],
            "status": row[3]
        }
        result.append(data)

    cursor.close()
    connection.close()
    return result


### update country url status ..

def update_country_url_status(country_id, status, country_error):
    connection = get_connection()
    cursor = connection.cursor()
    sql_query = f"UPDATE {country_url_table_name} SET status = %s, country_error = %s  WHERE id = %s ;"
    values = (status, country_error, country_id)
    cursor.execute(sql_query, values)
    connection.commit()
    cursor.close()
    connection.close()








### region table code 

region_table_name = "region_detail"


def create_table_region():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query =  f"""
                CREATE TABLE IF NOT EXISTS {region_table_name}(
                id INT AUTO_INCREMENT PRIMARY KEY,
                country_name VARCHAR(100) ,
                region_name VARCHAR(150) ,
                region_url TEXT,
                status VARCHAR(150),
                region_error TEXT
        ); """
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Table creation failed")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()




def region_data_insert(list_data : list):
    connection = get_connection()
    cursor = connection.cursor()
    if not list_data:
        return
    dict_data = list_data[0]
    columns = ", ".join(list(dict_data.keys()))
    values = "".join([len(dict_data.keys()) * '%s,']).strip(',')
    parent_sql = f"""INSERT INTO {region_table_name} ({columns}) VALUES ({values})"""

    try:
        product_values = []
        for dict_data in list_data:
            product_values.append( (
                dict_data.get("country_name"),
                dict_data.get("region_name"),
                dict_data.get("region_url"),
                dict_data.get("status"),
                dict_data.get("region_error")
            ))

        try:
            batch_count = data_commit_batches_wise(connection, cursor, parent_sql, product_values)
            # print(f"Parent batches executed count={batch_count}")
        except Exception as e:
            print(f"batch can not. Error : {e} ")
        cursor.close()
        connection.close()

    except Exception as e:
        ## this exception execute when error occur in try block and rollback until last save on database .
        connection.rollback()
        # print(f"Transaction failed, rolled back. Error: {e}")
        print("Transaction failed. Rolling back")
    except:
        print("except error raise ")
    finally:
        connection.close()


## fetch region data..

def fetch_region_table_data():
    connection = get_connection()
    cursor = connection.cursor()
    query = f"SELECT * FROM {region_table_name} WHERE status = 'pending' and region_error = '' ;" 
    # query = f"SELECT * FROM {region_table_name} WHERE region_name = 'alberta' and status = 'pending';"
    cursor.execute(query)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        data = {
            "id": row[0],
            "country_name": row[1],
            "region_name": row[2],
            "region_url": row[3],
            "status": row[4]
        }
        result.append(data)

    cursor.close()
    connection.close()
    return result


### update country url status ..

def update_region_status(region_id, status, region_error):
    connection = get_connection()
    cursor = connection.cursor()
    sql_query = f"UPDATE {region_table_name} SET status = %s, region_error = %s WHERE id = %s;"
    values = (status, region_error, region_id)
    cursor.execute(sql_query, values)
    connection.commit()
    cursor.close()
    connection.close()







### area table code 

area_table_name = "area_detail"


def create_table_area():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query =  f"""
                CREATE TABLE IF NOT EXISTS {area_table_name}(
                id INT AUTO_INCREMENT PRIMARY KEY,
                country_name VARCHAR(100) ,
                region_name VARCHAR(150) ,
                area_name VARCHAR(150) ,
                area_url TEXT,
                status VARCHAR(150),
                area_error TEXT
        ); """
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Table creation failed")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()




def area_data_insert(list_data : list):
    connection = get_connection()
    cursor = connection.cursor()
    if not list_data:
        return
    dict_data = list_data[0]
    columns = ", ".join(list(dict_data.keys()))
    values = "".join([len(dict_data.keys()) * '%s,']).strip(',')
    parent_sql = f"""INSERT INTO {area_table_name} ({columns}) VALUES ({values})"""
    try:

        product_values = []
        for dict_data in list_data:
            product_values.append( (
                dict_data.get("country_name"),
                dict_data.get("region_name"),
                dict_data.get("area_name"),
                dict_data.get("area_url"),
                dict_data.get("status"),
                dict_data.get("area_error")
            ))

        try:
            batch_count = data_commit_batches_wise(connection, cursor, parent_sql, product_values)
            # print(f"Parent batches executed count={batch_count}")
        except Exception as e:
            print(f"batch can not. Error : {e} ")
        cursor.close()
        connection.close()

    except Exception as e:
        ## this exception execute when error occur in try block and rollback until last save on database .
        connection.rollback()
        # print(f"Transaction failed, rolled back. Error: {e}")
        print("Transaction failed. Rolling back")
    except:
        print("except error raise ")
    finally:
        connection.close()


## fetch region data..

def fetch_area_table_data():
    connection = get_connection()
    cursor = connection.cursor()
    query = f"SELECT * FROM {area_table_name} WHERE status = 'pending' and area_error = '' ;"
    cursor.execute(query)
    rows = cursor.fetchall()

    result = []
    for row in rows:
        data = {
            "id": row[0],
            "country_name": row[1],
            "region_name": row[2],
            "area_name": row[3],
            "area_url": row[4],
            "status": row[5]
        }
        result.append(data)

    cursor.close()
    connection.close()
    return result


### update country url status ..

def update_area_status(area_id, status, area_error):
    connection = get_connection()
    cursor = connection.cursor()
    sql_query = f"UPDATE {area_table_name} SET status = %s, area_error = %s  WHERE id = %s;"
    values = (status, area_error, area_id)
    cursor.execute(sql_query, values)
    connection.commit()
    cursor.close()
    connection.close()








## table of postal code 

postal_table_name = "country_postal_code_detail"


def create_table_postal():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query =  f"""
                CREATE TABLE IF NOT EXISTS {postal_table_name}(
                id INT AUTO_INCREMENT PRIMARY KEY,
                country_name VARCHAR(100) ,
                region_name VARCHAR(150) ,
                area_name VARCHAR(150) ,
                area_url TEXT ,
                postal_code TEXT
        ); """
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        print("Table creation failed")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()




def postal_data_insert(list_data : list):
    connection = get_connection()
    cursor = connection.cursor()
    if not list_data:
        return
    dict_data = list_data[0]
    columns = ", ".join(list(dict_data.keys()))
    values = "".join([len(dict_data.keys()) * '%s,']).strip(',')
    parent_sql = f"""INSERT INTO {postal_table_name} ({columns}) VALUES ({values})"""
    try:
        product_values = []
        for dict_data in list_data:
            product_values.append( (
                dict_data.get("country_name"),
                dict_data.get("region_name"),
                dict_data.get("area_name"),
                dict_data.get("area_url"),
                dict_data.get("postal_code")
            ))

        try:
            batch_count = data_commit_batches_wise(connection, cursor, parent_sql, product_values)
            # print(f"Parent batches executed count={batch_count}")
        except Exception as e:
            print(f"batch can not. Error : {e} ")
        cursor.close()
        connection.close()

    except Exception as e:
        ## this exception execute when error occur in try block and rollback until last save on database .
        connection.rollback()
        # print(f"Transaction failed, rolled back. Error: {e}")
        print("Transaction failed. Rolling back")
    except:
        print("except error raise ")
    finally:
        connection.close()

