class Automaton:
    def __init__(self, num_symbols, num_states, initial_states, final_states, transitions):
        self.num_symbols = num_symbols #nb de symboles
        self.num_states = num_states #nb d'état
        self.initial_states = initial_states #états
        self.final_states = final_states
        self.transitions = transitions

        # Création de l'alphabet à partir des symboles trouvés dans les transitions
        self.alphabet = set()
        for (start_state, symbol, end_state) in transitions:
            self.alphabet.add(symbol)
        # Alternative : générer l'alphabet à partir de num_symbols
        # self.alphabet = {chr(ord('a') + i) for i in range(num_symbols)}

    def display(self):
        print("Automate chargé :")
        print("Nombre de lettres :", self.num_symbols)
        print("Nombre d'états: ", self.num_states)
        print("Etats initiaux : ", self.initial_states)
        print("Etats finaux :", self.final_states)
        print("Transitions :")
        for start_state, symbol, end_state in self.transitions:
            print(f"{start_state} --{symbol}--> {end_state}")

    
    def reconnaitre_mot(self, mot):
        """
        Reconnaît si un mot est accepté par l'automate.
        """
        # Vérification que l'automate possède un état initial unique
        if len(self.initial_states) != 1:  # Changé: initial_states au lieu de etats_initiaux
            print(f"❌ L'automate a {len(self.initial_states)} états initiaux, il en faut 1.")
            return False

        # Vérifier si le mot est "end" (pour quitter)
        if mot == "end":
            print("Fin de la reconnaissance de mots.")
            return True

        # Récupération de l'état initial unique
        etat_courant = self.initial_states[0]  # Changé: utilisation directe

        # Parcours du mot
        for symbole in mot:
            # Vérifier que le symbole appartient à l'alphabet
            if symbole not in self.alphabet:
                print(f"❌ Symbole '{symbole}' non reconnu par l'automate")
                return False

            # Rechercher une transition
            transition_trouvee = False
            for (start_state, symbol, end_state) in self.transitions:
                if start_state == etat_courant and symbol == symbole:
                    etat_courant = end_state
                    transition_trouvee = True
                    break

            if not transition_trouvee:
                print(f"❌ Aucune transition pour ({etat_courant}, '{symbole}')")
                return False

        # Vérification état terminal
        if etat_courant in self.final_states:  # Changé: final_states au lieu de etats_terminaux
            print(f"✅ Le mot '{mot}' est accepté.")
            return True
        else:
            print(f"❌ Le mot '{mot}' est rejeté (état {etat_courant} non terminal).")
            return False


def read_txt(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]
        # on retire les espaces et les sauts a la lines inutilles

    num_symbols = int(lines[0])
    num_states = int(lines[1])
    # on lit le nombre de symboles et d'états

    initial_line = lines[2].split()
    num_initial_states = int(initial_line[0])
    initial_states = list(map(int, initial_line[1:1 + num_initial_states]))
    # on lit le nombre d'états initiaux puis on établit la liste de ces derniers

    final_line = lines[3].split()
    num_final_states = int(final_line[0])
    final_states = list(map(int, final_line[1:1 + num_final_states]))
    # même chose avec les états terminaux

    num_transitions = int(lines[4])
    # on lit le nombres de transition

    transition_lines = lines[5:5 + num_transitions]
    # on prend ici toutes les lignes a partir de la 5ème ligne en créant une liste pour en faire l'inventaire

    transitions = []

    for transition in transition_lines:
        # On découpe la ligne en utilisant split() qui gère les espaces automatiquement
        parts = transition.split()

        if len(parts) >= 3:
            start_state = int(parts[0])  #état de départ
            symbol = parts[1]  #symbole associé a la transition
            end_state = int(parts[2])  #état d'arrivé

            transitions.append((start_state, symbol, end_state))
            # on insère l'état de départ, le symbole associé a la transition e l'état d'arrivé

    return Automaton(num_symbols, num_states, initial_states, final_states, transitions)

