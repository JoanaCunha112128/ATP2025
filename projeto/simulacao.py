"""
Módulo: simulacao.py
Baseado no código base.
CORREÇÃO CRÍTICA: Pediatra nunca atende adultos.
"""
import random
import numpy as np

# --- CONSTANTES ---
CHEGADA = 1
SAIDA = 2

VERMELHA = 0
AMARELA = 1
VERDE = 2
CORES_STR = {0: "Vermelha", 1: "Amarela", 2: "Verde"}

# --- ESPECIALIDADES & TEMPOS ---
PROB_ESPECIALIDADES = {
    "GERAL": 0.40,
    "INTERN": 0.30,
    "ORTO": 0.15,
    "CARD": 0.10,
    "PED": 0.05
}

TEMPO_MEDIO_ESP = {
    "GERAL": 10,
    "INTERN": 15,
    "PED": 15,
    "ORTO": 20,
    "CARD": 25
}

# Contador de pacientes por especialidade
global contagem_especialidade
contagem_especialidade = {
    "GERAL": 0,
    "INTERN": 0,
    "ORTO": 0,
    "CARD": 0,
    "PED": 0
}


# --- FUNÇÕES BASE (DO STOR) ---
def e_tempo(ev): 
    resultado = ev[0]
    return resultado

def e_tipo(ev): 
    resultado = ev[1]
    return resultado

def e_doente(ev): 
    resultado = ev[2]
    return resultado

def enqueue(queue, evento):
    queue.append(evento)
    queue.sort(key=e_tempo)
    resultado = queue
    return resultado

def dequeue(queue):
    resultado_evento = None
    resultado_queue = []
    if not queue:
        pass
    else:
        resultado_evento = queue[0]
        resultado_queue = queue[1:]
    return resultado_evento, resultado_queue

# Medico: [id, ocupado, doente, tempo_ocup, inicio_ult, especialidade]
def mOcupa(medico):
    medico[1] = True
    resultado = medico
    return resultado

def mLivre(medico):
    medico[1] = False
    resultado = medico
    return resultado

def mInicioConsulta(medico, tempo):
    medico[4] = tempo
    resultado = medico
    return resultado

def mDoenteCorrente(medico, doente):
    medico[2] = doente
    resultado = medico
    return resultado

def m_doente_corrente(medico):
    resultado = medico[2]
    return resultado

def mTempoOcupado(medico, tempo):
    medico[3] = tempo
    resultado = medico
    return resultado

def m_total_tempo_ocupado(medico):
    resultado = medico[3]
    return resultado

def m_inicio_ultima_consulta(medico):
    resultado = medico[4]
    return resultado

def m_especialidade(medico):
    resultado = medico[5]
    return resultado

def procuraMedico(medicos, especialidade_doente):
    """
    Lógica Rigorosa:
    1. Se o doente for PED, procura PED ou GERAL.
    2. Se o doente for ADULTO, procura a sua esp, ou GERAL, ou QUALQUER UM (EXCETO PEDIATRA).
    """
    resultado = None
    
    # CASO 1: É CRIANÇA?
    if especialidade_doente == "PED":
        # Tenta Pediatra
        medico_encontrado = None
        for m in medicos:
            if not m[1] and m[5] == "PED":
                medico_encontrado = m
        
        if medico_encontrado is None:
            # Tenta Geral
            for m in medicos:
                if not m[1] and m[5] == "GERAL":
                    medico_encontrado = m
        
        resultado = medico_encontrado
    else:
        # CASO 2: É ADULTO (Não pode ir ao Pediatra)
        
        # 2.1 Tenta Especialista Exato
        medico_encontrado = None
        for m in medicos:
            if not m[1] and m[5] == especialidade_doente:
                medico_encontrado = m
        
        if medico_encontrado is None:
            # 2.2 Tenta Geral
            for m in medicos:
                if not m[1] and m[5] == "GERAL":
                    medico_encontrado = m
        
        if medico_encontrado is None:
            # 2.3 Tenta Qualquer Outro (EXCETO PEDIATRA)
            for m in medicos:
                # Se estiver livre E NÃO FOR PEDIATRA
                if not m[1] and m[5] != "PED":
                    medico_encontrado = m
        
        resultado = medico_encontrado
    
    return resultado

# --- LÓGICA DE NEGÓCIO ---

