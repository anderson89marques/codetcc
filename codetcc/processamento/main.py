
__author__ = 'andersonmarques'

from codetcc.processamento.processaArquivoLocalidades import processaLocalidades

from codetcc.processamento.rabbitmqflow.processarBairrosCosumer import start_consumers_bairros_json
from codetcc.processamento.rabbitmqflow.processarLogradouroConsumer import start_consumers_logradouro_json
from codetcc.processamento.processaArquivoCaixasPostaisComunidade import processaCaixaPostal

from codetcc.processamento.processarArquivoUnidadesOperacionais import processaUnidadeOperacional
from codetcc.processamento.processarArquivoGrandesUsuarios import processaGrandeUsuario

#Essas variáveis representam o tipo de registro


#comentar a linha abaixo assim que o processamento terminar.
#processaLocalidades()
#processaBairros()
#processaCaixaPostal()
#processaLogradouro()
#processaLogradouroParallelamente()

#é preciso sempre que for rodar dar stop e start no rabbitmq
#sudo rabbitmqctl start_app
#start_consumers_bairros_json(4)
start_consumers_logradouro_json(4)
#start_consumers(5)
#start_consumers_json(5)

#processaUnidadeOperacional()
#processaGrandeUsuario()
