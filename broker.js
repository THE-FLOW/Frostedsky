var mosca = require("mosca");
//add redis and soket and alphauser

var ascoltatore = {
  type: 'redis',
  redis: require('redis'),
  db: 2,
  port: 6379,
  return_buffers: true, // to handle binary payloads
  host: "localhost"
};
var redis = require('redis');
var redisdb = redis.createClient(); //creates a client for send and receive data from redis database
redisdb.select(11, function() { /* ... */ });
const settings = {
  port: 1883,
  backend: ascoltatore,
  persistence: {
  factory: mosca.persistence.Redis
},
   http: {
    // port for websockets, MQTT is running in default port 1883
    port: 8800,
    bundle: true,
    static: './public',
  }
}
var defienduser = [{
    userId: 1,
    username:'publisher1',
    password:'123',
    publishTopics:['led', 'abc/e'],
    subscribeTopics:['led', 'text','Alphaorder']
},
{
    userId: 2,
    username:'publisher2',
    password:'123',
    publishTopics:['myTopic2', 'abc/e'],
    subscribeTopics:['myTopic2', 'text','Alphaorder']

}];
var counter=0;
var topic = [];
for(counter ;counter <= (defienduser.length)-1 ; counter+=1){
  topic[counter]=defienduser[counter].subscribeTopics;
}
console.log(topic[0]);
//topic=topic.toString();
//console.log(topic);
var Alphaid =[{
  userId:3,
  username:'Alphaclient',
  password:'123',
  publishTopics:['Alphaorder'],
  subscribeTopics:topic
}]
var users = defienduser.concat(Alphaid);
var usermap = new Map();
redisdb.on('connect', function() {
    console.log('connected to redis for send and receive data');
});
var accunt='';
var authenticate = function(client, username, password, callback){
console.log("client： " + client + " username: " + username + " password:" + password );
   accunt=username;
    var user = users.find(function(data){
      //  console.log(data.toString());
       if(username == data.username && password == data.password) {
           return data;
       }
    })

    if(user){
        console.log("auntiticated");

        usermap.set(client.id, {
            userId: user.userId,
            publishTopics: user.publishTopics,
            subscribeTopics: user.subscribeTopics
        });
         callback(null, true);
    }else{
        console.log("auntication false");
          callback(null, false);
    }
}


var authorizePublish = function(client, topic, payload, callback){
    console.log("authorizePublish: " + client.id + " topic: " + topic + " payload:" + payload );
    let time = new Date();
    var hours=time.getHours();
    var minutes=time.getMinutes();
    var second=time.getSeconds();
    time = 'H:'+hours.toString()+'/'+'M:'+minutes.toString()+'/'+'s:'+second.toString();
    redisdb.hmset(accunt+'pd', {
    'user': client.id,
    'data': payload,
    'time': time}, function(err, reply) {
        console.log('redis is '+reply);
      });
    var user = usermap.get(client.id);
    if(!user){
        console.log('canot find user');
        return;
    }
    if(user.publishTopics.indexOf(topic) < 0){
        console.log('didnt find topic for publishing: ' + topic);
        callback(null, false);
    }else{
        console.log('topic for publishing is found: ' + topic);
        callback(null, true);
    }
}

var authorizeSubscribe = function(client, topic, callback){
    console.log("authorizeSubscribe: " + client + " topic: " + topic );
    var user = usermap.get(client.id);
    if(!user){
        console.log('canot find user');
        return;
    }
    if(user.subscribeTopics.indexOf(topic) < 0){
        console.log('subscribe： didnt find topic for subscribe: ' + topic);
        callback(null, false);
    }else{
        console.log('subscribe：  topic found for subscribe: ' + topic);
        callback(null, true);
    }
}

var server = new mosca.Server(settings);

server.on('ready', function(){
    console.log('Mosca server is up and running in port 1883!')
    console.log('Using port 8000 for MQTT over Web-Sockets!')
    server.authenticate = authenticate;
    server.authorizePublish = authorizePublish;
    server.authorizeSubscribe = authorizeSubscribe;
    console.log('auth ready');
});

server.on('published', function(packet, client){
    console.log('Published: ', packet.payload);
});

server.on('subscribed', function(topic, client){
     console.log('subscribed: ', topic);
});

server.on('unSubscribed', function(topic, client){
     console.log('unSubscribed: ', topic);
})

server.on('clientConnected', function(client){
    console.log('client connected: ', client.id);

});

server.on('clientDisConnected', function(client){

      usermap.delete(client.id);
        console.log('client disConnected: ' + client.id + " userNumber:" + usermap.keys.length);
});
module.exports = server
