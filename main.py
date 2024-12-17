from file_parser import read_nfa_and_input_string_from_file, salvar_afd_em_arquivo
from dfa import afn_para_afd, imprimir_afd, simular_afd_com_transicoes, complement_AFD,inverter_dfa


def main():
    # Solicita o nome do arquivo com o AFN
    filename = input("Digite o nome do arquivo com o AFN (por exemplo, 'AFN.txt'): ")

    # Lê o AFN e a cadeia de entrada do arquivo
    nfa, input_string = read_nfa_and_input_string_from_file(filename)
    if input_string is None:
        print("Erro: Nenhuma cadeia encontrada no arquivo.")
        return

    # Converte o AFN para AFD
    dfa = afn_para_afd(nfa)

    # Salva o AFD original em um arquivo
    salvar_afd_em_arquivo(dfa, "afd_original.txt")

    # Cria o complemento do AFD
    complement_AFD_print = complement_AFD(dfa)

    # Salva o complemento do AFD em um arquivo
    salvar_afd_em_arquivo(complement_AFD_print, "afd_complemento.txt")

    # Cria o AFD invertido
    afd_invertido = inverter_dfa(dfa)

    # Salva o AFD invertido em um arquivo
    salvar_afd_em_arquivo(afd_invertido, "afd_invertido.txt")



    # Simula o AFD com a cadeia fornecida
    resultado, transicoes = simular_afd_com_transicoes(dfa, input_string)

    # Exibe o resultado da simulação
    if resultado:
        print(f"A cadeia '{input_string}' foi aceita pelo AFD!")
    else:
        print(f"A cadeia '{input_string}' foi rejeitada pelo AFD!")


if __name__ == "__main__":
    main()
