from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
from codetcc.domain.models import (
    DBSession, Localidade, Logradouro, Base,
    GrandeUsuario, UnidadeOperacional, CaixaPostalComunidade)


@view_config(route_name='home', renderer='templates/home.jinja2')
def my_view(request):
    return {'project': 'codetcc'}


@view_config(route_name='findCep', renderer="json", request_method="GET")
def findcep(request):
    cep = request.params['cep']
    resp = findJson(cep)

    return resp


def findJson(cep):
    local = findLocalidade(cep)
    if local:
        print("Localidade")
        resp = montaResposta(local.nomeOficial, '', '', '', local.siglaUF, local.siglaPais)
    else:
        logradouro = findLogradouro(cep)
        if logradouro:
            print("Logradouro")
            resp = montaResposta(logradouro.tipoOficialLogradouro + logradouro.nomeOficial, logradouro.informacaoAdicional, logradouro.bairro.nomeOficial,
                                 logradouro.localidade.nomeOficial, logradouro.localidade.siglaUF,
                                 logradouro.localidade.siglaPais)
        else:
            gUsuario = findGrandeUsuario(cep)

            if gUsuario:
                print("Grande Usuário")
                print(gUsuario)
                resp = montaResposta(gUsuario.endereco.tipoOficialLogradouro + gUsuario.endereco.nomeOficial, '',
                                     gUsuario.nomeOficialBairro, gUsuario.nomeOficialLocalidade, gUsuario.sigla, 'BR')
            else:
                unidadeOp = findUnidadeOperacional(cep)

                if unidadeOp:
                    print("Unidade Operacional")
                    print(unidadeOp)
                    resp = montaResposta(unidadeOp.endereco.tipoOficialLogradouro + gUsuario.endereco.nomeOficial, '',
                                         unidadeOp.nomeOficialBairro, unidadeOp.nomeOficialLocalidade, unidadeOp.sigla,
                                         'BR')
                else:
                    cpc = findCPC(cep)

                    if cpc:
                        print("Caixa Postal")
                        print(cpc)
                        resp = montaResposta(cpc.nomeCpc, '', '',
                                 cpc.localidade.nomeOficial, cpc.localidade.siglaUF,
                                 cpc.localidade.siglaPais)
                    else:
                        print("CEP não encontrado")
                        resp = {"msg": "cep não encontrado"}
    return resp


def montaResposta(nomeOficial, informacaoAdicional, bairro, nomeLocalidade, siglaUF, siglaPais):
    resp = {'nomeOficial': nomeOficial, 'informacaoAdicional': informacaoAdicional, 'bairro': bairro,
                    'nomeLocalidade': nomeLocalidade, 'siglaUF': siglaUF,
                    'siglaPais': siglaPais}
    return resp


def findLocalidade(cep):
    return DBSession.query(Localidade).filter(Localidade.cep == cep).first()


def findLogradouro(cep):
    return DBSession.query(Logradouro).filter(Logradouro.cep == cep).first()


def findGrandeUsuario(cep):
    return DBSession.query(GrandeUsuario).filter(GrandeUsuario.cep == cep).first()


def findUnidadeOperacional(cep):
    return DBSession.query(UnidadeOperacional).filter(UnidadeOperacional.cep == cep).first()


def findCPC(cep):
    return DBSession.query(CaixaPostalComunidade).filter(CaixaPostalComunidade.cep == cep).first()


@view_config(route_name='start_consume', renderer='json')
def start_consume(request):
    #start_consumers(3)
    return {"msg": ":D"}