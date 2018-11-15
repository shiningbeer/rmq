#!/usr/bin/env node

var amqp = require('amqplib/callback_api');

amqp.connect('amqp://localhost', function(err, conn) {
  conn.createChannel(function(err, ch) {
    var q = 'task_queue';
    
    for (var x=0;x<100;x++){
    var msg = JSON.stringify({q})
        ch.assertQueue(q, {durable: true});
    ch.sendToQueue(q, new Buffer.from(msg), {persistent: true});
    console.log(" [x] Sent '%s'", msg);
    }
  });

  setTimeout(function() { conn.close(); process.exit(0) }, 500);
});