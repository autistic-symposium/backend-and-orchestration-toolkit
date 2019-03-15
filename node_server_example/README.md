# Spinning up a Hello World node server in docker

Build the image:

```
$ make build:
```

Run the container:

```
$ make run
```
    docker build -t  node_app_test .

Check whether the server worked:
```
$ make curl
```

Check container's status:
```
$ make status
```


#### Other useful commands

Exec inside the container:

```
$ docker exec -i -t <container name from status> /bin/bash
```

Check images in disk:

```
$ docker images
```


## Some References:

* [Dockerfiles good practices](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#general-guidelines-and-recommendations).