var os = require("os");
var hostname = os.hostname();
var http = require('http');
var handleRequest = function(request, response) {
	  console.log('Received request for URL: ' + request.url);
	  response.writeHead(200);
	  response.end("Hello from container " + hostname + "!\n\n");
};
var www = http.createServer(handleRequest);
www.listen(1337);

