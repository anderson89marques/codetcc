import codecs

import transaction

from codetcc.processamento.constantes import CABECALHO, DADOS, ENDERECO, PATH
from codetcc.processamento.tokenize import generateTokens
from codetcc.domain.models import UnidadeOperacional, Endereco, DBSession, Localidade, Bairro

FILE_PATH = PATH.format("DNE_GU_UNIDADES_OPERACIONAIS.TXT")

mapUnidadesOperacionais = {CABECALHO:
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
                                {'descricao': 21}],
                           DADOS:
                               [{'sigla': 2},
                                {'separador': 6},
                                {'chaveLocalidade': 8},
                                {'nomeOficialLocalidade': 72},
                                {'separador': 5},
                                {'chaveBairro': 8},
                                {'nomeOficialBairro': 72},
                                {'tipoUnidadeOperacional': 72},
                                {'cep': 8},
                                {'separador': 6},
                                {'chaveUnidadeOperacional': 8},
                                {'nomeOficialUnidadeOperacional': 72},
                                {'abreviaturaUnidadeOperacional': 36},
                                {'tipoNumeracaoCaixaPostalFaixa1': 1},
                                {'numeroInicialCaixaPostalFaixa1': 7},
                                {'numeroFinalCaixaPostalFaixa1': 7},
                                {'tipoNumeracaoCaixaPostalFaixa2': 1},
                                {'numeroInicialCaixaPostalFaixa2': 7},
                                {'numeroFinalCaixaPostalFaixa2': 7},
                                {'tipoNumeracaoCaixaPostalFaixa3': 1},
                                {'numeroInicialCaixaPostalFaixa3': 7},
                                {'numeroFinalCaixaPostalFaixa3': 7}],
                           ENDERECO:
                               [{'separador': 6},
                                {'chave': 8},
                                {'tipoOficialLogradouro': 72},
                                {'preposicao': 3},
                                {'patenteOficialLogradouro': 72},
                                {'separador': 6},
                                {'chaveLogradouro': 8},
                                {'nomeOficial': 72},
                                {'numeroLote': 11},
                                {'nomeComplemento1': 36},
                                {'numeroComplemento1': 11},
                                {'nomeComplemento2': 36},
                                {'numeroComplemento2': 11},
                                {'tipoOficial': 36},
                                {'numero': 36}]}


def findLocalidade(chaveLocalidade):
    return DBSession.query(Localidade).filter(Localidade.chave == chaveLocalidade).first()


def findBairro(chaveBairro):
    return DBSession.query(Bairro).filter(Bairro.chave == chaveBairro).first()


def createEndereco(mapAttrs, ctx):
    localidade = findLocalidade(mapAttrs.get("chaveLocalidade"))
    bairro = findBairro(mapAttrs.get("chaveBairro"))
    endereco = Endereco(mapAttrs)
    ctx['unidadeOperacional'].endereco = endereco
    ctx['unidadeOperacional'].localidade = localidade
    ctx['unidadeOperacional'].bairro = bairro
    print(ctx['unidadeOperacional'])
    if ctx['unidadeOperacional'].chaveUnidadeOperacional:
        DBSession.add(ctx['unidadeOperacional'])


def createUnidadeOperacional(mapAttrs, ctx):
    unidadeOperacional = UnidadeOperacional(mapAttrs)
    ctx['unidadeOperacional'] = unidadeOperacional


def processaUnidadeOperacional():
    """ Usei codecs pq estava dando erro:
        UnicodeDecodeError: 'utf8' codec can't decode byte 0x9c, por causa do conteúdo do arquivo
    """
    print("Processando Unidades Operacionais")

    with codecs.open(FILE_PATH, "r", encoding='iso-8859-1', errors='ignore') as f:
        ctx = {'unidadeOperacional': None}

        for ind, linha in enumerate(f.readlines()):
            if ind == 0:
                continue

            mapAttrs = generateTokens(linha, mapUnidadesOperacionais)
            if linha.startswith("D"):
                createUnidadeOperacional(mapAttrs, ctx)
            else:
                createEndereco(mapAttrs, ctx)

            if (ind+1) % 800 == 0:
                    transaction.commit()
        transaction.commit()