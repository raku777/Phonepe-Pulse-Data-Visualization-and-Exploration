import mysql.connector as sql

def sql_database_table_creation():
    my_db = sql.connect(host= 'localhost', user='root', password = 'raku#123')
    db_name = 'phonepe_pulse' 
    cursor = my_db.cursor()
    cursor.execute('create database if not exists %s' %db_name)
    my_db.database = db_name
    my_db.commit()
    cursor.close()


    cursor = my_db.cursor()
    cursor.execute("create table if not exists aggregated_transaction(\
                            state				varchar(255),\
                            year				int,\
                            quarter				varchar(2),\
                            transaction_type	varchar(255),\
                            transaction_count	int,\
                            transaction_amount	float);\
                   create table if not exists aggregated_user(\
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
                        create table if not exists map_user(\
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
                        create table if not exists top_user_district(\
                            state				varchar(255),\
                            year				int,\
                            quarter				varchar(2),\
                            district			varchar(255),\
                            registered_users		int);\
                        create table if not exists top_user_pincode(\
                            state				varchar(255),\
                            year				int,\
                            quarter				varchar(2),\
                            pincode				varchar(255),\
                            registered_users		int);")
    cursor.close()
    my_db.close()
