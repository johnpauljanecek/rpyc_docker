#command used to build docker container
docker build -t="rpyc_docker_ipython" .

#command used to run a shell with docker sock forwarded
docker run -i -t -p 9999:9999/tcp -v /var/run/docker.sock:/run/docker.sock rpyc_docker_ipython /bin/bash

#listening on 0.0.0.0 instead of local host so ipython can be connected to outside container
docker run -i -t -p 9999:9999/tcp -v /var/run/docker.sock:/run/docker.sock rpyc_docker_ipython /usr/local/bin/ipython notebook --ip=0.0.0.0 --port 9999 --no-browser

#name the container so it can be restarted
docker run -i -t -p 9999:9999/tcp -v=/var/run/docker.sock:/run/docker.sock -v=/home/john:/home/john  --name ipython_container rpyc_docker_ipython 
docker start -a -i  ipython_container

docker run -i -t -p 9999:9999/tcp -v /var/run/docker.sock:/run/docker.sock -v /home/john:/home/john --name ipython_container rpyc_docker_ipython /bin/bash

/usr/local/bin/ipython notebook  --ip=* --port 9999 --no-browser