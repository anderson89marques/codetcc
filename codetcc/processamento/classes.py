__author__ = 'andersonmarques'


class Localidade(object):
    def __init__(self, mapAttrs=None):
        self.siglaPais = None
        self.siglaUF = None
        self.chave = None
        self.nomeOficial = None
        self.cep = None
        self.abreviaturaLogradouro = None
        self.tipoLocalidade = None
        self.situacaoLocalidade = None
        self.separador = None
        self.chaveSubordinacao = None
        self.siglaDRLocalidade = None
        self.codigoIBGE = None

        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "Sigla Pais:{}; Sigla UF:{}; CEP: {}".format(self.siglaPais, self.siglaUF, self.cep)


class Bairro:
    def __init__(self, mapAttrs=None):
        self.sigla = None
        self.chaveLocalidade = None
        self.nomeOficialLocalidade = None
        self.chave = None
        self.nomeOficial = None
        self.abreviatura = None
        self.localidade = None

        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "Sigla:{}; nome:{}; chave:{}".format(self.sigla, self.nomeOficial, self.chave)


class CaixaPostalComunidade:
    def __init__(self, mapAttrs=None):
        self.sigla = None
        self.chaveLocalidade = None
        self.nomeOficialLocalidade = None
        self.cep = None
        self.nomeCpc = None
        self.chaveCpc = None
        self.enderecoCpc = None
        self.numeroInicialCpc = None
        self.numeroFinalCpc = None
        self.areaAbrangencia = None
        self.localidade = None

        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "Sigla:{}; nome:{}; chave:{}; cep:{}".format(self.sigla, self.nomeCpc, self.chaveCpc, self.cep)


class Logradouro:
    def __init__(self, mapAttrs=None):
        self.sigla = None
        self.chaveLocalidade = None
        self.nomeOficialLocalidade = None
        self.chaveBairro = None
        self.bairroInicial = None
        self.chaveBairroFinal = None
        self.bairroFinal = None
        self.tipoOficialLogradouro = None
        self.preposicao = None
        self.patenteOficial = None
        self.chaveLogradouro = None
        self.nomeOficial = None
        self.abreviaturaLogradouro = None
        self.informacaoAdicional = None
        self.cep = None
        self.indicadorGrandeUsuario = None
        self.numeroInicialTrecho = None
        self.numeroFinaltrecho = None
        self.identificacaoParidade = None
        self.chaveSeccionamento = None
        self.tipoLogradouroAtivo = None
        self.localidade = None

        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "Sigla:{}; Nome:{}; ChaveSeccionamento:{}; cep:{}"\
            .format(self.sigla, self.nomeOficial,
                    self.chaveSeccionamento, self.cep)


class UnidadeOperacional:
    def __init__(self, mapAttrs):
        self.sigla = None
        self.chaveLocalidade = None
        self.chaveBairro = None
        self.nomeOficialBairro = None
        self.tipoUnidadeOperacional = None
        self.cep = None
        self.nomeOficialLocalidade = None
        self.chaveUnidadeOperacional = None
        self.nomeOficialUnidadeOperacional = None
        self.abreviaturaUnidadeOperacional = None
        self.tipoNumeracaoCaixaPostalFaixa1 = None
        self.numeroInicialCaixaPostalFaixa1 = None
        self.numeroFinalCaixaPostalFaixa1 = None
        self.tipoNumeracaoCaixaPostalFaixa2 = None
        self.numeroInicialCaixaPostalFaixa2 = None
        self.numeroFinalCaixaPostalFaixa2 = None
        self.tipoNumeracaoCaixaPostalFaixa3 = None
        self.numeroInicialCaixaPostalFaixa3 = None
        self.numeroFinalCaixaPostalFaixa3 = None
        self.endereco = None
        self.localidade = None

        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "Sigla:{}; Nome:{}; ChaveUnidadeOperacional:{}; cep:{};Endereco: {}"\
            .format(self.sigla, self.nomeOficialUnidadeOperacional,
                    self.chaveUnidadeOperacional, self.cep, self.endereco)


class GrandeUsuario:
    def __init__(self, mapAttrs):
        self.sigla = None
        self.chaveLocalidade = None
        self.nomeOficialLocalidade = None
        self.chaveBairro = None
        self.nomeOficialBairro = None
        self.chaveGrandeUsuario = None
        self.nomeOficialGrandeBairro = None
        self.cep = None
        self.abreviaturaLogradouro = None
        self.endereco = None
        self.localidade = None

        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "Sigla:{}; ChaveGrandeUsuario:{}; cep:{};Endereco: {}"\
            .format(self.sigla, self.chaveGrandeUsuario, self.cep, self.endereco)


class Endereco:
    def __init__(self, mapAttrs):
        self.chave = None
        self.tipoOficialLogradouro = None
        self.preposicao = None
        self.patenteOficialLogradouro = None
        self.chaveLogradouro = None
        self.nomeOficial = None
        self.numeroLote = None
        self.nomeComplemento1 = None
        self.numeroComplemento1 = None
        self.nomeComplemento2 = None
        self.numeroComplemento2 = None
        self.tipoOficial = None
        self.numero = None

        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "NomeOficial:{}; Chave:{}"\
            .format(self.nomeOficial, self.chave)
