#!/usr/bin/env python
import pika
import logging
class Receiver:
    def __init__(self, ip,queue,callback):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue, durable=True)
        self.queue=queue
        self.callback=callback
    def close(self):
        self.connection.close()
    def start_listen(self):
        def callback(ch, method, properties, body):
            self.callback(body)
            ch.basic_ack(delivery_tag = method.delivery_tag)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(callback, self.queue)
        self.channel.start_consuming()

if __name__ == "__main__":
    def xxx(body):
        print(" [x] Received %r" % body)
        print(" [x] Done")
    receiver=Receiver('localhost','task_queue',xxx)
    receiver.start_listen()
    