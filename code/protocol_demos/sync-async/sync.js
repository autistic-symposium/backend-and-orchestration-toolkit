const fs = require("fs");

console.log("first");

const res = fs.readFileSync("file.txt");

console.log(res);

console.log("second");

