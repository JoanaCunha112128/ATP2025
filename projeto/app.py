"""
Interface Gráfica Corrigida
"""
import FreeSimpleGUI as sg
import simulacao
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'
import json
import os

sg.theme("DarkBlue14")

def mostrar_dashboard(res):
    try:
        plt.close('all')
        plt.style.use('seaborn-v0_8-darkgrid') 
        plt.figure("Resultados", figsize=(10, 6))

        plt.subplot(2, 1, 1)
        x, y = res['plot_fila']
        plt.step(x, y, where='post', color='#00d2d3', linewidth=2, label='Fila')
        plt.fill_between(x, y, step='post', color='#00d2d3', alpha=0.2)
        plt.title(f"Fila (Máx: {res['max_fila']})")
        plt.legend()

        plt.subplot(2, 1, 2)
        x2, y2 = res['plot_ocup']
        plt.plot(x2, y2, color='#ff9f43', label='Ocupação Inst.', linewidth=1)
        plt.axhline(y=res['ocupacao_media'], color='red', linestyle='--', label=f'Média Total: {res["ocupacao_media"]:.1f}%')
        plt.title("Ocupação Médica")
        plt.ylim(-5, 105) # Garante que visualmente não passa dos 100
        plt.legend()
        
        plt.tight_layout()
        plt.show(block=False)
    except:
        pass

def mostrar_grafico_sensibilidade(x, y):
    try:
        plt.figure("Stress Test", figsize=(8, 5))
        plt.plot(x, y, color='#ff5252', marker='o')
        plt.title("Sensibilidade da Fila")
        plt.xlabel("Doentes/Hora")
        plt.grid(True)
        plt.tight_layout()
        plt.show(block=False)
    except:
        pass

def mostrar_grafico_pizza(res):
    if 'contagem_especialidade' not in res:
        sg.popup_error("Não há dados de especialidade para gerar gráfico de pizza.")
    else:
        dados = res['contagem_especialidade']
        labels = list(dados.keys())
        valores = list(dados.values())

        if sum(valores) == 0:
            sg.popup_error("Nenhum paciente atendido para gerar gráfico de pizza.")
        else:
            plt.figure("Distribuição por Especialidade", figsize=(6,6))
            cores = ['#3498db','#2ecc71','#f1c40f','#e74c3c','#9b59b6']  # cores para cada especialidade
            plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=140, colors=cores)
            plt.title("Distribuição de Pacientes por Especialidade")
            plt.axis('equal')  # círculo perfeito
            plt.show(block=False)


