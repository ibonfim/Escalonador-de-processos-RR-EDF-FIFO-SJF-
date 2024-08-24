import copy
import matplotlib.pyplot as plt


class Processo:
    def __init__(
        self,
        id,
        tempo_chegada,
        tempo_execucao,
        deadline,
        quantum_sistema,
        sobrecarga_sistema,
    ):
        self.id = id
        self.tempo_chegada = tempo_chegada
        self.tempo_execucao = tempo_execucao
        self.deadline = deadline
        self.quantum_sistema = quantum_sistema
        self.sobrecarga_sistema = sobrecarga_sistema
        self.tempo_restante = tempo_execucao
        self.contador_quantum = 0
        self.historico = []

    def __repr__(self):
        return (
            f"Processo(id={self.id}, tempo_chegada={self.tempo_chegada}, "
            f"tempo_execucao={self.tempo_execucao}, deadline={self.deadline}, "
            f"tempo_restante={self.tempo_restante}"
        )


def fifo(processos: Processo):
    tempo_atual = 0
    resultados = []
    turnaround_total = 0
    # Ordena os processos pelo tempo de chegada
    processos_ordenados = sorted(processos, key=lambda p: p.tempo_chegada)

    for processo in processos_ordenados:
        # Atualiza o tempo atual se for menor que o tempo de chegada do process
        if tempo_atual < processo.tempo_chegada:
            tempo_atual = processo.tempo_chegada

        # Calcula o tempo de espera e o turnaround do processo
        tempo_espera = tempo_atual - processo.tempo_chegada
        turnaround_processo = tempo_espera + processo.tempo_execucao
        turnaround_total += turnaround_processo

        # Adiciona os resultados à lista
        resultados.append({ 
            'id': processo.id,
            'inicio': processo.tempo_chegada,
            'fim':processo.tempo_execucao,
            'tempo_espera': tempo_espera+processo.tempo_chegada,
            'turnaround': turnaround_processo,
             'Turnaround_Medio': turnaround_total / len(processos)

    
        })
        
        print(
            f"Executando {processo} tempo_espera {tempo_espera} turnaround_processo = {turnaround_processo}"
        )

        # Atualiza o tempo atual após a execução do processo
        tempo_atual += processo.tempo_execucao
    #resultados.append(turnaround_total / len(processos))
    print(f"turnaround_total = {turnaround_total}")

    print(resultados)
    return resultados


def sjf(processos):
    copia_processos = copy.deepcopy(processos)
    tempo_atual = 0
    resultados = []
    list_turnaround = []
    turnaround_total = 0
    

    while copia_processos:
        # Filtra processos que já chegaram e estão prontos para execução
        processos_prontos = [
            p for p in copia_processos if p.tempo_chegada <= tempo_atual
        ]
        if not processos_prontos:
            # Se nenhum processo está pronto, avança o tempo para o próximo processo que chegará
            tempo_proximo = min(p.tempo_chegada for p in copia_processos)
            tempo_atual = tempo_proximo
            continue

        # Seleciona o processo com o menor tempo de execução entre os prontos
        processo = min(processos_prontos, key=lambda p: p.tempo_execucao)

        # Remove o processo selecionado da lista
        copia_processos.remove(processo)

        # Calcula o tempo de espera e turnaround
        tempo_espera = tempo_atual - processo.tempo_chegada
        turnaround_processo = tempo_espera + processo.tempo_execucao
        turnaround_total += turnaround_processo
        list_turnaround.append(turnaround_processo)
        resultados.append({ 
            'id': processo.id,
            'inicio': processo.tempo_chegada,
            'fim':processo.tempo_execucao,
            'tempo_espera': tempo_espera+processo.tempo_chegada,
            'turnaround': turnaround_processo,
             'Turnaround_Medio': turnaround_total / len(processos)

    
        })
        

        # Imprime informações do processo
        print(
            f"Executando {processo} tempo_espera {tempo_espera} turnaround_processo = {turnaround_processo}"
        )

        # Atualiza o tempo atual após a execução do processo
        tempo_atual += processo.tempo_execucao
    #resultados.append(turnaround_total / qtdProcessos)
    print(resultados)
    return resultados


