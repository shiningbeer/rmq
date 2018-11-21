#!/usr/bin/env python
import pika
from logger import logger
class Sender:
    def __init__(self, ip,queue):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=ip))
        self.channel = self.connection.channel()
        self.queue=self.channel.queue_declare(queue, durable=True)
        self.queue_name=queue
    def send_msg(self,msg):
        self.channel.basic_publish(exchange='',
                            routing_key=self.queue_name,
                            body=msg,
                            properties=pika.BasicProperties(
                                delivery_mode=2,  # make message persistent
                            ))
    def close(self):
        self.connection.close()
    def get_msg_count(self):
        return self.queue.method.message_count

if __name__ == "__main__":
    send=Sender('localhost','task_queue')
    for i in range(10):
        send.send_msg(str(i))
    send.close()