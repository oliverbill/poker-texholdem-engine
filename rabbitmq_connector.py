#!/usr/bin/env python
import pika


class RabbitMQConnector:
    def __init__(self, queue_name: str):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
    def publish(self, msg: str, queue_name: str, exchange_name=''):
        self.channel.queue_declare(queue=exchange_name)
        self.channel.basic_publish(exchange=exchange_name,
                                   routing_key=queue_name,
                                   body=msg)
        print("Sent " + msg)
        self.connection.close()
    def consume(self, queue_name='') -> str:
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        msg_body = ''

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            msg_body = body

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(callback,
                                   queue=queue_name)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
