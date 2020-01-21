/**
 * @name monitoring
 * @param {Object} context Lambda context object
 * @return {Object} Object with a message and the original event
 */
exports.handler = async function(event) {
  console.log("got event", event);

  if (event.forceError) {
    throw new Error ("Intentional Error.")
  }

  return {
    message: "Work complete.",
    event
  };
}

if (require.main === module) {
  const event = require("./event.json");
  exports.handler(event);
}