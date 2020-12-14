'''
Logger use RabbitMQ.

Author: minhdq99hp@gmail.com
'''

class Logger:
    EXCHANGE = 'log'
    EXCHANGE_TYPE = 'topic'

    def __init__(self, host, port, username, password):
        self._credentials = pika.PlainCredentials(username, password)
        self._host = host
        self._port = port

        self._params = pika.ConnectionParameters(host=host, port=port, credentials=self._credentials)

        self._connection = None
        self._channel = None

        self.connect()


    def connect(self):
        if not self._connection or self._connection.is_closed:
            self._connection = pika.BlockingConnection(self._params)
            self._channel = self._connection.channel()
            self._channel.exchange_declare(exchange=self.EXCHANGE, exchange_type=self.EXCHANGE_TYPE)


    def send(self, **kwargs):
        data = dict(**kwargs)
        data.setdefault('log_type', INFO)
        data.setdefault('updated_datetime', now().isoformat())

        rt = 0
        max_retry = 3

        while True:
            try:
                self._channel.basic_publish(exchange='log', routing_key=f"", body=json.dumps(data), properties=pika.BasicProperties(delivery_mode=2))
                break
            except (pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPChannelError):
                rt += 1

                if rt == max_retry:
                    print("Unable to send log.")
                    traceback.print_exc()
                    break

                self.connect()
    
    def __del__(self):
        if self._connection and self._connection.is_open:
            self._connection.close()

