import json
import multiprocessing

import threading
import time

from pika.exceptions import ConnectionClosed
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from codetcc.processamento.constantes import MAPLOGRADOURO
from codetcc.processamento.rabbitmqflow.classesflow import ControlProccess
from codetcc.processamento.tokenize import generateTokens
from codetcc.domain.models import Bairro, Logradouro, Localidade


engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/consultaCepRabbitmqJsonDB")
DBSession = scoped_session(sessionmaker(bind=engine))()

# Estou usando a mesma sessão para todas as threads que é o DBSESSION
# será que seria melhor criar um sessão para cada thread?

lock = multiprocessing.Lock()


def findLocalidade(chaveLocalidade):
    return DBSession.query(Localidade.id).filter(Localidade.chave == chaveLocalidade).first()


def findBairro(chaveBairro):
    return DBSession.query(Bairro.id).filter(Bairro.chave == chaveBairro).first()


def createLogradouro(mapAttrs):
    # Acho melhor tirar os métodos que buscam a localidadee e o bairro para recebe-los como parâmetro

    localidade_id = findLocalidade(mapAttrs.get("chaveLocalidade"))
    bairro_id = findBairro(mapAttrs.get("chaveBairro"))
    logradouro = Logradouro(mapAttrs)
    logradouro.localidade_id = localidade_id
    logradouro.bairro_id = bairro_id

    #print(logradouro)
    # with transaction.manager:
    if logradouro.chaveLogradouro:
        DBSession.add(logradouro)


def processaLogradouroForRabbitMqJson(mapa_linhas):
    print("Processando logradouros")
    ini_time = time.clock()
    mapa_linhas = json.loads(mapa_linhas.decode("utf8"))

    for ind, linha in enumerate(mapa_linhas["linhas"]):
        if ind == 0:
            continue

        mapAttrs = generateTokens(linha, MAPLOGRADOURO)
        createLogradouro(mapAttrs)
        #if (ind + 1) % 700 == 0:
        #    transaction.commit()
    global lock
    with lock:
        DBSession.commit()

    return {'lotes': mapa_linhas['lote'], 'time': (time.clock() - ini_time)}


class TheadConsumer(threading.Thread):
    def __init__(self, prod_host, prod_queue, cons_host, cons_queue, callback, *args, **kwargs):
        super(TheadConsumer, self).__init__(*args, **kwargs)

        self.consumer = ControlProccess(prod_host="localhost", prod_queue="_QUEUE_END", cons_host="localhost",
                                        cons_queue="_QUEUE_PROCCESS", callback=callback, name=self.name)

    def _stop(self):
        print("Parando a thead:")

    def run(self):
        print("Esperando Mensagem! i am thread: %r" % self.name)
        try:
            self.consumer.start_consuming()
        except ConnectionClosed as c:
            print("ConnectionResetError huahuahuiahuia")
            self.run()  # SE DER ERRO DE CONEXÃO RECONECTA-SE


class ProcessConsumer:
    def __init__(self, prod_host, prod_queue, cons_host, cons_queue, callback, *args, **kwargs):

        self.name = kwargs["name"]

        self.consumer = ControlProccess(prod_host="localhost", prod_queue="_QUEUE_END", cons_host="localhost",
                                        cons_queue="_QUEUE_PROCCESS", callback=callback, name=self.name)

    def _stop(self):
        print("Parando a thead:")

    def run(self):
        print("Esperando Mensagem! i am thread: %r" % self.name)
        try:
            self.consumer.start_consuming()
        except ConnectionClosed as c:
            print("ConnectionResetError huahuahuiahuia")
            self.consumer.start_consuming()
            self.run()  # SE DER ERRO DE CONEXÃO RECONECTA-SE


def start_consumers_logradouro_json(number_of_consumers=1):
    pool = multiprocessing.Pool(processes=number_of_consumers)

    jobs = [ProcessConsumer(prod_host="localhost", prod_queue="_QUEUE_END", cons_host="localhost",
                            cons_queue="_QUEUE_PROCCESS", callback=processaLogradouroForRabbitMqJson, name="consumer_%s" % i)
            for i in range(number_of_consumers)]

    for job in jobs:
        pool.apply_async(job.run)

    print("Consumidores iniciados!!")

    # Stay alive
    try:
        while True:
            continue
    except KeyboardInterrupt:
        print(' [*] Exiting...')
        pool.terminate()
        pool.join()


if __name__ == '__main__':
    start_consumers_logradouro_json(8)
