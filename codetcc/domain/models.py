from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))()  #Para tentar Fazer Funcionar com o multiprocessing
Base = declarative_base()


class Localidade(Base):
    __tablename__ = 'localidade'

    id = Column(Integer, primary_key=True)
    siglaPais = Column(Text)
    siglaUF = Column(Text)
    chave = Column(Text, index=True)
    nomeOficial = Column(Text)
    cep = Column(Text)
    abreviaturaLogradouro = Column(Text)
    tipoLocalidade = Column(Text)
    situacaoLocalidade = Column(Text)
    separador = Column(Text)
    chaveSubordinacao = Column(Text)
    siglaDRLocalidade = Column(Text)
    codigoIBGE = Column(Text)

    def __init__(self, mapAttrs=None):

        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "Sigla Pais:{}; Sigla UF:{}; CEP: {}".format(self.siglaPais, self.siglaUF, self.cep)

#Index("idx_chave_localidade", Localidade.chave)


class Bairro(Base):
    __tablename__ = 'bairro'

    id = Column(Integer, primary_key=True)
    sigla = Column(Text)
    chaveLocalidade = Column(Text)
    nomeOficialLocalidade = Column(Text)
    chave = Column(Text, index=True)
    nomeOficial = Column(Text)
    abreviatura = Column(Text)
    localidade_id = Column(Integer, ForeignKey('localidade.id'))
    localidade = relationship("Localidade", uselist=False) #pra fazer um pra um, mais so um lado sabe do outro.

    def __init__(self, mapAttrs=None):

        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "Sigla:{}; nome:{}; chave:{}; localidade: {}".format(self.sigla, self.nomeOficial, self.chave, self.localidade)

#Index("idx_chave_bairro", Bairro.chave)


class Logradouro(Base):
    __tablename__ = 'logradouro'

    id = Column(Integer, primary_key=True)
    sigla = Column(Text)
    chaveLocalidade = Column(Text)
    nomeOficialLocalidade = Column(Text)
    chaveBairro = Column(Text)
    bairroInicial = Column(Text)
    chaveBairroFinal = Column(Text)
    bairroFinal = Column(Text)
    tipoOficialLogradouro = Column(Text)
    preposicao = Column(Text)
    patenteOficial = Column(Text)
    chaveLogradouro = Column(Text)
    nomeOficial = Column(Text)
    abreviaturaLogradouro = Column(Text)
    informacaoAdicional = Column(Text)
    cep = Column(Text)
    indicadorGrandeUsuario = Column(Text)
    numeroInicialTrecho = Column(Text)
    numeroFinaltrecho = Column(Text)
    identificacaoParidade = Column(Text)
    chaveSeccionamento = Column(Text)
    tipoLogradouroAtivo = Column(Text)
    localidade_id = Column(Integer, ForeignKey('localidade.id'))
    localidade = relationship("Localidade", uselist=False) #pra fazer um pra um, mais so um lado sabe do outro.
    bairro_id = Column(Integer, ForeignKey('bairro.id'))
    bairro = relationship("Bairro", uselist=False) #pra fazer um pra um, mais so um lado sabe do outro.

    def __init__(self, mapAttrs=None):
        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "Sigla:{}; Nome:{}; ChaveSeccionamento:{}; cep:{}; bairro:{}"\
            .format(self.sigla, self.nomeOficial,
                    self.chaveSeccionamento, self.cep, self.bairro)


class CaixaPostalComunidade(Base):
    __tablename__ = 'caixa_postal_comunidade'

    id = Column(Integer, primary_key=True)
    sigla = Column(Text)
    chaveLocalidade = Column(Text)
    nomeOficialLocalidade = Column(Text)
    cep = Column(Text)
    nomeCpc = Column(Text)
    chaveCpc = Column(Text)
    enderecoCpc = Column(Text)
    numeroInicialCpc = Column(Text)
    numeroFinalCpc = Column(Text)
    areaAbrangencia = Column(Text)
    localidade_id = Column(Integer, ForeignKey('localidade.id'))
    localidade = relationship("Localidade", uselist=False) #pra fazer um pra um, mais so um lado sabe do outro.

    def __init__(self, mapAttrs=None):
        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "Sigla:{}; nome:{}; chave:{}; cep:{}; localidade: {}".format(self.sigla, self.nomeCpc, self.chaveCpc,
                                                                            self.cep, self.localidade)


