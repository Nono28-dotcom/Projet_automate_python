class Automaton:
    def __init__(self, num_symbols, num_states, initial_states, final_states, transitions):
        self.num_symbols = num_symbols
        self.num_states = num_states
        self.initial_states = initial_states
        self.final_states = final_states
        self.transitions = transitions
        #on crée la classe automate avec les attributs suivants : nombre de lettres dans l'alphabet, nombre d'état, liste d'etats initiaux, liste d'états finaux, liste de transitions sous forme de tuple

    def display(self):
        print("Automate chargé :")
        print("Nombre de lettres :", self.num_symbols)
        print("Nombre d'états: ", self.num_states)
        print("Etats initiaux : ",self.initial_states)
        print("Etats finaux :", self.final_states)
        print("Transitions :")
        for start_state, symbol, end_state in self.transitions:
            print(f"{start_state} --{symbol}--> {end_state}")
            #on affiche pour chaque transition l'état de départ, d'arrivée et le symbole qui assure la transition





def read_txt(filename):
    with open(filename,"r",encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]
        #on retire les espaces et les sauts a la lines inutilles
    num_symbols = int(lines[0])
    num_states = int(lines[1])
    #on lit le nombrez de symboles et d'états

    initial_line = lines[2].split()
    num_initial_states = int(initial_line[0])
    initial_states = list(map(int, initial_line[1:1 + num_initial_states]))
    #on lit le nombre d'états initiaux puis on établit la liste de ces derniers

    final_line = lines[3].split()
    num_final_states = int(final_line[0])
    final_states = list(map(int, final_line[1:1 + num_final_states]))#même chose avec les états terminaux

    num_transitions = int(lines[4])
    #on lit le nombres de transition

    transition_lines = lines[5:5 + num_transitions]
    #on prend ici toutes les lignes a partir de la 5ème ligne en créant une liste pour en faire l'inventaire

    transitions = []

    for transition in transition_lines:
        i=0
        while i < len(transition) and transition[i].isdigit():
            i += 1

        start_state = int(transition[:i])
        #on incrémente i jusqu'à qu'on tombe sur la lettre, et on séléctionne les chiffres présent avant pour extraire l'état de départ

        symbol = transition[i]

        end_state = int(transition[i + 1:])

        transitions.append((start_state, symbol, end_state))
        #on insère l'état de départ, le symbole associé a la transition e l'état d'arrivé

    return Automaton(num_symbols, num_states, initial_states, final_states, transitions)
