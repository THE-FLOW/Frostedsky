var mqtt = require('mqtt');
var client  = mqtt.connect('ws:0.0.0.0:8800',{
        username: "publisher2",
        password: '123'
});
client.on('connect', function () {
    client.subscribe('myTopic2')
  });
client.on('message', function (topic, message, packet) {
console.log("Received '" + message + "' on '" + topic + "'");
//  console.log(' - message', JSON.stringify(message));
//  console.log(' - packet', JSON.stringify(packet));
//  context = message.toString();
//  console.log(context);
});
