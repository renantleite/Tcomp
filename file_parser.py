from nfa import NFA
from dfa import afn_para_afd, imprimir_afd, simular_afd_com_transicoes, complement_AFD,inverter_dfa
def read_nfa_and_input_string_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    states = set()
    alphabet = set()
    transitions = {}
    start_state = None
    accept_states = set()
    input_string = None
    reading_transitions = False

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):  # Ignorar linhas em branco ou comentários
            continue

        if line.startswith("Q:"):
            states = set(line.split(":")[1].replace(',', ' ').split())
        elif line.startswith("E:"):
            alphabet = set(line.split(":")[1].replace(',', ' ').split())
        elif line.startswith("Transicoes:"):
            reading_transitions = True
        elif line.startswith("q0:"):
            start_state = line.split(":")[1].strip()
        elif line.startswith("F:"):
            accept_states = set(line.split(":")[1].replace(',', ' ').split())
        elif line.startswith("W:"):
            input_string = line.split(":")[1].strip()
        elif reading_transitions:
            try:
                # Separar o estado de origem e o símbolo
                parts = line.split()
                from_state = parts[0]
                symbol = parts[1]
                # Separar os estados de destino pela vírgula
                to_states_set = set(parts[2].split(','))
                transitions[(from_state, symbol)] = to_states_set
            except ValueError:
                print(f"A transição '{line}' está mal formatada e foi ignorada.")
                continue

    return NFA(states, alphabet, transitions, start_state, accept_states), input_string
def salvar_afd_em_arquivo(afd, nome_arquivo):
    # Função que salva o AFD em um arquivo.
    with open(nome_arquivo, 'w') as f:
        f.write("Estados do AFD: {}\n".format([set(estado) for estado in afd.estados]))
        f.write("Estado inicial: {}\n".format(set(afd.estado_inicial)))
        f.write("Estados finais: {}\n".format([set(estado) for estado in afd.estados_aceitacao]))
        f.write("Transicoes:\n")
        for (estado, simbolo), proximo_estado in afd.transicoes.items():
            f.write(f"{set(estado)} -- {simbolo} --> {set(proximo_estado)}\n")
    print(f"Resultado salvo em {nome_arquivo}")