import codecs
import transaction
from codetcc.processamento.constantes import PATH, MAPLOCALIDADE
from codetcc.processamento.tokenize import generateTokens
from codetcc.domain.models import Localidade, DBSession


FILE_PATH = PATH.format("DNE_GU_LOCALIDADES.TXT")


def createLocalidade(mapAttrs):
    localidade = Localidade(mapAttrs)
    print(localidade)
    #with transaction.manager:
    DBSession.add(localidade)


def processaLocalidades():
    """ Usei codecs pq estava dando erro:
        UnicodeDecodeError: 'utf8' codec can't decode byte 0x9c, por causa do conteúdo do arquivo
    """
    print("Processando Localidades")
    with codecs.open(FILE_PATH, "r", encoding='iso-8859-1', errors='ignore') as f:

        for ind, linha in enumerate(f.readlines()):
            if ind == 0:
                continue

            mapAttrs = generateTokens(linha, MAPLOCALIDADE)
            createLocalidade(mapAttrs)

            if (ind+1) % 700 == 0:
                transaction.commit()

        transaction.commit()