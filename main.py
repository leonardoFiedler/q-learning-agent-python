import os

# 7x6 grid
# 0 - Current agent position
# 1 - Free places
# 2 - Wall's
# 3 - Object
# 4 - Base
environment = [
    [1, 1, 4, 4, 4, 1, 1],
    [1, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [2, 2, 1, 2, 2, 2, 2],
    [0, 1, 1, 1, 1, 1, 2]
]

INITIAL_AGENT_POS = (5,0)

def visualize_environment(clear_screen=False):
    if clear_screen:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    print('-'*40)
    for i in range(len(environment)):
        txt = ''
        for j in range(len(environment[i])):
            txt += '|{:<5}'.format(environment[i][j])
        
        print(txt)
        print('-'*40)


def main():
    visualize_environment()


main()