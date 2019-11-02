# Docker Best Practices

## Installation in macOS

```
brew cask install docker
```

### Shared Folders

Removing some of the default shared folders can decrease CPU usage (e.g. remove `/Volumes` and `/private`). 

Check storage with:

```
$ docker info |grep Storage
```

### Performance

In case of performance problems you can run:

```
docker run --rm=true -it --privileged --pid=host \
    <image name> /usr/bin/top
```

### Cleaning Up

See disk space:

```
docker system df
```


Remove stopped containers, dangling images, the build cache, and unused networks:

```
docker system prune
```
