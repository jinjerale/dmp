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