## useful tricks for docker

<br>


#### shared folders

Removing some of the default shared folders can decrease CPU usage (e.g. remove `/Volumes` and `/private`). 

Check storage with:

```
docker info |grep Storage
```


<br>

#### performance

In case of performance problems you can run:

```
docker run --rm=true -it --privileged --pid=host \
    <image name> /usr/bin/top
```

<br>

#### cleaning up

See disk space:

```
docker system df
```


Remove stopped containers, dangling images, the build cache, and unused networks:

```
docker system prune
```
