# Simulador Clínico

## Trabalho de
- **Nome**: [Francisca Pereira a112168, Joana Cunha a112128, Maria Moura a111681]
- **Instituição**: Universidade do Minho
- Curso: Engenharia Biomédoca

---

## 1. Visão Geral

Este projeto implementa um **simulador clínico** para análise do fluxo de pacientes numa clínica, incluindo:

- Sistema de triagem por prioridades
- Encaminhamento por especialidade médica
- Regras de funcionamento (por exemplo, um pediatra não atende adultos)
- Recolha de métricas de desempenho globais e individuais
- Interface gráfica interativa para controlo e análise

---

## 2. Modelo de Simulação

- Chegadas: Distribuição de Poisson (intervalos exponenciais)
- Tempos de consulta:
  - Distribuição exponencial
  - Distribuição normal
  - Distribuição uniforme

Cada paciente possui:
- Nome
- Idade
- Prioridade (Verde, Amarela, Vermelha)
- Especialidade médica

Regras de encaminhamento:
- Crianças são encaminhadas apenas para Pediatria ou Medicina Geral
- Adultos nunca são encaminhados para Pediatria
- O sistema tenta distribuir primeiro um médico da especialidade correta, depois um geral e, por fim, qualquer médico disponível que não seja pediatra para adultos

---

## 3. Funcionalidades Principais

### 3.1 Simulação Clínica

- Geração aleatória de pacientes
- Gestão de fila com prioridades
- Distribuição dinâmica de médicos
- Cumpre restrições de especialidade
- Recolha de estatísticas 

### 3.2 Visualização Gráfica

O sistema produz automaticamente:

- Gráfico da evolução do tamanho da fila ao longo do tempo
- Gráfico da ocupação dos médicos ao longo do tempo
- Gráfico circular da distribuição de pacientes por especialidade
- Gráfico de análise de sensibilidade (Stress Test)

### 3.3 Análise de Sensibilidade 

- Varia automaticamente a taxa de chegada de pacientes
- Mede o impacto no tamanho médio da fila
- Produz um gráfico de resposta do sistema à carga 

### 3.4 Logs e Gestão de Dados

- Geração automática do ficheiro:
  - `relatorio_final.txt` com o registo detalhado dos eventos da simulação
  - Importação de ficheiro `pessoas.json` para dados reais.

### 3.5 Gestão da Equipa

Para cada médico são calculadas:
- Percentagem de ocupação
- Tempo médio de consulta
- Número total de pacientes atendidos

---

## 3.6 Configuração Técnica
O sistema utiliza um motor baseado em Python com as seguintes dependências:
- `numpy`: Para modelação de processos de Poisson.
- `FreeSimpleGUI`: Para a interface de utilizador.
- `matplotlib`: Para visualização de dados.

---

## 4. Interface Gráfica

A interface foi desenvolvida com FreeSimpleGUI e inclui:

- Separadores:
  - Controlo e Indicadores
  - Equipa
  - Logs
  - Stress Test
  - Relatório
- Controlo interativo de:
  - Pacientes por hora
  - Número de médicos
  - Tempo médio base de consulta
  - Tipo de distribuição estatística
- Botão para iniciar a simulação
- Botão para sair da aplicação com confirmação
- Indicador de estado da simulação

---


