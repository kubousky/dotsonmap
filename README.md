# build and run
docker-compose up -d --build

# remove
docker-compose down

# up and run
docker-compose up

# ran command
docker-compose run web python manage.py migrate / test
docker-compose run web python manage.py startapp <name>

# enter container:
docker exec -it <container_name> sh

# backup
# command insider postgres container ('t' comes from tar)
pg_dump -u postgres -W -F t postgres > backup.tar

