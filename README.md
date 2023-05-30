# How to start:

## frontend
 - Install node v16
 - Install Yarn v1.22
## Project setup
```
yarn install
```
## compile in dev mode
```
yarn watch
```
## backend
- create .env file in root
- docker-compose up
- docker exec -ti teachbeach_web ./manage.py migrate
- docker exec -ti teachbeach_web ./manage.py createsuperuser
- docker exec -ti teachbeach_web ./manage.py loaddata fixtures.json

Useful
to backup database:
- docker exec -ti teachbeach_postgres pg_dump -c -U teachbeach -h postgres teachbeach -W > dump.sql  (enter password)
maybe required to copy dump into pg container, find the data directory:
- docker inspect -f '{{ json .Mounts }}' teachbeach_postgres | python3 -m json.tool
```
[
    {
        "Type": "bind",
        "Source": "/home/pavel/Developer/teachbeach/postgres-data",
        "Destination": "/var/lib/postgresql/data",
        "Mode": "rw",
        "RW": true,
        "Propagation": "rprivate"
    }
]
```
so copy dump.sql into destination:
- docker cp dump.sql teachbeach_postgres:/var/lib/postgresql/data
now it could be imported:
- docker exec -i teachbeach_postgres psql -U teachbeach -d teachbeach -h postgres -W -f dump.sql  (enter password)
### for production
```
yarn build js/src/main.js
docker-compose -f docker-compose.yml -f docker-compose.deploy.yml up -d
(for update after git pull: docker restart teachbeach_web)
```

# tests
```
npx cypress open
```