def atribuir_pulseira(idade):
    cores = [VERDE, AMARELA, VERMELHA]
    pesos = [0.3, 0.5, 0.2] if idade >= 70 else [0.7, 0.2, 0.1]
    resultado = random.choices(cores, weights=pesos, k=1)[0]
    return resultado

def atribuir_especialidade(idade):
    # Se for menor de 18, É SEMPRE PED.
    resultado = None
    if idade < 18:
        resultado = "PED"
    else:
        # Se for maior de 18, NUNCA É PED.
        esps_adulto = ["GERAL", "INTERN", "ORTO", "CARD"]
        pesos_adulto = [0.45, 0.35, 0.15, 0.05]
        resultado = random.choices(esps_adulto, weights=pesos_adulto, k=1)[0]
    return resultado

def gera_intervalo_tempo_chegada(taxa):
    resultado = np.random.exponential(60.0 / taxa)
    return resultado

def gera_tempo_consulta(media_base, tipo="Exponencial"):
    resultado = None
    if tipo == "Normal":
        resultado = max(2.0, np.random.normal(media_base, 4.0))
    elif tipo == "Uniforme":
        resultado = np.random.uniform(media_base * 0.8, media_base * 1.2)
    else:
        resultado = np.random.exponential(media_base)
    return resultado

