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
* the OSI model is 7 layers each describing a specific networking component

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

#### What's a HTTP request

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

* built on top of HTTP/2 (as a hidden implementation) adding several features
* any communication protocol needs client library for the language of choice, but with gRPC you only have one client library
* message format is protocol buffers
* the gRPC modes are: unary, server streaming, client streaming, and bidirectional streaming
* **pros**: fast and compact, one client library, progress feedback (upload), cancel request (H2), H2/protobuf
* **cons**: schema, thick client (libraries have bugs), proxies, no native error handling, no native browser support, timeouts (pub/sub)

<br>

---

### WebRTC (web real-time communication)

<br>

* find a p2p path to exchange video and audio in an efficient and low latency manner
* standardized API
* enables rich communication browsers, mobile, IOT devices
* **pros**: p2p is great (low latency for high bandwidth content), standardized api
* **cons**: maintaining STUN and TURN servers, p2p falls apart in case of multiple participants (e.g. discord)

<br>

#### WebRTC overview

1. A wants to connect to B
2. A finds out all possible ways the public can connect to it
3. B finds out all possible ways the public can connect to it
4. A and B signal this session information via other means (whatsapp, QR, tweet, etc.)
5. A connects to B via the most optimal path
6. A and B also exchanges their supported media and security