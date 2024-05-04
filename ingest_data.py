#!/usr/bin/env python
# coding: utf-8

import os
import argparse
from time import time
from sqlalchemy import create_engine
import pandas as pd

def main(params):
    #assign all the parameters
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv.gz'
    
    #download the csv
    os.system("wget {} -O {}".format(url, csv_name))
    
    #create an engine connection to postgres
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db))

    #read the csv in chunks of 100000, and decrompress the csv.gz file
    df_iter = pd.read_csv(csv_name, compression='gzip', low_memory=False, iterator=True, chunksize=100000)
    
    #get the first 100000 chunks of data
    df = next(df_iter)
    
    #change the data type of these columns from string to datetime
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    #create the database with the column names only
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    
    #add the first chunk of data to the database
    df.to_sql(name=table_name, con=engine, if_exists='append')

    #repeat this until there is no more data to get
    while True:
        t_start = time()
        
        try:
            df = next(df_iter)
        except StopIteration:
            #exit loop without error popping up once all chunks are processed
            print('All chunks are processed, upload commplete...')
            break
        
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
        
        df.to_sql(name=table_name, con=engine, if_exists='append')
        
        t_end = time()
        
        print('inserted another chunk..., took %.3f seconds' %(t_end - t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # all of the arguments that need to be parsed
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of table where results will be written to')
    parser.add_argument('--url', help='url of the csv file')

    #will store all of the arguments in a dictionary
    args = parser.parse_args()
    
    main(args)

#go to the "untitled" file to get the terminal command to run the script