class UnidadeOperacional(Base):
    __tablename__ = 'unidade_operacional'

    id = Column(Integer, primary_key=True)
    sigla = Column(Text)
    chaveLocalidade = Column(Text)
    chaveBairro = Column(Text)
    nomeOficialBairro = Column(Text)
    tipoUnidadeOperacional = Column(Text)
    cep = Column(Text)
    nomeOficialLocalidade = Column(Text)
    chaveUnidadeOperacional = Column(Text)
    nomeOficialUnidadeOperacional = Column(Text)
    abreviaturaUnidadeOperacional = Column(Text)
    tipoNumeracaoCaixaPostalFaixa1 = Column(Text)
    numeroInicialCaixaPostalFaixa1 = Column(Text)
    numeroFinalCaixaPostalFaixa1 = Column(Text)
    tipoNumeracaoCaixaPostalFaixa2 = Column(Text)
    numeroInicialCaixaPostalFaixa2 = Column(Text)
    numeroFinalCaixaPostalFaixa2 = Column(Text)
    tipoNumeracaoCaixaPostalFaixa3 = Column(Text)
    numeroInicialCaixaPostalFaixa3 = Column(Text)
    numeroFinalCaixaPostalFaixa3 = Column(Text)
    endereco_id = Column(Integer, ForeignKey('endereco.id'))
    endereco  = relationship("Endereco", uselist=False, cascade="all") #pra fazer um pra um, mais so um lado sabe do outro.
    localidade_id = Column(Integer, ForeignKey('localidade.id'))
    localidade = relationship("Localidade", uselist=False) #pra fazer um pra um, mais so um lado sabe do outro.
    bairro_id = Column(Integer, ForeignKey('bairro.id'))
    bairro = relationship("Bairro", uselist=False) #pra fazer um pra um, mais so um lado sabe do outro.

    def __init__(self, mapAttrs):
        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "Sigla:{}; Nome:{}; ChaveUnidadeOperacional:{}; cep:{};Endereco: {}, bairro: {}"\
            .format(self.sigla, self.nomeOficialUnidadeOperacional,
                    self.chaveUnidadeOperacional, self.cep, self.endereco, self.bairro)


class GrandeUsuario(Base):
    __tablename__ = 'grande_usuario'

    id = Column(Integer, primary_key=True)
    sigla = Column(Text)
    chaveLocalidade = Column(Text)
    nomeOficialLocalidade = Column(Text)
    chaveBairro = Column(Text)
    nomeOficialBairro = Column(Text)
    chaveGrandeUsuario = Column(Text)
    nomeOficialGrandeBairro = Column(Text)
    cep = Column(Text)
    abreviaturaLogradouro = Column(Text)
    endereco_id = Column(Integer, ForeignKey('endereco.id'))
    endereco  = relationship("Endereco", uselist=False, cascade="all") #pra fazer um pra um, mais so um lado sabe do outro.
    localidade_id = Column(Integer, ForeignKey('localidade.id'))
    localidade = relationship("Localidade", uselist=False) #pra fazer um pra um, mais so um lado sabe do outro.
    bairro_id = Column(Integer, ForeignKey('bairro.id'))
    bairro = relationship("Bairro", uselist=False) #pra fazer um pra um, mais so um lado sabe do outro.

    def __init__(self, mapAttrs):
        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "Sigla:{}; ChaveGrandeUsuario:{}; cep:{};Endereco: {}, bairro: {}"\
            .format(self.sigla, self.chaveGrandeUsuario, self.cep, self.endereco, self.bairro)


    class Endereco(Base):
    __tablename__ = 'endereco'

    id = Column(Integer, primary_key=True)

    chave = Column(Text)
    tipoOficialLogradouro = Column(Text)
    preposicao = Column(Text)
    patenteOficialLogradouro = Column(Text)
    chaveLogradouro = Column(Text)
    nomeOficial = Column(Text)
    numeroLote = Column(Text)
    nomeComplemento1 = Column(Text)
    numeroComplemento1 = Column(Text)
    nomeComplemento2 = Column(Text)
    numeroComplemento2 = Column(Text)
    tipoOficial = Column(Text)
    numero = Column(Text)

    def __init__(self, mapAttrs):
        if mapAttrs:
            self.__dict__.update(mapAttrs)

    def __repr__(self):
        return "NomeOficial:{}; Chave:{}"\
            .format(self.nomeOficial, self.chave)
