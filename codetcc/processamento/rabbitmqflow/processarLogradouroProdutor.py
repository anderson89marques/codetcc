import glob
import json
import datetime
import codecs

from codetcc.processamento.constantes import PATH
from codetcc.processamento.rabbitmqflow.classesflow import ControlProccess

FILE_PATH = PATH.format("DNE_GU_*_LOGRADOUROS.TXT")

global lote
lote = 0

global lotes_processados
lotes_processados = 0


def callback_end_control(msg):
    print("Recebendo FeedBack:{}".format(json.loads(msg.decode("utf8"))))
    global lotes_processados
    lotes_processados += 1

    if lotes_processados == lote:
        print("Fim Processamento {}".format(datetime.datetime.now()))

    # só para que no receiver do consumer do produtor eu mande basic_ack para que eu retire a msg da fila _QUEUE_END
    return json.dumps({'ack': lotes_processados})


def start_producer():
    producer = ControlProccess(prod_host="localhost", prod_queue="_QUEUE_PROCCESS", cons_host="localhost",
                               cons_queue="_QUEUE_END", callback=callback_end_control)
    producer.start_producer()

    inicio = datetime.datetime.now()
    files = glob.glob(FILE_PATH)
    for file_name in files:
        mapa_linhas = {"linhas": [], "lote": 0}
        global lote

        with codecs.open(file_name, "r", encoding='iso-8859-1', errors='ignore') as f:
            for ind, linha in enumerate(f.readlines()):
                if ind == 0:
                    continue

                # cada elemento em linhas é uma linha do arquivo
                mapa_linhas["linhas"].append(linha)

                # enviando de 500 em 500 a fila
                if (ind+1) % 500 == 0:
                    lote += 1
                    mapa_linhas["lote"] = lote
                    producer.send_menssage(msg=json.dumps(mapa_linhas))
                    mapa_linhas["linhas"] = []  # reinicializando a lista de linhas
            else:
                # garantindo que não fique linhas sem ser enviadas, pois pode ser que no final do processamento de um arquivo
                # mapa_linhas["linhas"] contenha um número menor que 500 linhas
                if mapa_linhas["linhas"]:
                    lote += 1
                    mapa_linhas["lote"] = lote
                    producer.send_menssage(msg=json.dumps(mapa_linhas))
                    #mapa_linhas["linhas"] = []  # reinicializando a lista de linhas

    print("INICIO DO PROCESSAMENTO DE ENVIO: {}".format(inicio))
    print("FIM DO PROCESSAMENTO DE ENVIO: {}".format(datetime.datetime.now()))
    print("TOTAL LOTES: %d" % lote)

    producer.stop_producer()
    producer.start_consuming() #startando o consumidor do produtor para controlar o termino dos proessamentos

if __name__ == '__main__':
    start_producer()