def main():
    layout_params = [
        [sg.Text("CONFIGURAÇÃO", font=("Arial", 10, "bold"), text_color="#54a0ff")],
        [sg.Text("Pacientes/Hora:", size=(15,1)), sg.Slider((5, 50), 15, orientation='h', size=(25, 15), key='-TAXA-')],
        [sg.Text("Nº Médicos:", size=(15,1)), sg.Spin(list(range(1, 15)), 4, size=(5,1), key='-MEDICOS-')],
        [sg.Text("T. Base (min):", size=(15,1)), sg.Input("15", size=(6,1), key='-TEMPO-')],
        [sg.Text("Distribuição:", size=(15,1)), sg.Combo(["Exponencial", "Normal", "Uniforme"], "Exponencial", key='-DIST-')],
        [sg.HSeparator(pad=(0, 20))],
        [sg.Button("SIMULAR ▶", size=(30, 2), button_color=("white", "#10ac84"), font=("Arial", 10, "bold"))]
    ]

    layout_kpis = [
        [sg.Text("RESULTADOS MÉDIOS", font=("Arial", 10, "bold"), text_color="#54a0ff")],
        [sg.Text("Total Atendidos:", size=(20,1)), sg.Text("0", key='-TOT-', font=("Arial", 10, "bold"))],
        [sg.Text("Espera Média:", size=(20,1)), sg.Text("0.0 m", key='-ESP-', text_color="orange", font=("Arial", 10, "bold"))],
        [sg.Text("Tempo na Clínica:", size=(20,1)), sg.Text("0.0 m", key='-CLINICA-', font=("Arial", 10, "bold"))],
        [sg.Text("Ocupação Média:", size=(20,1)), sg.Text("0.0 %", key='-OCUP-', text_color="green", font=("Arial", 10, "bold"))],
        [sg.Text("Fila Máxima:", size=(20,1)), sg.Text("0", key='-MAXFILA-', font=("Arial", 10, "bold"))],
    ]

    layout_equipa = [
        [sg.Text("Ocupação por Médico", font=("Arial", 11))],
        [sg.Listbox(values=[], size=(55, 10), key='-LISTA-', font=("Consolas", 10))]
    ]

    layout_logs = [
        [sg.Text("Log (Nome | Idade | Pulseira | Esp)", font=("Arial", 11))],
        [sg.Multiline(size=(60, 15), key='-LOG_VIEW-', font=("Consolas", 8), disabled=True, background_color="#222f3e", text_color="#c8d6e5")]
    ]

    layout_stress = [
        [sg.Text("ANÁLISE SENSIBILIDADE", font=("Arial", 12, "bold"), text_color="#ff5252")],
        [sg.Button("EXECUTAR TESTE 📈", size=(30, 2), button_color=("white", "#ff5252"), font=("Arial", 10, "bold"))]
    ]

    layout_relatorio = [
        [sg.Text("RELATÓRIO", font=("Arial", 12, "bold"), text_color="#54a0ff")],
        [sg.Button("📊 Fila & Ocupação", key='-REL_DASH-', size=(30,2))],
        [sg.Button("🥧 Distribuição por Especialidade", key='-REL_PIZZA-', size=(30,2))]
    ]

    layout = [
        [sg.Text("🏥 SIMULADOR CLÍNICO FINAL", font=("Verdana", 14, "bold"), text_color="white", pad=(10,10))],
        [sg.TabGroup([
            [sg.Tab("Controlo", [[sg.Column(layout_params), sg.VSeparator(), sg.Column(layout_kpis)]]),
             sg.Tab("Equipa", layout_equipa),
             sg.Tab("Logs", layout_logs),
             sg.Tab("Stress Test", layout_stress, element_justification='c'),
             sg.Tab("Relatório", layout_relatorio)]
        ], tab_location='topleft', font=("Arial", 10))],
        [
            sg.Text("Pronto.", key='-STATUS-', size=(40,1), relief=sg.RELIEF_SUNKEN, text_color="gray"),
            sg.Push(),
            sg.Button("❌ SAIR", size=(10,1), button_color=("white", "#ee5253"))
        ]
    ]
    
    ultimo_resultado = None

    window = sg.Window("Simulação Biomédica", layout, finalize=True)

    running = True
    while running:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "❌ SAIR"):
            if sg.popup_yes_no("Tem a certeza que quer sair?") == "Yes":
                running = False

        if event == "SIMULAR ▶":
            try:
                window['-STATUS-'].update("A simular...")
                window.refresh()
                
                
            # --- CARREGAR JSON DE FORMA SEGURA (CAMINHO ABSOLUTO) ---
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                JSON_PATH = os.path.join(BASE_DIR, "pessoas.json")

                db = []
                if os.path.exists(JSON_PATH):
                    try:
                        with open(JSON_PATH, "r", encoding="utf-8") as f:
                            db = json.load(f)
                    except Exception as e:
                        print("Erro a ler pessoas.json:", e)
                else:
                    print("pessoas.json NÃO encontrado em:", JSON_PATH)



                cfg = {
                    'taxa_chegada': float(values['-TAXA-']),
                    'num_medicos': int(values['-MEDICOS-']),
                    'tempo_medio': float(values['-TEMPO-']),
                    'distribuicao': values['-DIST-'],
                    'tempo_max': 480
                }
                
                res = simulacao.simular_atendimento(cfg, db)
                ultimo_resultado = res

                window['-TOT-'].update(res['total'])
                window['-ESP-'].update(f"{res['media_espera']:.1f} m")
                window['-CLINICA-'].update(f"{res['media_clinica']:.1f} m")
                window['-OCUP-'].update(f"{res['ocupacao_media']:.1f} %")
                window['-MAXFILA-'].update(res['max_fila'])
                
                window['-LISTA-'].update(res['stats_equipa'])
                
                if os.path.exists("relatorio_final.txt"):
                    with open("relatorio_final.txt","r",encoding="utf-8") as f:
                        window['-LOG_VIEW-'].update(f.read())

                window['-STATUS-'].update("Concluído.")
                
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == '-REL_DASH-' and ultimo_resultado:
            mostrar_dashboard(ultimo_resultado)

        if event == '-REL_PIZZA-' and ultimo_resultado:
            mostrar_grafico_pizza(ultimo_resultado)

        if event == "EXECUTAR TESTE 📈":
            try:
                window['-STATUS-'].update("A testar...")
                window.refresh()
                cfg_base = {
                    'taxa_chegada': 10,
                    'num_medicos': int(values['-MEDICOS-']),
                    'tempo_medio': float(values['-TEMPO-']),
                    'distribuicao': values['-DIST-'],
                    'tempo_max': 480
                }
                x, y = simulacao.realizar_analise_sensibilidade(cfg_base)
                window['-STATUS-'].update("Teste terminado.")
                mostrar_grafico_sensibilidade(x, y)
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

    window.close()

if __name__ == "__main__":
    main()