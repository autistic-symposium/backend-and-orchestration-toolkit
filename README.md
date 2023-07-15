## ☁️🧰 master orchestration and backend engineering 


<br>

### learn the fundamentals

<br>

* **[communication](communication/)**
  * Request Response model
  * Synchronous vs. Asynchronous workloads
  * Push
  * Polling and Long Polling
  * Server Sent Events
  * Publish Subscribe (Pub/Sub)
  * Multiplexing vs. Demultiplexing
  * Stateful vs. Stateless
  * Sidecar Pattern

<br>

* **[protocols](protocols/)**
  * protocol properties
  * protocol properties
  * OSI model
  * internet protocol
  * UDP
  * TCP
  * TLS
  * HTTP/1.1
  * WebSockets
  * HTTP/2
  * HTTP/3
  * gRPC
  * WebRTC

  <br>

* **[HTTP](https/)**
  * https communication 
  * https over TCP with TLS 1.2
  * https over TCP with TLS 1.3
  * https over QUIC (HTTP/3)
  * https over TFO with TLS 1.3
  * https over TCP with TLS 1.3 and ORTT
  * https over QUICK with ORTT

  <br>

* **[execution](execution/)**
  * backend execution patterns
  * the process, the thread, the cpu time
  * reading and sending socket data
  * the listener, the acceptor, the reader
  * single listener, acceptor, and reader thread execution pattern
  * single listener, acceptor, and multiple readers thread execution pattern
  * single listener, acceptor, reader with message load balancing execution pattern
  * multiple accepter threads on a single socket execution pattern
  * multiple listeners, acceptors, and reader with socket sharding execution pattern
  * backend idempotency
  * nagle's algorithm

  <br>

* **[proxy and load balance](proxy_and_lb)**
  * proxy vs. reverse proxy
  * Layer 4 vs. Layer 7 load balancers


<br>

---
### source code and snippets

<br>


* **[docker](code/docker)**
* **[kubernetes](code/kubernetes):**
  * **[spin up a node server](code/kubernetes/node-server-example)**
  * **[kustomize for deployment](code/kubernetes/kustomize)**
  * **[python cdk for deployment](code/kubernetes/python-cdk)**
* **[aws](code/aws)**
* **[gcp](code/gcp)**
* **[chef](code/chef)**
* **[kafka](code/kafka)**

<br>

---

### more resources

<br>

* **[my end-to-end pipeline on AWS SQS + lambda + SNS](https://github.com/go-outside-labs/aws-pipeline-py)**
* **[saw, a multi-purpose tool for aws cloudwatch logs](https://github.com/TylerBrock/saw)**
