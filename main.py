import os
import numpy as np
import time
import matplotlib.pyplot as plt

# 6x7 grid
# 0 - Current agent position
# 1 - Free places
# 2 - Wall's
# 3 - Object
# 4 - Base
environment = [
    [1, 1, 4, 4, 4, 1, 1],
    [1, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [2, 2, 1, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 2]
]
ENVIRONMENT_ROWS = 6
ENVIRONMENT_COLUMNS = 7
INITIAL_AGENT_POS = (5,0)
INITIAL_OBJECT_POS = (2,3)
ACTIONS = ['up', 'right', 'down', 'left', 'stay']
TERMINAL_STATE_INDEX = {0: [2, 3, 4]}

q_values = np.zeros((ENVIRONMENT_ROWS, ENVIRONMENT_COLUMNS, 4))

# Define todos os lugares em que o agente nao pode se mover
walls = {}
walls[1] = [3]
walls[4] = [i for i in range(0, 2)]
walls[4].extend([i for i in range(3, 7)])
walls[5] = [6]

# Define todos os locais inicialmente como -100
# O tamanho do array de recompensas é 6x7x2
# O tamanho 2 ao final foi definido para enquadrar as situacoes
# em que o objeto esta selecionado ou nao, sendo
# 0 - objeto nao esta anexado / 1 - objeto esta anexado
rewards = np.full((ENVIRONMENT_ROWS, ENVIRONMENT_COLUMNS, 2), -100.)

# Define os espacos possiveis de caminhar com uma recompensa de -1
aisles = {}
aisles[0] = [i for i in range(0, 7)]
aisles[1] = [i for i in range(0, 3)]
aisles[1].extend([i for i in range(4, 7)])
aisles[2] = [i for i in range(0, 7)]
aisles[3] = [i for i in range(0, 7)]
aisles[4] = [2]
aisles[5] = [i for i in range(0, 6)]

for row_index in range(0, 6):
    for col_index in aisles[row_index]:
        for i in range(2):
            rewards[row_index, col_index, i] = -1

# Quando o objeto nao esta selecionado
# Adiciona nas duas laterais o valor de recompensa de 50
rewards[2, 2, 0] = 40
rewards[2, 4, 0] = 40

# Quando o objeto esta selecionado, adiciona 100 nos campos da base
rewards[0, 2, 1] = 100
rewards[0, 3, 1] = 100
rewards[0, 4, 1] = 100

def visualize_environment(
    current_row_position, current_col_position,
    current_row_object_position, current_col_object_position,
    clear_screen=False
):
    if clear_screen:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    print('-'*40)
    for i in range(len(environment)):
        txt = ''
        for j in range(len(environment[i])):
            if i == current_row_position and j == current_col_position:
                txt += '|{:<5}'.format('X')
            elif i == current_row_object_position and j == current_col_object_position:
                txt += '|{:<5}'.format('3')
            else:
                txt += '|{:<5}'.format(environment[i][j])
        
        print(txt)
        print('-'*40)
    
    # time.sleep(0.3)

def is_terminal_state(object_row_index, object_column_index):
    if object_row_index in TERMINAL_STATE_INDEX.keys():
        return object_column_index in TERMINAL_STATE_INDEX[object_row_index]
    return False

def is_invalid_state(
    current_row_index, current_column_index,
    current_row_object_position, current_col_object_position
):
    # Verifica se esta se movendo para alguma parede
    if current_row_index in walls.keys() and current_column_index in walls[current_row_index]:
        return True
    # Adiciona uma validacao para nao permitir que a posicao do agente seja a mesma do objeto
    elif current_row_index == current_row_object_position and current_column_index == current_col_object_position:
        return True
    # Verifica se o objeto esta se movendo para uma parede
    elif current_row_object_position in walls.keys() and current_col_object_position in walls[current_row_object_position]:
        return True
    else:
        return False

def get_next_action(current_row_index, current_column_index, epsilon):
    # Obtem um valor aleatorio e compara com episolon
    # Caso o valor seja menor, seleciona a melhor opcao do q table
    # Caso contrario obtem uma acao randomica
    if np.random.random() < epsilon:
        return np.argmax(q_values[current_row_index, current_column_index])
    else:
        return np.random.randint(4)

def get_next_location(current_row_index, current_column_index, action_index):
    new_row_index = current_row_index
    new_column_index = current_column_index

    if ACTIONS[action_index] == 'stay':
        return new_row_index, new_column_index
    elif ACTIONS[action_index] == 'up' and current_row_index > 0:
        new_row_index -= 1
    elif ACTIONS[action_index] == 'right' and current_column_index < ENVIRONMENT_COLUMNS - 1:
        new_column_index += 1
    elif ACTIONS[action_index] == 'down' and current_row_index < ENVIRONMENT_ROWS - 1:
        new_row_index += 1
    elif ACTIONS[action_index] == 'left' and current_column_index > 0:
        new_column_index -= 1

    return new_row_index, new_column_index

def plot_convergence_curve(convergence_data):
    x = convergence_data.keys()
    y = convergence_data.values()
    plt.scatter(x,y)
    plt.plot(x,y)

    plt.title('Curva de Convergência - Número total de timesteps por episódio')
    plt.xlabel('Episódios')
    plt.ylabel('Timesteps')
    plt.savefig('Curva de Convergência.png')

def main():
    epsilon = 0.9 # e
    discount_factor = 0.9 # γ - gamma
    learning_rate = 0.9 # a
    max_timesteps_per_episode = 200
    visualize = False
    start_time = time.time()

    convergence_curve = {}

    for episode in range(2000):
        row_index, column_index = INITIAL_AGENT_POS
        object_row_index, object_column_index = INITIAL_OBJECT_POS

        object_attached = 0

        timesteps = 0

        if visualize:
            visualize_environment(
                row_index, column_index,
                object_row_index, object_column_index
            )
        
        print('Episodio: {}'.format(episode))
        # time.sleep(1)

        while not is_terminal_state(object_row_index, object_column_index):
            action_index = get_next_action(row_index, column_index, epsilon)
            
            old_row_index, old_column_index = row_index, column_index
            old_obj_row_index, old_obj_col_index = object_row_index, object_column_index

            row_index, column_index = get_next_location(row_index, column_index, action_index)

            # Adiciona uma recompensa de -10 para casos invalidos
            reward = -100

            # Caso o objeto esteja anexado, o objeto passa a ser o ponto de referencia
            # Para obter os valores
            if object_attached > 0:
                object_row_index, object_column_index = get_next_location(object_row_index, object_column_index, action_index)
                if old_obj_row_index != object_row_index or old_obj_col_index != object_column_index:
                    reward = rewards[object_row_index, object_column_index, object_attached]
            else:
                # Caso a posicao de destino nao seja a mesma de origem
                if old_row_index != row_index or old_column_index != column_index:
                    reward = rewards[row_index, column_index, object_attached]
            
            old_q_value = q_values[old_row_index, old_column_index, action_index]
            max_next_state = np.max(q_values[row_index, column_index])

            # Calculo do Epsilon greedy strategy
            new_q_value = old_q_value + learning_rate * (reward + discount_factor * max_next_state - old_q_value)

            q_values[old_row_index, old_column_index, action_index] = new_q_value

            if (is_invalid_state(row_index, column_index, object_row_index, object_column_index)):
                row_index, column_index = old_row_index, old_column_index
                object_row_index, object_column_index = old_obj_row_index, old_obj_col_index
            else:
                if not object_attached:
                    if row_index == INITIAL_OBJECT_POS[0]:
                        if (column_index + 1) == INITIAL_OBJECT_POS[1]:
                            object_attached = 1
                        elif (column_index - 1) == INITIAL_OBJECT_POS[1]:
                            object_attached = 1

            timesteps += 1

            if visualize:
                visualize_environment(
                    row_index, column_index,
                    object_row_index, object_column_index
                )

            if timesteps > (max_timesteps_per_episode - 1):
                print('Quantidade maxima atingida. Reiniciando...')
                # time.sleep(1)
                break

        print('Etapa concluida com {0} timesteps.'.format(timesteps))
        convergence_curve[episode] = timesteps
    
    end_time = time.time()
    plot_convergence_curve(convergence_curve)
    print('Treinamento completo em {0}'.format(end_time - start_time))

if __name__ == "__main__":
    main()