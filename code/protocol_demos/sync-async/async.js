const fs = require("fs");

console.log("first");

fs.readFile("file.txt", (err,data)=> console.log(data.toString()));

console.log("second");
