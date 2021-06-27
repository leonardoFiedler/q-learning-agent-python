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
    R.:

    1. Lista de estados do agente

    1. Posição
    2. Direção
    3. Agarrado ao objeto
    4. Posição do objeto
    5. Direção do objeto

    2. Modelagem de Estados do Agente

    S = {
        (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
        (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
        (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
        (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
        (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
        (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)
    }

    3. Total de Estados possíveis: 6 (linhas) X 7 (colunas)

    (b) Apresente a modelagem das ações que o agente pode executar
    R.:

    1. Lista de ações do agente

    1. Mover para cima
    2. Mover para a esquerda
    3. Mover para a direita
    4. Mover para baixo
    5. Permanecer na mesma célula

    (c) Apresente a modelagem da função de recompensa, com as situações em que o agente é recompensado bem como a magnitude da recompensa. Justifique as suas escolhas.
    R.: O objetivo principal é agarrar o objeto e chegar a base na quantidade mínima de passos.


2. Configuração dos Experimentos
    
    (a) Apresente os valores de taxa de aprendizagem (alfa) e fator de desconto (gamma) do algoritmo de aprendizagem Q-Learning;

    (b) Apresente as configurações do horizonte de aprendizagem, que é representado pela quantidade máxima de passos de tempo por episódios, quantidade máxima de episódios, e política de exploração ao longo do tempo;

3. Resultados Experimentais
    
    (a) Apresente a curva de convergência, representada pela quantidade de passos (timesteps) necessários para resolver a tarefa ao longo do tempo (episódios).

    (b) Apresente o tempo de processamento necessário para resolver o problema.
