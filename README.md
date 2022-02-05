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
1) Auto login when updated
2) show user name when logged-in
3) \dotsonmap\core\models.py class Dot -> Tag ManyToOne?
4) Tag required for Dot
5) class Tag and Dot - Do not delet Published Dots if the user is deleted
