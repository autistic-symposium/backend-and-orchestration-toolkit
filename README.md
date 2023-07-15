## ☁️🧰 master orchestration and backend engineering 

<br>

<p align="center">
<img src="https://github.com/go-outside-labs/orchestration-toolkit/assets/1130416/ad6b4bf7-b306-4a57-8f20-62193ee4091d" width="55%" align="center" style="padding:1px;border:1px solid black;"/>
 </p>


<br>

### learn the fundamentals

<br>

* **[communication patterns](communication/)**
  * Request Response model
  * Synchronous vs. Asynchronous workloads
  * Push
  * Polling and Long Polling
  * Server-Sent Events
  * Publish-Subscribe (Pub/Sub)
  * Multiplexing vs. Demultiplexing
  * Stateful vs. Stateless
  * Sidecar Pattern

<br>

* **[execution patterns](execution/)**
  * backend execution patterns
  * the process, the thread, the cpu time
  * reading and sending socket data
  * the listener, the acceptor, the reader
  * single listener, acceptor, and reader thread execution pattern
  * single listener, acceptor, and multiple readers thread execution pattern
  * single listener, acceptor, readers with message load-balancing execution pattern
  * multiple accepter threads on a single socket execution pattern
  * multiple listeners, acceptors, and reader with socket-sharding execution pattern
  * backend idempotency
  * nagle's algorithm

  <br>

* **[protocols](protocols/)**
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
* **[protocol demos](code/protocol_demos/)**

<br>

---

### more resources

<br>

* **[my end-to-end pipeline on AWS SQS + lambda + SNS](https://github.com/go-outside-labs/aws-pipeline-py)**
* **[saw, a multi-purpose tool for aws cloudwatch logs](https://github.com/TylerBrock/saw)**