def standardisation(AF):
    print("\n── Standardisation ────────────────────────")

    i0 = AF.num_states  # Le nouvel état initial i0 reçoit le numéro suivant le dernier état existant (les états vont de 0 à num_states-1, donc i0 = num_states)

    nouvelles_transitions = list(AF.transitions) # On copie toutes les transitions existantes dans la nouvelle liste

    # Pour chaque ancien état initial, on copie ses transitions sortantes vers i0
    # i0 "hérite" ainsi du comportement de tous les anciens états initiaux
    for etat_init in AF.initial_states:
        for (start_state, symbol, end_state) in AF.transitions:
            if start_state == etat_init:
                nouvelle = (i0, symbol, end_state)
                if nouvelle not in nouvelles_transitions:   # On évite les doublons
                    nouvelles_transitions.append(nouvelle)

    nouveaux_terminaux = list(AF.final_states)    # On copie la liste des états terminaux existants
    if any(e in AF.final_states for e in AF.initial_states):    # Si un ancien état initial était terminal, i0 doit l'être aussi (pour que le langage reconnu reste le même)
        if i0 not in nouveaux_terminaux:
            nouveaux_terminaux.append(i0)

    print(f"  Nouvel état initial créé : {i0}")
    print(f"  Il hérite des transitions de : {AF.initial_states}")
    if i0 in nouveaux_terminaux:
        print(f"  {i0} est aussi terminal (un ancien initial l'était).")

    # On retourne le nouvel automate standardisé avec i0 comme seul état initial
    return Automaton(
        num_symbols=AF.num_symbols,
        num_states=AF.num_states + 1,    # un état de plus
        initial_states=[i0],
        final_states=nouveaux_terminaux,
        transitions=nouvelles_transitions
    )


def non_standard(AF):
    print("\n── Test : standard ? ──────────────────────")
    raisons = []

    # Condition 1 : un automate standard a exactement UN état initial
    if len(AF.initial_states) != 1:
        raisons.append(
            f"  → Nombre d'états initiaux : {len(AF.initial_states)} (doit être 1)"
        )

    # Condition 2 : aucune transition ne doit arriver sur l'état initial
    if len(AF.initial_states) >= 1:
        etat_init = AF.initial_states[0]
        for (start_state, symbol, end_state) in AF.transitions:
            if end_state == etat_init:       # une transition arrive sur l'état initial
                raisons.append(
                    f"  → Transition ({start_state}, '{symbol}') "
                    f"arrive sur l'état initial {etat_init}"
                )

    # Si on a trouvé au moins une raison, l'automate est non standard
    if raisons:
        print("  L'automate N'EST PAS standard :")
        for r in raisons:
            print(r)
        return True      # non standard
    else:
        print("  L'automate EST standard.")
        return False     # standard


def minimize(self):
    alphabet = [chr(ord('a') + i) for i in range(self.num_symbol)]
    # on génére l'alphabet selon le nombre de symboles de l'automate

    final_states = set(self.final_states)
    non_final_states = set(range(self.num_states)) - final_states
    partitions = [final_states, non_final_states]
    # on crée la partition initiale en créant des ensembles d'états

    changed = True

    while changed:
        changed = False
        new_partitions = []
        # on répéte la boucle tant que l'automate est modifié

        for group in partitions:
            subgroups = {}
            # on prends un groupe d'état dans la partition

            for state in group:
                signature = []
                # pour chaque état, la signature décrit vers quel groupe il va

                for symbol in alphabet:
                    next_states = [
                        t[2] for t in self.transitions
                        if t[0] == state and t[1] == symbol
                    ]
                    # on crée ici pour chaque état de l'alphabet une liste qui fait l'inventaire de chauque état suivant en faisant correspondre l'état et le symbole avec l'automate chargé

                    next_state = next_states[0] if next_states else None
                    # on crée une variable qui stock l'état suivant si il existe

                    for i, p in enumerate(partitions):
                        if next_state in p:
                            signature.append(i)
                            break
                    # on rajoute l'indice de l'ensemble de la partition initiale dans lequel l'état suivant est présent

                signature = tuple(signature)

                if signature not in subgroups:
                    subgroups[signature] = set()
                subgroups[signature].add(state)

            new_partitions.extend(subgroups.values())
            # on rajoute tout les nouveaux sous groupe dans la nouvelle partition

            if len(subgroups) > 1:
                changed = True
            # si le groupe de départ à été modifié, on relance une itération

        partitions = new_partitions
        # on remplace la partition initiale par la nouvelle partition

    new_states = list(partitions)
    # chaque groupe devient un état

    new_transitions = []
    new_initial = None
    new_final = []

    # on crée les listes pour le nouvel automate et on s'aprete a recalculer le nouvel état initial

    for i, group in enumerate(new_states):
        if any(s in self.initial_states for s in group):
            new_initial = i
            # on cherche l'ancien état initial dans les nouveaux états

        if any(s in self.final_states for s in group):
            new_final.append(i)
            # meme chose pour les états finaux

        for symbol in alphabet:
            state = next(iter(group))

            next_state = [
                t[2] for t in self.transitions
                if t[0] == state and t[1] == symbol
            ][0]

            for j, g in enumerate(new_states):
                if next_state in g:
                    new_transitions.append((i, symbol, j))

    # Sauvegarde correspondance
    self.minimized_partitions = new_states

    return Automaton(
        self.num_symbols,
        len(new_states),
        [new_initial],
        new_final,
        new_transitions
    )

def display_minimal(self):
    print("Automate minimal :")

    print("États (groupes) :")
    for i, group in enumerate(self.minimized_partitions):
        print(f"{i} -> {group}")

    self.display()