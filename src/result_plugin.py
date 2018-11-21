#!/usr/bin/env python
from util.receiver import Receiver
from util.logger import logger
import ConfigParser
config=ConfigParser.ConfigParser()
config.read('config.ini')
host=config.get('rmq','host')
channel=config.get('rmq','plugin_task_channel')
def xxx(body):
    logger.info("Received %r" % body)
result_receiver=Receiver('localhost','plugin_result_queue',xxx)
result_receiver.start_listen()