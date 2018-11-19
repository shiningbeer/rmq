#!/usr/bin/env python
from util.receiver import Receiver
from util.logger import logger
def xxx(body):
    logger.info("Received %r" % body)
result_receiver=Receiver('localhost','result_queue',xxx)
result_receiver.start_listen()