def round_robin(processos):
    copia_processos = copy.deepcopy(processos)
    tempo_atual = 0
    turnaround_total = 0
    resultados = []
    fila_processos = []

    dados_processos = {p.id: {} for p in processos}
    
    while copia_processos or fila_processos:
        # Adiciona processos que chegaram ao tempo_atual à fila de processos
        processos_chegaram = [
            p for p in copia_processos if p.tempo_chegada <= tempo_atual
        ]
        for p in processos_chegaram:
            fila_processos.append(p)
            copia_processos.remove(p)

        if not fila_processos:
            if copia_processos:
                # Se não há processos prontos, avance o tempo para o próximo processo que chegará
                tempo_proximo = min(p.tempo_chegada for p in copia_processos)
                tempo_atual = tempo_proximo
                continue
            else:
                break

        # Seleciona o próximo processo da fila de processos prontos
        processo_atual = fila_processos.pop(0)
        # Executa o processo atual por até o quantum ou até terminar
        tempo_execucao = min(processo_atual.quantum_sistema, processo_atual.tempo_restante)
        dados_processos[processo_atual.id]['quantum_sistema'] =processo_atual.quantum_sistema
        processo_atual.tempo_restante -= tempo_execucao
        tempo_atual += tempo_execucao
        
        if 'inicio' not in dados_processos[processo_atual.id]:
            dados_processos[processo_atual.id]['inicio'] = tempo_atual - tempo_execucao
        dados_processos[processo_atual.id]['fim'] = tempo_atual
        dados_processos[processo_atual.id]['id'] = processo_atual.id
        
        if processo_atual.tempo_restante > 0:
            # Se o processo não terminou, coloque-o de volta no final da fila de prontos
            fila_processos.append(processo_atual)
            tempo_atual += processo_atual.sobrecarga_sistema
            dados_processos[processo_atual.id]['sobrecarga'] =processo_atual.sobrecarga_sistema

        # Se o processo terminou, calcula os tempos de turnaround e espera
        if processo_atual.tempo_restante == 0:
            turnaround_processo = tempo_atual - processo_atual.tempo_chegada
            tempo_espera = turnaround_processo - processo_atual.tempo_execucao
            turnaround_total += turnaround_processo
            
            # Atualiza o dicionário do processo com os dados finais
            dados_processos[processo_atual.id]['tempo_espera'] = tempo_espera
            dados_processos[processo_atual.id]['turnaround'] = turnaround_processo
            dados_processos[processo_atual.id]['Turnaround_Medio'] = turnaround_total / len(processos)
            
            
            # Adiciona os dados do processo aos resultados
            resultados.append(dados_processos[processo_atual.id])

            print(f"Processo {processo_atual.id}: tempo_espera = {tempo_espera}, turnaround_processo = {turnaround_processo}")
    
    # Adiciona a média do turnaround aos resultados
    media_turnaround = turnaround_total / len(processos) if processos else 0

    print("Resultados:", resultados)
    return resultados

def edf(processos):
    copia_processos = copy.deepcopy(processos)
    tempo_atual = 0
    turnaround_total = 0
    tempo_espera = 0
    resultados = []
    lista_com_dados = []
    lista_aux = []

    while copia_processos:
        # Filtra processos que já chegaram e estão prontos para execução
        processos_prontos = [
            p for p in copia_processos if p.tempo_chegada <= tempo_atual
        ]

        if not processos_prontos:
            # Se nenhum processo está pronto, avança o tempo para o próximo processo que chegará
            if copia_processos:
                tempo_proximo = min(p.tempo_chegada for p in copia_processos)
                tempo_atual = tempo_proximo
                continue
            else:
                break
        # Seleciona o processo com o menor tempo de deadline entre os prontos
        processo = min(processos_prontos, key=lambda p: p.deadline)

        if processo.tempo_restante == 0:
            processo.tempo_restante = processo.tempo_execucao
        inicio_execucao = tempo_atual
        # Decrementa do tempo restante
        while processo.tempo_restante > 0:
            processo.tempo_restante -= 1
            processo.contador_quantum += 1
            tempo_atual += 1

            processos_prontos = [
                p for p in copia_processos if p.tempo_chegada <= tempo_atual
            ]

            if processos_prontos:
                processo_aux = min(processos_prontos, key=lambda p: p.deadline)
                if (
                    tempo_atual >= processo_aux.tempo_chegada
                    and processo.deadline > processo_aux.deadline
                ):

                    lista_aux.append(processo)
                    copia_processos.remove(processo)
                    tempo_atual += processo.sobrecarga_sistema

                    break
            # checa se o processo atingiu o quantum
            if (
                processo.contador_quantum == processo.quantum_sistema
                and processo_aux.tempo_restante != 0
            ):
                tempo_atual += processo.sobrecarga_sistema
                processo.contador_quantum = 0

                break

            else:
                # Caso não haja processos prontos, continue executando o processo atual
                continue

        # Remove o processo selecionado da lista
        if processo.tempo_restante == 0:
            copia_processos.remove(processo)

            turnaround_processo = tempo_atual - processo.tempo_chegada
            tempo_espera = turnaround_processo - processo.tempo_execucao
            turnaround_total += turnaround_processo
            resultados.append(
                (
                    f"processo_id= {processo.id},tempo_espera= {tempo_espera}, turnaround_processo = {turnaround_processo}"
                )
            )

            # print(tempo_atual)
            print(
                f"Executando {processo} tempo_espera {tempo_espera} turnaround_processo = {turnaround_processo}"
            )

        # Adiciona processos pausados de volta à lista de processos
        copia_processos.extend(lista_aux)
        lista_aux.clear()

    resultados.append(turnaround_total / len(processos))

    print(resultados)
    return resultados


  
