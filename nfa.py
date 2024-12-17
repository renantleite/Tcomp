class NFA:
    # todo NFA tem estado , alfabeto , transições , estado inicial , e estados de aceitação
    def __init__(self, estado, alfabeto, transicoes, estado_inicial, estados_aceitacao ):
        self.estado = estado
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao  = estados_aceitacao