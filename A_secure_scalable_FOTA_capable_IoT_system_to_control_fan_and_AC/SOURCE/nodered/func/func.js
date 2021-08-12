module.exports = function(RED) {
  function funcNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    var c = node.context();
    var f = c.flow;
    var g = c.global;
    node.name = config.name;
    node.content = config.content;
    var log = m => node.warn(m);
    node.on('input', function(msg, send, done) { 
      var pl = p => {msg.payload = p};
      try {
        eval('function core(msg) {'+ node.content + ';return msg}');
        send(core(msg));
        done();
      }
      catch(err) {
        done(err.message);
      }
    });
  }
  RED.nodes.registerType("func", funcNode);
}
