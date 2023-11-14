import mysql.connector as sql
from data_extraction import *

def sql_database_table_creation():
    my_db = sql.connect(host= 'localhost', user='root', password = 'raku#123')
    db_name = 'phonepe_pulse' 
    cursor = my_db.cursor()
    cursor.execute('create database if not exists %s' %db_name)
    my_db.database = db_name
    my_db.commit()
    cursor.close()


    cursor = my_db.cursor()
    cursor.execute('create table if not exists aggregate_transaction(\
                            state				varchar(255),\
                            year				int,\
                            quarter				varchar(2),\
                            transaction_type	varchar(255),\
                            transaction_count	int,\
                            transaction_amount	float);\
                   create table if not exists aggregate_users(\
                            state				varchar(255),\
                            year				int,\
                            quarter				varchar(2),\
                            user_brand			varchar(255),\
                            user_count			int,\
                            user_percentage		float);\
                        create table if not exists map_transaction(\
                            state				varchar(255),\
                            year				int,\
                            quarter				varchar(2),\
                            district			varchar(255),\
                            transaction_count	int,\
                            transaction_amount	float);\
                        create table if not exists map_users(\
                            state				varchar(255),\
                            year				int,\
                            quarter				varchar(2),\
                            district			varchar(255),\
                            registered_users		int,\
                            app_opens			int);\
                        create table if not exists top_transaction_district(\
                            state				varchar(255),\
                            year				int,\
                            quarter				varchar(2),\
                            district			varchar(255),\
                            transaction_count	int,\
                            transaction_amount	float);	\
                        create table if not exists top_transaction_pincode(\
                            state				varchar(255),\
                            year				int,\
                            quarter				varchar(2),\
                            pincode				varchar(255),\
                            transaction_count	int,\
                            transaction_amount	float);\
                        create table if not exists top_users_district(\
                            state				varchar(255),\
                            year				int,\
                            quarter				varchar(2),\
                            district			varchar(255),\
                            registered_users		int);\
                        create table if not exists top_users_pincode(\
                            state				varchar(255),\
                            year				int,\
                            quarter				varchar(2),\
                            pincode				varchar(255),\
                            registered_users		int);')
    cursor.close()
    my_db.close()

def data_insertion():
    my_db = sql.connect(host= 'localhost', user='root', password = 'raku#123',database = 'phonepe_pulse')
    cursor = my_db.cursor()
    try:
        cursor.execute('DELETE FROM aggregate_transaction')
        cursor.execute('DELETE FROM aggregate_users')
        cursor.execute('DELETE FROM map_transaction')
        cursor.execute('DELETE FROM map_users')
        cursor.execute('DELETE FROM top_transaction_district')
        cursor.execute('DELETE FROM top_transaction_pincode')
        cursor.execute('DELETE FROM top_users_district')
        cursor.execute('DELETE FROM top_users_pincode')

        
        my_db.commit()
    except sql.Error as err:
        print(f"Error: {err}")

    cursor.executemany('insert into aggregate_transaction(\
                       state, year, quarter, transaction_type, transaction_count, transaction_amount)\
                       values(%s,%s,%s,%s,%s,%s)', aggregate_transaction().values.tolist())
    cursor.executemany('insert into aggregate_users(\
                       state, year, quarter, user_brand, user_count, user_percentage)\
                       values(%s,%s,%s,%s,%s,%s)', aggregate_users().values.tolist())
    cursor.executemany('insert into map_transaction(\
                       state, year, quarter, district, transaction_count, transaction_amount)\
                       values(%s,%s,%s,%s,%s,%s)',map_transaction().values.tolist())
    cursor.executemany('insert into map_users(\
                       state, year, quarter, district, registered_users, app_opens)\
                       values(%s,%s,%s,%s,%s,%s)',map_users().values.tolist())
    cursor.executemany('insert into top_transaction_district(\
                       state, year, quarter, district, transaction_count, transaction_amount)\
                       values(%s,%s,%s,%s,%s,%s)', top_transaction_district().values.tolist())   
    cursor.executemany('insert into top_transaction_pincode(\
                       state, year, quarter, pincode, transaction_count, transaction_amount)\
                       values(%s,%s,%s,%s,%s,%s)', top_transaction_pincode().values.tolist())
    cursor.executemany('insert into top_users_district(\
                       state, year, quarter, district, registered_users)\
                       values(%s,%s,%s,%s,%s)', top_users_district().values.tolist())
    cursor.executemany('insert into top_users_pincode(\
                       state, year, quarter, pincode, registered_users)\
                       values(%s,%s,%s,%s,%s)', top_users_pincode().values.tolist())        

    cursor.close()
    my_db.commit()
    my_db.close()   
    



