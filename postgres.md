# Setting up PostgreSQL using Docker

### Run Docker Container

#### install docker from website
#### Download image from command line
```
docker pull postgres
```
#### run docker
```
docker run --name postgresql-container -p 5432:5432 -e POSTGRES_PASSWORD=somePassword -d postgres
```

### Initialize PostgreSQL

Now you have to initialize your PostgreSQL, which includes creating a new database and creating a new database user for the server to make connection.

#### check your container id
```
docker ps
```
#### enter your postres container
```
docker exec -it <container_id> bash
```
#### exec postgres
```
psql -h localhost -p 5432 -U postgres -W
```
#### PSQL commands
Use the following commands to create a new database and user for the server to log in.
```
CREATE DATABASE dbname;
CREATE USER username WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE dbname TO username;
ALTER USER username WITH SUPERUSER;
```
### Fill up .env file
The information required is as follows.
```
SECRET_KEY=<POSTGRES_PASSWORD when you created the container>
DB_NAME=<DB you created in postgres>
DB_USER=<DB user you created in postgres>
DB_PASSWORD=<DB user you set in postgres>
DB_HOST=<ip address of the container, localhost by default>
DB_PORT=5432
```

### Stop Your database
```
docker stop <container_id>
```
You can restart the container by running
```
docker start <container_id>
```