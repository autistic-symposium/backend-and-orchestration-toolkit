## 🪡 Protocols

<br>

#### What's a protocol

* a protocol is a system that allows two parties to communicate
* they are designed with a set of properties, depending on their purpose

<br>

#### Protocol design properties


* **data format**
    - text based (plain text, JSON, XML)
    - binary (protobuf, RESP, h2, h3)
* **transfer mode**
    - message based (UDP, HTTP)
    - stream (TCP, WebRTC)
* **addressing system**
    - DNS name, IP, MAC
* **directionality**
    - bidirectional (TCP)
    - unidirectional (HTTP)
    - full/half duplex
* **state**
    * stateful
    * stateless
* **routing**
    * proxies, gateways



<br>

#### Why do you need a communication model?

* you want to build agnostic applications
* without a standard model, upgrading network equipments become difficult
* innovations can be done in each layer separately without affecting the rest of the models
* the OSI model is 7 layers, each describing a specific networking component

<br>

#### What's the OSI model?

* **layer 7**, application: HTTP, FTP, gRCP
* **layer 6**, presentation: encoding, serialization
* **layer 5**, session: connection establishment, TLS
* **layer 4**, transport: UDP, TCP 
* **layer 3**, network: IP
* **layer 2**, data link: frames, mac address ethernet
* **layer 1**, physical: electric signals, fiber or radio waves


<br>

##### An example sending a POST request

* **layer 7:** POST request with JSON data to HTTP server
* **layer 6:** serialize JSON to flat byte strings
* **layer 5:** request to establish TCP connection/TLS
* **layer 4:** send SYN request target port 443
* **layer 3:** SYN is placed an IP packet(s) and adds the source/dest IPs
* **layer 2:** each packet goes into a single frame and adds the source/dest MAC addresses
* **layer 1:** each frame becomes a string of bits which converted into either radio signal (wifi), electric signal (ethernet), or light (fiber)

<br>

---

### HTTP/1.1, 2, 3

<br>

* clients example: browser, apps that make http request
* server examples: IIS, Apache TomCat, Python Tornado, NodeJS 

<br>

#### What's an HTTP request

* a method (GET, POST, etc.)
* a path (the URL)
* a protocol (HTTP/1.1, 2, 3 etc.)
* headers (key-values)
* body

<br>

#### HTTP/2

* by google, called SPDY
* support compression in both head and body
* multiplexing
* server push
* secure by default
* protocol negotiation during TLS (NPN/ALPN)

<br>

#### HTTP/3

<br>

* HTTP over QUIC and multiplexed streams over UDP
* merges connection setup + TLS in one handshake
* has congestion control at stream level

<br>

----

### WebSockets (ws://, wss://)

<br>

* bidirectional communications on the web
* use cases: chatting, live feed, multiplayer gaming, showing client progress/logging
* apps: twitch, whatsapp
* **pros**: full-duplex (no polling), http compatible, firewall friendly
* **cons**: proxying is tricky, layer 7 load balancing is challenging (timeouts), stateful and difficult to horizontally scale
* long polling and side server events might be better solutions

<br>

----

### gRPC 

<br>

* built on top of HTTP/2 (as a hidden implementation), adding several features
* any communication protocol needs client library for the language of choice, but with gRPC you only have one client library
* message format is protocol buffers
* the gRPC modes are: unary, server streaming, client streaming, and bidirectional streaming
* **pros**: fast and compact, one client library, progress feedback (upload), cancel request (H2), H2/protobuf
* **cons**: schema, thick client (libraries have bugs), proxies, no native error handling, no native browser support, timeouts (pub/sub)

<br>

---

### WebRTC (web real-time communication)

<br>

* find a p2p path to exchange video and audio in an efficient and low-latency manner
* standardized API
* enables rich communication browsers, mobile, IOT devices
* **pros**: p2p is great (low latency for high bandwidth content), standardized api
* **cons**: maintaining STUN and TURN servers, p2p falls apart in case of multiple participants (e.g., discord)

<br>

#### WebRTC overview

1. A wants to connect to B
2. A finds out all possible ways the public can connect to it
3. B finds out all possible ways the public can connect to it
4. A and B signal this session information via other means (whatsapp, QR, tweet, etc.)
5. A connects to B via the most optimal path
6. A and B also exchange their supported media and security


<br>

-----

### Proxies

<br>

#### What's a proxy

* a server that makes requests on your behalf (you as a client)
* this means that your tcp connection is being established not with the server, but with the proxy
* in other words, the proxy has the role of layer 4, but layer 7 content gets forwarded (there are exceptions when the proxy adds a header such as with `X-Forwarded-For`)
* **uses**: caching, anonymity, logging, block sites, microservices

<br>

#### What's a reverse proxy

* the client does not know the "final destination server", meaning that the server thar serves the url requested could be a reverse proxy that will forward the request to the underline server
* **uses**: load balancing, caching, CDN, api gateway/ingress, canary deployment, microservices




<br>


#### Layer 4 vs. Layer 7 Load Balancers

<br>

* load balancers, also known as fault tolerant systems, is a reverse proxy talking to many backends
* a **layer 4 load balancer** starts with several TCP connection and keep them "warm"
    - when a user starts a connection, this connection will have a state, the LB chooses one server and all segments for that connection go to that server and through ONE connection (layer 4 is stateful)
    - the LB almost acts like a router
    - **pros**: simpler load balancing, efficient, more secure, works with any protocol, one TCP connection (NAT)
    - **cons**: no smart load balancing, NA services, sticky per connection, no caching, protocol unaware (can be risky) bypass rules
* a **layer 7 load balancer** starts with several TCP connection and keep them "warm", but in this case, when a client connects to the L7 LB, it becomes protocol specific
    - any logical request will be buffered, parsed, and then forwarded to a new backend server
    - this could be one or more segments
    - certificates, private keys, all need to live in the load balancer
    - **pros**: smart LB, caching, great for microservices, API gateway logic, authentication
    - **cons**: expensive (because it's looking at the data), decrypts (terminates TLS), two TCP connections, needs to buffer, needs to understand protocol