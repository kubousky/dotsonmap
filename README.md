# build and run
docker-compose up -d --build

# remove
docker-compose down

# up and run
docker-compose up

# exec command (run would start a new container)
docker-compose exec web python manage.py migrate / test 
docker-compose exec web python manage.py startapp <name>

# enter container:
docker exec -it <container_name> /bin/sh

# test
docker-compose run --rm  web python manage.py test

# Permissions issue solving
docker exec -it --user root <container_name> /bin/sh
chmod -R 777 /app/core/migrations

# WSL2 -> Docker -> libreries
cd /usr/local/lib/python3.9/site-packages/rest_framework


[Postgres]

# to locate psql
which psql    #/usr/local/bin
# login
/usr/local/bin/psql -d hello_django_dev -U hello_django
# show all tables
\dt+
# show table
\d <table_name>
SELECT * FROM core_dotprivate;   # do not forget about ";" at the end.

# drop DB
docker-compose exec db psql -U <user_name> -d postgres -c “DROP DATABASE <db_name>;”
https://bilesanmiahmad.medium.com/how-to-drop-and-create-a-database-in-docker-part-1-b705ca41a28e
docker-compose exec db psql -U hello_django -d postgres -c “DROP DATABASE hello_django_dev;”
docker-compose exec db psql -U hello_django -d postgres -c “CREATE DATABASE hello_django_dev;”
# backup
# command inside the postgres container ('t' comes from tar)
pg_dump -U <user_name> -W -F t <db_name> > backup.tar



### TO-DO List React
1) Auto login when updated
2) show user name when logged-in

3) \dotsonmap\core\models.py class Dot -> Tag ManyToOne?
4) Tag required for Dot
5) class Tag and Dot - Do not delet Published Dots if the user is deleted
6) if public: user create Tag only or give an option to request new tag creation 

### TO-DO List Django 
1) Dockerfile - "User user" doesn´t work - compromise security)
2)
3) \dotsonmap\core\models.py class Dot -> Tag ManyToOne?
4) Tag required for Dot
5) class Tag and Dot - Do not delet Published Dots if the user is deleted
6) if public: user create Tag only or give an option to request new tag creation 



