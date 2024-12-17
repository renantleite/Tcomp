from collections import deque, defaultdict
# todo AFD tem estado , alfabeto , transições , estado inicial , e estados de aceitação

class AFD:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao):
        # Define os atributos de um AFD (Automato Finito Determinístico):
        self.estados = estados  # Lista de estados do AFD.
        self.alfabeto = alfabeto  # Conjunto de símbolos aceitos pelo AFD.
        self.transicoes = transicoes  # Dicionário que mapeia (estado, símbolo) -> próximo estado.
        self.estado_inicial = estado_inicial  # Estado inicial do AFD.
        self.estados_aceitacao = estados_aceitacao  # Conjunto de estados finais ou de aceitação.

# Função que converte um AFN (Automato Finito Não-Determinístico) para um AFD.

def afn_para_afd(afn):
    # Inicializa os componentes do AFD.
    estados_afd = []  # Lista para armazenar os estados do AFD.
    transicoes_afd = {}  # Dicionário para armazenar as transições do AFD.

    # O estado inicial do AFD é um conjunto contendo apenas o estado inicial do AFN por isso o uso de frozenset ao inves de set.
    estado_inicial_afd = frozenset({afn.estado_inicial})

    # Fila para processar os estados .
    fila_estados = deque([estado_inicial_afd])

    # Conjunto para marcar quais estados já foram processados.
    estados_visitados = set()

    # Conjunto para armazenar os estados de aceitação do AFD.
    estados_aceitacao_afd = set()

    # Enquanto houver estados na fila para processar...
    while fila_estados:
        # Remove o próximo estado da fila para processar suas transições.
        estado_atual = fila_estados.popleft()

        # Se o estado já foi processado antes, pula para o próximo.
        if estado_atual in estados_visitados:
            continue

        # Marca o estado atual como visitado.
        estados_visitados.add(estado_atual)

        # Adiciona o estado atual à lista de estados do AFD.
        estados_afd.append(estado_atual)

        # Verifica se o estado atual contém algum estado de aceitação do AFN.
        # Se sim, adiciona o estado atual à lista de estados de aceitação do AFD.
        if any(estado in afn.estados_aceitacao for estado in estado_atual):
            estados_aceitacao_afd.add(estado_atual)

        # Para cada símbolo no alfabeto do AFN, calcula o próximo estado no AFD.
        for simbolo in afn.alfabeto:
            proximo_estado = set()  # Inicializa um conjunto vazio para o próximo estado.

            # Para cada estado no estado atual, adiciona os estados alcançáveis pelo símbolo.(E-FECHO)
            for estado in estado_atual:
                proximo_estado.update(afn.transicoes.get((estado, simbolo), set()))

            # Converte o próximo estado para um conjunto imutável (frozenset).
            proximo_estado = frozenset(proximo_estado)

            # Adiciona a transição ao dicionário de transições do AFD.
            transicoes_afd[(estado_atual, simbolo)] = proximo_estado

            # Se o próximo estado não for vazio e ainda não foi visitado, adiciona à fila.
            if proximo_estado and proximo_estado not in estados_visitados:
                fila_estados.append(proximo_estado)

    # Retorna o AFD criado com todos os seus componentes.
    return AFD(estados_afd, afn.alfabeto, transicoes_afd, estado_inicial_afd, estados_aceitacao_afd)

def complement_AFD(dfa):
    # Inverter os estados de aceitação

    dfa_states_set = set(dfa.estados)  # Garantindo que seja um conjunto
    dfa_accept_states_set = set(dfa.estados_aceitacao)
    novos_estados_aceitos = dfa_states_set - dfa_accept_states_set

    # Criar um novo DFA com os estados de aceitação invertidos
    complement_AFD = AFD(dfa.estados, dfa.alfabeto, dfa.transicoes, dfa.estado_inicial, novos_estados_aceitos)
    return complement_AFD

# Função para exibir os detalhes de um AFD.

def imprimir_afd(afd):
    print("\nEstados do AFD:", [set(estado) for estado in afd.estados])  # Mostra os estados do AFD.
    print("Estado inicial:", set(afd.estado_inicial))  # Mostra o estado inicial do AFD.
    print("Estados finais:", [set(estado) for estado in afd.estados_aceitacao])  # Mostra os estados de aceitação.

    print("Transições:")
    for (estado, simbolo), proximo_estado in afd.transicoes.items():
        # Exibe cada transição no formato: {estado} -- símbolo do alfabeto --> {próximo estado}.
        print(f"{set(estado)} -- {simbolo} --> {set(proximo_estado)}")

# Função para simular uma cadeia de entrada no AFD e exibir as transições realizadas.

def inverter_dfa(dfa):
    transicoes_invertidas = defaultdict(set)
    for (estado_origem, simbolo), estado_destino in dfa.transicoes.items():
        transicoes_invertidas[(estado_destino, simbolo)].add(estado_origem)

    novos_estados_iniciais = dfa.estados_aceitacao
    novos_estados_aceitacao = {dfa.estado_inicial}

    # Considera a criação de um NFA
    nfa_invertido = AFD(
        dfa.estados, dfa.alfabeto, transicoes_invertidas, novos_estados_iniciais, novos_estados_aceitacao
    )
    return nfa_invertido

def simular_afd_com_transicoes(afd, cadeia):
    estado_atual = afd.estado_inicial  # Começa no estado inicial do AFD.
    transicoes_realizadas = []  # Lista para registrar as transições realizadas.

    # Percorre cada símbolo da cadeia de entrada.
    for simbolo in cadeia:
        # Obtém o próximo estado a partir do estado atual e do símbolo.
        proximo_estado = afd.transicoes.get((estado_atual, simbolo), None)

        # Se não houver transição válida, a cadeia é rejeitada.
        if proximo_estado is None:
            return False, transicoes_realizadas

        # Registra a transição realizada.
        transicoes_realizadas.append((estado_atual, simbolo, proximo_estado))

        # Atualiza o estado atual para o próximo estado.
        estado_atual = proximo_estado

    # Verifica se o estado final é de aceitação.
    cadeia_aceita = estado_atual in afd.estados_aceitacao
    return cadeia_aceita, transicoes_realizadas
