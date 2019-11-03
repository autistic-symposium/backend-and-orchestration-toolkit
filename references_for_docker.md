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

### Learning

##  Docker Certified Associate exam

* [250 Practice Questions for the DCA Exam](https://medium.com/bb-tutorials-and-thoughts/250-practice-questions-for-the-dca-exam-84f3b9e8f5ce).