def criar_grafico_gantt(resultados ,tempo_total, tipo_escalonador):
    fig, gnt = plt.subplots()

    gnt.set_xlabel('Tempo')
    gnt.set_ylabel('Processos')

    y_ticks = []
    y_labels = []

    for idx, resultado in enumerate(resultados):
        if 'id' in resultado:
            y_ticks.append(10 * (idx + 1))
            y_labels.append(f"Processo {resultado['id']}")
            
            if tipo_escalonador == 1:
                # Adiciona a barra para o tempo de espera (cor azul)
                if resultado['tempo_espera'] > 0:
                    gnt.broken_barh(
                        [(resultado['inicio'], resultado['tempo_espera'])],  # Tempo de espera
                        (10 * idx, 9),
                        facecolor='blue',
                        edgecolor='black'
                    )
                
                # Adiciona a barra para o tempo de execução (cor laranja)
                gnt.broken_barh(
                    [(resultado['tempo_espera'], resultado['fim'] )],  # Tempo de execução
                    (10 * idx, 9),
                    facecolor='orange',
                    edgecolor='black'
                )
            elif tipo_escalonador == 2:
                # Visualiza o tempo de execução (cor laranja)
                gnt.broken_barh(
                    [(resultado['inicio'], resultado['quantum_sistema'])],  # Quantum executado
                    (10 * idx, 9),
                    facecolor='orange',
                    edgecolor='black'
                )

                # Visualiza a sobrecarga (cor cinza)
                if 'sobrecarga' in resultado and resultado['sobrecarga'] > 0:
                    gnt.broken_barh(
                        [(resultado['fim'], resultado['sobrecarga'])],  # Sobrecarga
                        (10 * idx, 9),
                        facecolor='gray',
                        edgecolor='black'
                    )
            
            
            elif tipo_escalonador == 4:
              
                # Adiciona a barra para o tempo de execução (cor laranja ou vermelha para estourar o deadline)
                gnt.broken_barh(
                    [(resultado['inicio'], resultado['fim'] - resultado['inicio'])],
                    (10 * idx, 9),
                    facecolor='orange' if not resultado.get('estouro_deadline', False) else 'red',
                    edgecolor='black'
                )
                
                # Adiciona linha vertical para processos que estouraram o deadline
                if resultado.get('estouro_deadline', False):
                    gnt.axvline(x=resultado['fim'], color='blue', linestyle='--', linewidth=1)
    gnt.set_yticks(y_ticks)
    gnt.set_yticklabels(y_labels)
    
    x_ticks = range(0, tempo_total + 1)
    gnt.set_xticks(x_ticks)
    

    gnt.grid(True)
    plt.show()


    
   

def main():
    quantum_sistema = 2
    sobrecarga_sistema = 1

    # lista_processos = [
    #     Processo(1, 5, 1, 6, quantum_sistema, sobrecarga_sistema),
    #     Processo(2, 1, 5, 12, quantum_sistema, sobrecarga_sistema),
    #     Processo(3, 2, 7, 8, quantum_sistema, sobrecarga_sistema),
    #     Processo(4, 3, 3, 4, quantum_sistema, sobrecarga_sistema),
    # ]
    # lista_processos = [
    #     Processo(1, 0, 15, 45, quantum_sistema, sobrecarga_sistema),
    #     Processo(2, 3, 4, 9, quantum_sistema, sobrecarga_sistema),
    #     Processo(3, 6, 10, 22, quantum_sistema, sobrecarga_sistema),
    #     Processo(4, 9, 10, 35, quantum_sistema, sobrecarga_sistema),
    # ]

    lista_processos = [
        Processo(1, 0, 4, 7, quantum_sistema, sobrecarga_sistema),
        Processo(2, 2, 2, 5, quantum_sistema, sobrecarga_sistema),
        Processo(3, 4, 1, 8, quantum_sistema, sobrecarga_sistema),
        Processo(4, 6, 3, 10, quantum_sistema, sobrecarga_sistema),
    ]
    # self, id, tempo_chegada, tempo_execucao, deadline, quantum_sistema, sobrecarga_sistema, paginas
    # lista_processos = [
    #     Processo(1, 0, 1, 6, quantum_sistema, sobrecarga_sistema),
    #     Processo(2, 0, 5, 12, quantum_sistema, sobrecarga_sistema),
    #     Processo(3, 0, 7, 8, quantum_sistema, sobrecarga_sistema),
    #     Processo(4, 0, 3, 4, quantum_sistema, sobrecarga_sistema),
    # ]

    # print("FIFO:")
    # fifo_resultado=fifo(lista_processos[:])
    # criar_grafico_gantt( fifo_resultado,60,1)
    
    # print("\nSJF:")
    # sjf_resultado=sjf(lista_processos[:])
    # criar_grafico_gantt(sjf_resultado,60,1)

    print("\nRound Robin:")
    rr_resultado=round_robin(lista_processos)
    criar_grafico_gantt(rr_resultado,90,2)

    # print("\nEDF:")
    # edf(lista_processos[:])
    # criar_grafico_gantt(rr_resultado,60,1)
    # criar_grafico_gantt(lista_processos, 20)
    # criar_grafico_memoria(memoria.ram, memoria.disco)


if __name__ == "__main__":
    main()
