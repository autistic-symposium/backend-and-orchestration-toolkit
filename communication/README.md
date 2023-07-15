## 📡 communication design patterns

<br>

### Request Response model

<br>

#### used in

    - the web, HTTP, DNS, SSH
    - RPC (remote procedure call)
    - SQL and database protocols
    - APIs (REST/SOAP/GraphQL)

<br>


#### the basic idea

    1. clients sends a request
        - the request structure is defined by both client and server and has a boundary.
    2. server parses the request
        - the parsing cost is not cheap (e.g. `json` vs. `xml` vs. protocol buffers)
        - for example, for a large image, chunks can be sent, with a request per chunk
    3. Server processes the request
    4. Server sends a response
    5. Client parse the Response and consume

<br>

#### an example in your terminal


* see how it always get the headers firsts:

```bash
curl -v --trace marinasouza.xyz

== Info:   Trying 76.76.21.21:80...
== Info: Connected to marinasouza.xyz (76.76.21.21) port 80 (#0)
=> Send header, 79 bytes (0x4f)
0000: 47 45 54 20 2f 20 48 54 54 50 2f 31 2e 31 0d 0a GET / HTTP/1.1..
0010: 48 6f 73 74 3a 20 6d 61 72 69 6e 61 73 6f 75 7a Host: marinasouz
0020: 61 2e 78 79 7a 0d 0a 55 73 65 72 2d 41 67 65 6e a.xyz..User-Agen
0030: 74 3a 20 63 75 72 6c 2f 37 2e 38 38 2e 31 0d 0a t: curl/7.88.1..
0040: 41 63 63 65 70 74 3a 20 2a 2f 2a 0d 0a 0d 0a    Accept: */*....
== Info: HTTP 1.0, assume close after body
<= Recv header, 33 bytes (0x21)
0000: 48 54 54 50 2f 31 2e 30 20 33 30 38 20 50 65 72 HTTP/1.0 308 Per
0010: 6d 61 6e 65 6e 74 20 52 65 64 69 72 65 63 74 0d manent Redirect.
0020: 0a                                              .
<= Recv header, 26 bytes (0x1a)
0000: 43 6f 6e 74 65 6e 74 2d 54 79 70 65 3a 20 74 65 Content-Type: te
0010: 78 74 2f 70 6c 61 69 6e 0d 0a                   xt/plain..
<= Recv header, 36 bytes (0x24)
0000: 4c 6f 63 61 74 69 6f 6e 3a 20 68 74 74 70 73 3a Location: https:
0010: 2f 2f 6d 61 72 69 6e 61 73 6f 75 7a 61 2e 78 79 //marinasouza.xy
0020: 7a 2f 0d 0a                                     z/..
<= Recv header, 41 bytes (0x29)
0000: 52 65 66 72 65 73 68 3a 20 30 3b 75 72 6c 3d 68 Refresh: 0;url=h
0010: 74 74 70 73 3a 2f 2f 6d 61 72 69 6e 61 73 6f 75 ttps://marinasou
0020: 7a 61 2e 78 79 7a 2f 0d 0a                      za.xyz/..
<= Recv header, 16 bytes (0x10)
0000: 73 65 72 76 65 72 3a 20 56 65 72 63 65 6c 0d 0a server: Vercel..
<= Recv header, 2 bytes (0x2)
0000: 0d 0a                                           ..
<= Recv data, 14 bytes (0xe)
0000: 52 65 64 69 72 65 63 74 69 
```


<br>

----

### Synchronous vs. Asynchronous workloads

<br>

#### Synchronous I/O: the basic idea

    1. Caller sends a request and blocks
    2. Caller cannot execute any code meanwhile
    3. Receiver responds, Caller unblocks
    4. Caller and Receiver are in sync


<br>

##### example (note the waste!)

    1. program asks OS to read from disk
    2. program main threads is taken off the CPU
    3. read is complete and program resume execution (costly)

<br>

#### Asynchronous I/O: the basic idea

    1. caller sends a request
    2. caller can work until it gets a response
    3. caller either:
        - checks whether the response is ready (epoll)
        - receiver calls back when it's done (io_uring)
        - spins up a new thread that blocks
    4. caller and receiver not in sync

<br>

#### Sync vs. Async in a Request Response

    - synchronicity is a client property
    - most modern client libraries are async


<br>

#### Async workload is everywhere
    - async programming (promises, futures)
    - async backend processing
    - async commits in postgres
    - async IO in Linux (epoll, io_uring)
    - async replication
    - async OS fsync (filesystem cache)

<br>

----

### Push 

<br>

#### pros and coins

    - real time
    - the client must be online (connected to the server)
    - the client must be able to handle the load
    - polling is preferred for light clients

<br>

#### basic idea

    1. client connects to a server
    2. server sends data to the client
    3. client doesn't have to request anything
    4. protocol must be bidirectional

<br>
#### used in

    - RabbitMQ (clients consume the queues, and the messages are pushed to the clients)


<br>

----

### Polling

<br>

#### basic idea
    - when a request takes long time to process (e.g., upload a video)
    - the backend want to sends notification

<br>

---

### Long Polling


<br>

---

### Server Sent Events


<br>

----

### Publish Subscribe (Pub/Sub)


<br>

---

### Multiplexing vs. Demultiplexing


<br>

---

### Stateful vs. Stateless


<br>

---

### Sidecar Pattern


<br>