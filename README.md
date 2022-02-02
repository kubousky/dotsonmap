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

# test
docker-compose run --rm  web python manage.py test

### TO-DO List
1) \dotsonmap\core\models.py class Dot -> Tag ManyToOne?
2) Auto login when updated
3) show user name when logged-in
4) class Tag and Dot - Do not delet Dots if the user is deleted
