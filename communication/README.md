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
        - the request structure is defined by both client and server and has a boundary
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

- real-time
- the client must be online (connected to the server)
- the client must be able to handle the load
- polling is preferred for light clients.
- used by  RabbitMQ (clients consume the queues, and the messages are pushed to the clients)

<br>

#### the basic idea

1. client connects to a server
2. server sends data to the client
3. client doesn't have to request anything
4. protocol must be bidirectional


<br>

----

### Polling

<br>

* used when a request takes long time to process (e.g., upload a video) and very simple to build
* however, it can be too chatting, use too much network bandwidth and backend resources

<br>

#### the basic idea
 
1. client sends a request
2. server responds immediately with a handle
3. server continues to process the request
4. client uses that handle to check for status
5. multiple short request response as polls


<br>

---

### Long Polling


<br>

* a poll requests where the server only responds when the job is ready (used when a request takes long time to process and it's not real time)
* used by Kafka

<br>

#### the basic idea



1. clients sends a request
2. server responds immediately with a handle
3. server continues to process the request
4. client uses that handle to check for status
5. server does not reply until has the response (and there are some timeouts)


<br>

---

### Server Sent Events


<br>

* one request with a long response, but the client must be online and be able to handle the response

<br>

#### the basic idea

1. a response has start and end
2. client sends a request
3. server sends logical events as part of response
4. server never writes the end of the response
5. it's still a request but an unending response
6. client parses the streams data 
7. works with HTTP

<br>

----

### Publish Subscribe (Pub/Sub)

<br>

* one publisher has many reader (and there can be many publishers)
* relevant when there are many servers (e.g., upload, compress, format, notification)
* great for microservices as it scales with multiple receivers
* loose coupling (clients are not connected to each other and works while clients not running)
* however, you cannot know if the consumer/subscriber got the message or got it twice, etc.
* also, it might result on network saturation and extra complexity
* used by RabbitQ and Kafka



<br>

---

### Multiplexing vs. Demultiplexing

<br>


* used by HTTP/2, QUIC, connection pool, MPTCP
* connection pooling is a technique where you can spin several backend connections and keep them "hot"


<br>

---

### Stateful vs. Stateless


<br>

* a very contentious topic: is state stored in the backend? how do you rely on the state of an application, system, or protocol?
* **stateful backend**: store state about clients in its memory and depends on the information being there
* **stateless backend**: client is responsible to "transfer the state" with every request (you may store but can safely lose it).

<br>

#### Stateless backends

* stateless backends can still store data somewhere else
* the backend remain stateless but the system is stateful (can you restart the backend during idle time while the client workflow continues to work?)

<br>

#### Stateful backend

* the server generate a session, store locally, and return to the user
* the client check if the session is in memory to authenticate and return
* if the backend is restarted, sessions are empty (it never relied on the databases)

<br>

#### Stateless vs. Stateful protocols

* the protocols can be designed to store date
* TCP is stateful: sequences, connection file descriptor
* UDP is stateless: DNS send queryID in UDP to identify queries
* QUIC is stateful but because it sends connectionID to identify connection, it transfer the state across the protocol
* you can build a stateless protocol on top of a stateful one and vice versa (e.g., HTTP on top of TCP, with cookies)

<br>

#### Complete stateless systems

* stateless systems are very rare
* state is carried with every request
* a backend service that relies completely on the input
* **JWT (JSON Web Token)**, everything is in the token and you cannot mark it as invalid




<br>

---

### Sidecar Pattern

<br>

* every protocol requires a library, but changing the library is hard as the app is entrenched to it and breaking changes backward compatibility
* sidecar pattern is the idea of delegating communication through a proxy with a rich library (and the client has a thin library)
* in this case, every client has a sidecar proxy
* pros: it's language agnostic, provides extra security, service discovery, caching.
* cons: complexity, latency

<br>

#### Examples

* service mesh proxies (Linkerd, Istio, Envoy)
* sidecar proxy container (must be layer 7 proxy)


<br>