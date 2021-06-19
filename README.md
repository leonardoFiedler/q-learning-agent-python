## Setup

```
python3 -m venv .venv
source .venv/bin/activate
```

## Questões

Implemente uma solução via reinforcement learning para o problema de transporte de objeto e
apresente um relatório endereçando os seguintes aspectos da solução:

1. Modelagem do MDP:
    
    (a) Apresente a modelagem de estados considerada, bem como a quantidade de estados
presentes no MDP. Inclua na contagem os estados não-válidos;
    
    (b) Apresente a modelagem das ações que o agente pode executar;
    
    (c) Apresente a modelagem da função de recompensa, com as situações em que o agente é recompensado bem como a magnitude da recompensa. Justifique as suas escolhas.

2. Configuração dos Experimentos
    
    (a) Apresente os valores de taxa de aprendizagem (alfa) e fator de desconto (gamma) do algoritmo de aprendizagem Q-Learning;

    (b) Apresente as configurações do horizonte de aprendizagem, que é representado pela quantidade máxima de passos de tempo por episódios, quantidade máxima de episódios, e política de exploração ao longo do tempo;

3. Resultados Experimentais
    
    (a) Apresente a curva de convergência, representada pela quantidade de passos (timesteps) necessários para resolver a tarefa ao longo do tempo (episódios).

    (b) Apresente o tempo de processamento necessário para resolver o problema.
