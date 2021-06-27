import os
import numpy as np
import time

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
ACTIONS = ['up', 'right', 'down', 'left']
TERMINAL_STATE_INDEX = {0: [2, 3, 4]}

q_values = np.zeros((ENVIRONMENT_ROWS, ENVIRONMENT_COLUMNS, 4))

# Define todos os lugares em que o agente nao pode se mover
walls = {}
walls[1] = [3]
walls[4] = [i for i in range(0, 2)]
walls[4].extend([i for i in range(3, 7)])
walls[5] = [6]

# Define todos os locais inicialmente como -100
rewards = np.full((ENVIRONMENT_ROWS, ENVIRONMENT_COLUMNS), -100.)

# Define os pontos da base e ao lado do objeto como alguma recompensa maior
rewards[0, 2] = 100
rewards[0, 3] = 100
rewards[0, 4] = 100

# rewards[2, 2] = 50
# rewards[2, 4] = 50

# Define os espacos possiveis de caminhar com uma recompensa de -1
aisles = {}
aisles[0] = [i for i in range(0, 2)]
aisles[0].extend([i for i in range(5, 7)])
aisles[1] = [i for i in range(0, 3)]
aisles[1].extend([i for i in range(4, 7)])
aisles[2] = [i for i in range(0, 3)]
aisles[2].extend([i for i in range(4, 7)])
aisles[3] = [i for i in range(0, 7)]
aisles[4] = [2]
aisles[5] = [i for i in range(0, 6)]

for row_index in range(0, 6):
    for col_index in aisles[row_index]:
        rewards[row_index, col_index] = -1

print(rewards)

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
    
    # time.sleep(1)

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

    if ACTIONS[action_index] == 'up' and current_row_index > 0:
        new_row_index -= 1
    elif ACTIONS[action_index] == 'right' and current_column_index < ENVIRONMENT_COLUMNS - 1:
        new_column_index += 1
    elif ACTIONS[action_index] == 'down' and current_row_index < ENVIRONMENT_ROWS - 1:
        new_row_index += 1
    elif ACTIONS[action_index] == 'left' and current_column_index > 0:
        new_column_index -= 1
    
    return new_row_index, new_column_index

def get_shortest_path():
    current_row_index, current_column_index = INITIAL_AGENT_POS
    current_object_row_index, current_object_column_index = INITIAL_OBJECT_POS
    
    object_attached = False
    object_right_side = False

    shortest_path = []
    shortest_path.append([current_row_index, current_column_index])

    while not is_terminal_state(current_object_row_index, current_object_column_index):
        action_index = get_next_action(current_row_index, current_column_index, 1.)
        current_row_index, current_column_index = get_next_location(
            current_row_index, current_column_index, action_index
        )

        shortest_path.append([current_row_index, current_column_index])
    
    return shortest_path

def main():
    epsilon = 0.9
    discount_factor = 0.9
    learning_rate = 0.9
    max_timesteps_per_episode = 100

    for episode in range(10):
        row_index, column_index = INITIAL_AGENT_POS
        object_row_index, object_column_index = INITIAL_OBJECT_POS

        object_attached = False
        object_right_side = False

        timesteps = 0
        visualize_environment(
            row_index, column_index,
            object_row_index, object_column_index
        )
        
        print('Episodio: {}'.format(episode))
        # time.sleep(1)

        while not is_terminal_state(object_row_index, object_column_index):
            if object_attached:
                action_found = False
                while not action_found:
                    action_index = get_next_action(row_index, column_index, epsilon)
                    if object_right_side and ACTIONS[action_index] != 'right':
                        action_found = True
                    elif not object_right_side and ACTIONS[action_index] != 'left':
                        action_found = True
            else:    
                action_index = get_next_action(row_index, column_index, epsilon)
            
            old_row_index, old_column_index = row_index, column_index
            old_obj_row_index, old_obj_col_index = object_row_index, object_column_index

            row_index, column_index = get_next_location(row_index, column_index, action_index)

            if object_attached:
                object_row_index, object_column_index = get_next_location(object_row_index, object_column_index, action_index)

            reward = rewards[row_index, column_index]
            old_q_value = q_values[old_row_index, old_column_index, action_index]
            temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

            new_q_value = old_q_value + (learning_rate * temporal_difference)
            q_values[old_row_index, old_column_index, action_index] = new_q_value

            if (is_invalid_state(row_index, column_index, object_row_index, object_column_index)):
                row_index, column_index = old_row_index, old_column_index
                object_row_index, object_column_index = old_obj_row_index, old_obj_col_index
            else:
                if not object_attached:
                    if row_index == INITIAL_OBJECT_POS[0]:
                        if (column_index + 1) == INITIAL_OBJECT_POS[1]:
                            object_attached = True
                            object_right_side = True
                        elif (column_index - 1) == INITIAL_OBJECT_POS[1]:
                            object_attached = True
                            object_right_side = False

            timesteps += 1
            visualize_environment(
                row_index, column_index,
                object_row_index, object_column_index
            )

            if timesteps > max_timesteps_per_episode:
                print('Quantidade maxima atingida. Reiniciando...')
                # time.sleep(1)
                break
    
    print('Training complete')
    path = get_shortest_path()

main()