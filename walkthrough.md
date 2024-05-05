# to run postgres container
# create the postgres network
docker network create pg-network

# create docker volume
docker volume create --name ny_taxi_postgres_data -d local

# run postgres container
docker run -it \
    -e POSTGRES_USER=root \
    -e POSTGRES_PASSWORD=root \
    -e POSTGRES_DB=ny_taxi \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13

# to remove ny_taxi_postgres_data: sudo rm -rf ny_taxi_postgres_data

# to disconnect: /q + enter

# to start back up container
docker start pg-database #or include the container id

# to connect to database using pgcli
pgcli -h localhost -p 5432 -u root -d ny_taxi

# to reconnect to database: psql -h <hostname> -U <username> -d <database_name>
# to reconnect to database: 
psql -h localhost -U root -d ny_taxi

# to run pgadmin container
# run container
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
    -e PGADMIN_DEFAULT_PASSWORD=root \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4

# to start pg admin container
docker start pgadmin #or container id


# to convert the upload_data jupyter file to a python script
jupyter nbconvert --to script upload_data.ipynb

# to turn a zipped file into normal csv and then save it into the URL variable and to run ingest_data.py script
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL} \

# to build new dockerfile with ingest_data script, this will also create give this new image a tag called taxi_ingest:v001
docker build -t taxi_ingest:v001 .

# to run new container
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url=${URL} \

# host has to be pg-database since your connecting the postgres docker container

# docker compose is a what that you dont have to run two seperate containers under the same network, creating the compose yml file with the two services will automatically have them on the same network

# to start a docker compose
docker-compose up -d
# to shut it down
docker-compose down
# this will also remove the containers, runing docker compose up will recreate the containers