# --- SIMULAÇÃO ---
def simular_atendimento(config, db_pessoas=None):
    TAXA_CHEGADA = config['taxa_chegada']
    NUM_MEDICOS = config['num_medicos']
    TEMPO_SIMULACAO = config['tempo_max']
    TIPO_DIST = config['distribuicao']

    # Gerar Médicos (Garante que há pelo menos 1 de cada se houver medicos suficientes)
    lista_fixa = ["GERAL", "INTERN", "ORTO", "CARD", "PED"]
    medicos = []
    for i in range(NUM_MEDICOS):
        esp = lista_fixa[i % len(lista_fixa)]
        # [id, ocupado, doente, tempo_ocup, inicio_ult, especialidade, n_consultas]
        medicos.append([f"M{i+1}", False, None, 0.0, 0.0, esp, 0])

    # Pré-geração de chegadas
    tempo_atual = 0.0
    contadorDoentes = 1
    queueEventos = [] 
    queue = [] 

    t = 0.0
    while t < TEMPO_SIMULACAO:
        t += gera_intervalo_tempo_chegada(TAXA_CHEGADA)
        
        # Leitura do JSON Segura
        nome = None
        idade = None
        if db_pessoas:
            p = random.choice(db_pessoas)
            nome = str(p["nome"])
            idade = int(p.get("idade", 30))
        else:
            nome = f"Utente {contadorDoentes}"
            idade = 30

        
        prio = atribuir_pulseira(idade)
        esp_doente = atribuir_especialidade(idade)
        
        doente = {
            'id': f"d{contadorDoentes}",
            'nome': nome,
            'idade': idade,
            'chegada': t,
            'prioridade': prio,
            'cor': CORES_STR[prio],
            'esp': esp_doente,
            'ordem': contadorDoentes
        }
        
        queueEventos = enqueue(queueEventos, (t, CHEGADA, doente))
        contadorDoentes += 1

    # Variáveis de Controlo
    dados_fila = [(0.0, 0)]
    dados_ocupacao = []
    log_auditoria = []
    tempos_espera = []
    tempos_clinica = []
    tempos_consulta = []
    max_fila = 0
    doentes_atendidos = 0

    # LOOP PRINCIPAL
    while queueEventos != []:
        evento, queueEventos = dequeue(queueEventos)
        tempo_atual = e_tempo(evento)
        tipo = e_tipo(evento)
        doente_atual = e_doente(evento)

        if len(queue) > max_fila:
            max_fila = len(queue)
        dados_fila.append((tempo_atual, len(queue)))

        if tipo == CHEGADA:
            medico_livre = procuraMedico(medicos, doente_atual['esp'])
            
            if medico_livre:
                # Atende Já
                medico_livre = mOcupa(medico_livre)
                medico_livre = mInicioConsulta(medico_livre, tempo_atual)
                medico_livre = mDoenteCorrente(medico_livre, doente_atual)
                
                t_base = TEMPO_MEDIO_ESP.get(doente_atual['esp'], 15)
                duracao = gera_tempo_consulta(t_base, TIPO_DIST)
                
                queueEventos = enqueue(queueEventos, (tempo_atual + duracao, SAIDA, doente_atual))
                tempos_espera.append(0.0)
                log_auditoria.append(f"CHEGADA: {doente_atual['nome']} ({doente_atual['idade']}) | {doente_atual['cor']} | {doente_atual['esp']} -> Atendido {medico_livre[0]}")
            else:
                # Fila
                queue.append(doente_atual)
                queue.sort(key=lambda x: (x['prioridade'], x['ordem']))
                log_auditoria.append(f"FILA: {doente_atual['nome']} ({doente_atual['idade']}) | {doente_atual['cor']} | {doente_atual['esp']} -> Aguarda")

        elif tipo == SAIDA:
            doentes_atendidos += 1
            
            # Libertar
            medico_libertado = None
            for m in medicos:
                if m_doente_corrente(m) == doente_atual:
                    inicio = m_inicio_ultima_consulta(m)
                    duracao_real = tempo_atual - inicio
                    
                    m = mTempoOcupado(m, m_total_tempo_ocupado(m) + duracao_real)
                    m = mLivre(m)
                    m = mDoenteCorrente(m, None)
                    m[6] += 1  # incrementa número de consultas

                    tempos_clinica.append(tempo_atual - doente_atual['chegada'])
                    tempos_consulta.append(duracao_real)
                    medico_libertado = m
            
        # Atualizar contagem por especialidade
            esp = doente_atual['esp']
            contagem_especialidade[esp] += 1

            
            medico_livre = None
          
            if queue:
                prox_cand = queue[0]
              
                medico_livre = procuraMedico(medicos, prox_cand['esp'])

            if queue and medico_livre:
                prox = queue.pop(0)
                medico_livre = mOcupa(medico_livre)
                medico_livre = mInicioConsulta(medico_livre, tempo_atual)
                medico_livre = mDoenteCorrente(medico_livre, prox)
                
                espera = tempo_atual - prox['chegada']
                tempos_espera.append(espera)
                t_base = TEMPO_MEDIO_ESP.get(prox['esp'], 15)
                duracao = gera_tempo_consulta(t_base, TIPO_DIST)
                
                queueEventos = enqueue(queueEventos, (tempo_atual + duracao, SAIDA, prox))
                log_auditoria.append(f"ATENDIMENTO: {prox['nome']} (Esp:{espera:.1f}m) -> {medico_livre[0]}")

        # Gráfico Ocupação
        ocupados = sum(1 for m in medicos if m[1])
        dados_ocupacao.append((tempo_atual, (ocupados/NUM_MEDICOS)*100))

    # --- CORREÇÃO MATEMÁTICA 100% ---
    stats = []
    total_trabalho = 0

    for m in medicos:
        tempo_util = min(m[3], TEMPO_SIMULACAO)
        total_trabalho += tempo_util
        perc = (tempo_util / TEMPO_SIMULACAO) * 100

        tempo_medio = 0.0
        if m[6] > 0:
            tempo_medio = tempo_util / m[6]

        stats.append(
            f"{m[0]} [{m[5]}]: {perc:.1f}% Ocup. | ⏱ Média: {tempo_medio:.1f} min"
        )

    ocupacao_media = (total_trabalho / (NUM_MEDICOS * TEMPO_SIMULACAO)) * 100

    # Gravar Log
    try:
        with open("relatorio_final.txt", "w", encoding="utf-8") as f:
            f.write("LOG FINAL\n=========\n")
            f.write("\n".join(log_auditoria))
    except:
        pass

    resultado = {
        'total': doentes_atendidos,
        'media_espera': np.mean(tempos_espera) if tempos_espera else 0,
        'media_clinica': np.mean(tempos_clinica) if tempos_clinica else 0,
        'media_consulta': np.mean(tempos_consulta) if tempos_consulta else 0,
        'ocupacao_media': ocupacao_media,
        'max_fila': max_fila,
        'stats_equipa': stats,
        'plot_fila': list(zip(*dados_fila)),
        'plot_ocup': list(zip(*dados_ocupacao)),
        'contagem_especialidade': contagem_especialidade
    }
    return resultado

def realizar_analise_sensibilidade(config_base):
    taxas = range(10, 31, 2)
    y = []
    for t in taxas:
        cfg = config_base.copy()
        cfg['taxa_chegada'] = t
        res = simular_atendimento(cfg, None)
        valor = np.mean(res['plot_fila'][1]) if res['plot_fila'] else 0
        y.append(valor)
    resultado = (list(taxas), y)
    return resultado