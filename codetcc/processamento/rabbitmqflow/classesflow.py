import json
import pika
from pika.exceptions import ConnectionClosed
import multiprocessing


class Producer:
    def __init__(self, host=None, queue_name=None, control=None):
        self.host = host
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            self.channel = self.connection.channel()
            # definindo a fila
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            self.channel.confirm_delivery()
        except Exception as e:
            print(e)

    def close_connection(self):
        self.connection.close()

    def send_message(self, msg, lbuffer=None):
        print("Enviando Mensagem:%r" % msg)
        # dados_msg = {"arquivoId": ctx["arquivoId"], "linhas": lbuffer}
        # dados_msg = json.dumps(dados_msg)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=msg)


class Consumer:
    def __init__(self, host, queue_name, callback, control=None):
        self.connection = None
        self.channel = None
        self.host = host
        self.queue_name = queue_name
        self.callback = callback
        self.control = control

    def receiver_message(self, channel, method, properties, body):
        # print("body:{}".format(body.decode("utf8")))
        try:
            resp = self.callback(body)  # resposta deve ser json(eu defini assim)
            if resp:  # enviando resposta para a pilha de controle
                #resp = json.loads(resp)
                resp["name"] = self.control.name
                print("RESP: %r" % resp)
                #if not resp.get("ack"):  # Quando o receiver não for o consumer do produtor
                #    resp["name"] = self.control.name
                    #self.control.start_producer()
                    #self.control.send_menssage(msg=json.dumps(resp))
                    #self.control.stop_producer()
                channel.basic_ack(delivery_tag=method.delivery_tag)
        except ConnectionClosed as c:
            print("ConnectionResetError: {}".format(c.__str__()))
            self.start_consuming()

    def connect(self):
        try:
            print("QUEUE NAME: %s" % self.queue_name)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, heartbeat_interval=20))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            self.channel.basic_consume(self.receiver_message, queue=self.queue_name)
        except Exception as e:
            print(e)

    def start_consuming(self):
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()


class ControlProccess:
    def __init__(self, prod_host, prod_queue, cons_host, cons_queue, callback, name=None):
        self.name = name
        self.producer = Producer(host=prod_host, queue_name=prod_queue)
        self.consumer = Consumer(host=cons_host, queue_name=cons_queue, callback=callback, control=self)

    def start_producer(self):
        self.producer.connect()

    def stop_producer(self):
        self.producer.close_connection()

    def send_menssage(self, msg):
        self.producer.send_message(msg)

    def _connect(self):
        print("conectando o consumidor")
        self.consumer.connect()

    def start_consuming(self):
        print("Startando o consumidor:")
        self._connect()
        self.consumer.start_consuming()


if __name__ == "__main__":
    #processamento de bairro, lado produtor
    pass


