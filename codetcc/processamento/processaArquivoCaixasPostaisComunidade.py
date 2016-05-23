import codecs

import transaction

from codetcc import DBSession
from codetcc.domain.models import Localidade, CaixaPostalComunidade
from codetcc.processamento.constantes import CABECALHO, DADOS, PATH
from codetcc.processamento.tokenize import generateTokens

FILE_PATH = PATH.format("DNE_GU_CAIXAS_POSTAIS_COMUNITA.TXT")

mapCPC = {CABECALHO:
              [{'separador': 1},
               {'versao': 5},
               {'separador': 2},
               {'diaGravacao': 2},
               {'separador': 1},
               {'mesGravacao': 3},
               {'separador': 1},
               {'anoGravacao': 4},
               {'separador': 4},
               {'informacaoAutoria': 11},
               {'separador': 1},
               {'identificacaoAutor', 8},
               {'separador': 17},
               {'descricao': 27}],
          DADOS:
              [{'sigla': 2},
               {'separador': 6},
               {'chaveLocalidade': 8},
               {'nomeOficialLocalidade': 72},
               {'cep': 8},
               {'nomeCpc': 72},
               {'chaveCpc': 8},
               {'enderecoCpc': 72},
               {'numeroInicialCpc': 6},
               {'numeroFinalCpc': 6},
               {'areaAbrangencia': 72}]}


def findLocalidade(chaveLocalidade):
    return DBSession.query(Localidade).filter(Localidade.chave == chaveLocalidade).first()


def createCaixaPostal(mapAttrs):
    localidade = findLocalidade(mapAttrs.get("chaveLocalidade"))
    cpc = CaixaPostalComunidade(mapAttrs)
    cpc.localidade = localidade
    print(cpc)
    if cpc.chaveCpc:
        DBSession.add(cpc)


def processaCaixaPostal():
    """ Usei codecs pq estava dando erro:
        UnicodeDecodeError: 'utf8' codec can't decode byte 0x9c, por causa do conteúdo do arquivo
    """
    print("Processando mensalidades")
    with codecs.open(FILE_PATH, "r", encoding='iso-8859-1', errors='ignore') as f:

        for ind, linha in enumerate(f.readlines()):
            if ind == 0:
                continue

            mapAttrs = generateTokens(linha, mapCPC)
            createCaixaPostal(mapAttrs)

            if (ind+1) % 800 == 0:
                    transaction.commit()
        transaction.commit()