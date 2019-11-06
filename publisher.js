var mqtt = require('mqtt');

var options = {
  clientId: 'mqttjs_' + Math.random().toString(16).substr(2, 8),
  qos:2,
//  username: 'abc',
//  password: 123,
  protocolId: 'MQTT',
  clean:false,
  protocolVersion: 4,
};
//mqtt.connect('mqtt://192.168.43.79')
var client = mqtt.connect('ws:0.0.0.0:8800',{
        username: "publisher2",
        password: '123'
});
client.on('connect', function () {
setInterval(function(){
var published_data = Math.floor(Math.random() * 1001);
var data = published_data.toString();
client.subscribe('myTopic2');
client.publish('myTopic2',data,options,function(err){
  if (err) {
    console.log(err);
    //process.exit(1);
  }
});
console.log('Message Sent :'+data);
}, 5000);});


client.on('reconnect', function(){
  console.log('reconnect');
})

client.on('offline', function(){
  console.log('offline');
})
client.on('error', () => {
  console.log('got error');
});
