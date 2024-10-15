## Kafka Topics Cheatsheet

#### Create a temporary interactive container

```
kubectl exec -it -n <ns> kafka-tools -- bash
```

### List consumer groups

```
kafka-consumer-groups --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" --list
```

### Inspect a consumer group

```
kafka-consumer-groups --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" --describe --group GROUP
```


### Remove Lag - Reset a consumer group to latest

Reset offsets to latest (speeds up reset in Grafana):

```
kafka-consumer-groups --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" --group GROUP \
--reset-offsets --topic TOPIC --to-earliest --dry-run
```

### Delete a Consumer Group

Reset offsets to latest (speeds up reset in Grafana):

```
kafka-consumer-groups --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" --group GROUP \
--reset-offsets --topic TOPIC --to-earliest --dry-run
```

### Delete group.

```
kafka-consumer-groups --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" --group GROUP --delete 
Shift consumer back 10k
```

### Specify the partition to shift, else all will be shifted

```
kafka-consumer-groups --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" --group GROUP \
--topic TOPIC:0 --reset-offsets --shift-by -10000
```
