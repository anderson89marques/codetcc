import transaction
import threading
import multiprocessing
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#from zope.sqlalchemy import ZopeTransactionExtension

from codetcc.processamento.constantes import MAPABAIRROS, PATH
from codetcc.processamento.rabbitmqflow.classesflow import ControlProccess
from codetcc.processamento.tokenize import generateTokens
from codetcc.domain.models import Bairro, Localidade

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/consultaCepRabbitmqJsonDB")
DBSession = scoped_session(sessionmaker(bind=engine))()
#DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))()

lock = multiprocessing.Lock()


def findLocalidade(chaveLocalidade):
    print("Chave Localidade: {}".format(chaveLocalidade))
    return DBSession.query(Localidade.id).filter(Localidade.chave == chaveLocalidade).first()


def createBairro(mapAttrs):
    localidade_id = findLocalidade(mapAttrs.get("chaveLocalidade"))
    print(localidade_id)
    bairro = Bairro(mapAttrs)
    bairro.localidade_id = localidade_id
    print(bairro)

    DBSession.add(bairro)


def processaBairrosJson(mapa_linhas):

    print("Processando bairros")
    mapa_linhas = json.loads(mapa_linhas.decode("utf8"))

    for ind, linha in enumerate(mapa_linhas["linhas"]):
        if ind == 0:
            continue

        mapAttrs = generateTokens(linha, MAPABAIRROS)
        createBairro(mapAttrs)
    global lock
    with lock:
        print("With LOCK")
        DBSession.commit()
    return json.dumps({'lotes': mapa_linhas['lote']})


class TheadConsumer(threading.Thread):
    def __init__(self, prod_host, prod_queue, cons_host, cons_queue, callback, *args, **kwargs):
        super(TheadConsumer, self).__init__(*args, **kwargs)

        self.consumer = ControlProccess(prod_host="localhost", prod_queue="_QUEUE_END", cons_host="localhost",
                                        cons_queue="_QUEUE_PROCCESS", callback=callback, name=self.name)

    def _stop(self):
        print("Parando a thead:")

    def run(self):
        print("Esperando Mensagem! i am thread: %r" % self.name)
        self.consumer.start_consuming()


#Usando Multiprocessing
class ProcessConsumer:
    def __init__(self, prod_host, prod_queue, cons_host, cons_queue, callback, *args, **kwargs):
        #super(ProcessConsumer, self).__init__(*args, **kwargs)
        self.name = kwargs["name"]
        self.consumer = ControlProccess(prod_host="localhost", prod_queue="_QUEUE_END", cons_host="localhost",
                                        cons_queue="_QUEUE_PROCCESS", callback=callback, name=self.name)

    def _stop(self):
        print("Parando a thead:")

    def run(self):
        print("Esperando Mensagem! i am thread: %r" % self.name)
        self.consumer.start_consuming()


def start_consumers_bairros_json(number_of_consumers=1):
    pool = multiprocessing.Pool(processes=number_of_consumers)

    jobs = [ProcessConsumer(prod_host="localhost", prod_queue="_QUEUE_END", cons_host="localhost",
                            cons_queue="_QUEUE_PROCCESS", callback=processaBairrosJson, name="consumer_%s" % i)
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
    start_consumers_bairros_json(4)
    #pass