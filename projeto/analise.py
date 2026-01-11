import matplotlib.pyplot as plt
import numpy as np
from simulacao import ClinicaEngine

def plot_dashboard(res):
    if not res['hist_fila']:
        pass
    else:
        plt.figure(figsize=(10, 8))
        
        # Gráfico 1: Fila
        plt.subplot(2, 1, 1)
        t, f = zip(*res['hist_fila'])
        plt.plot(t, f, color='orange', label='Fila Total')
        plt.title("Evolução da Fila de Espera")
        plt.xlabel("Tempo (min)")
        plt.ylabel("Pessoas")
        plt.grid(True, alpha=0.3)
        plt.legend()

        # Gráfico 2: Ocupação
        plt.subplot(2, 1, 2)
        t_o, o = zip(*res['hist_ocupacao'])
        plt.plot(t_o, o, color='green', label='% Ocupação')
        plt.title("Taxa de Ocupação dos Médicos")
        plt.xlabel("Tempo (min)")
        plt.ylabel("%")
        plt.ylim(0, 105)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show(block=False)

        plot_pizza_especialidade(res)

def plot_sensibilidade(config_base):
    taxas = range(10, 31, 2)
    medias_fila = []

    print("A calcular análise de sensibilidade...")
    for t in taxas:
        sim = ClinicaEngine(
            config_base['medicos'], t, config_base['tempo'], 
            config_base['dist'], config_base['duracao']
        )
        r = sim.executar()
        # Média ponderada da fila
        if r['hist_fila']:
            vals = [x[1] for x in r['hist_fila']]
            medias_fila.append(np.mean(vals))
        else:
            medias_fila.append(0)

    plt.figure("Análise de Sensibilidade")
    plt.plot(taxas, medias_fila, marker='o', color='red')
    plt.title("Impacto da Taxa de Chegada no Tamanho da Fila")
    plt.xlabel("Taxa de Chegada (doentes/hora)")
    plt.ylabel("Tamanho Médio da Fila")
    plt.grid(True)
    plt.show(block=False)

def plot_pizza_especialidade(res):
    # Verifica se existe o dado de contagem
    if 'contagem_especialidade' not in res:
        print("Não há dados de especialidade para pizza.")
    else:
        dados = res['contagem_especialidade']
        labels = list(dados.keys())
        valores = list(dados.values())

        if sum(valores) == 0:
            print("Nenhum paciente atendido para gerar pizza.")
        else:
            # Criar gráfico de pizza
            plt.figure("Distribuição por Especialidade", figsize=(6,6))
            plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#3498db','#2ecc71','#f1c40f','#e74c3c','#9b59b6'])
            plt.title("Distribuição de Pacientes por Especialidade")
            plt.axis('equal')  # Para círculo perfeito
            plt.show(block=False)



