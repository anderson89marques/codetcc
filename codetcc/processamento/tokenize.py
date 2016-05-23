from codetcc.processamento.constantes import CABECALHO


def generateTokens(linha, mapa):
    init = 0
    fim = 0
    result = {}
    list_attr = []
    for tipo in mapa.keys():
        if linha.startswith(tipo) and tipo != CABECALHO: #deu um pequeno problema na leitura do cabeçalho que ainda precisa ser corrigido
            list_attr = mapa[tipo]
            init = len(tipo) #tamanho do tipo registro. Como o tipo já é identificado é preciso ler a linha a partir dele
            break
    for attr in list_attr:
        len_attr = list(attr.values())[0]
        fim = init + len_attr
        result[list(attr.keys())[0]] = linha[init:fim]
        init = fim
    print
    return result
