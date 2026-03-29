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

    def minimize(self):
        alphabet = [chr(ord('a') + i) for i in range(self.num_symbols)]
        # on génére l'alphabet selon le nombre de symboles de l'automate

        final_states = set(self.final_states)
        non_final_states = set(range(self.num_states)) - final_states

        # Initialisation propre des partitions (évite les ensembles vides)
        partitions = []
        if final_states: partitions.append(final_states)
        if non_final_states: partitions.append(non_final_states)
        # on crée la partition initiale en créant des ensembles d'états

        changed = True

        while changed:
            changed = False
            new_partitions = []
            # on répéte la boucle tant que l'automate est modifié

            for group in partitions:
                if len(group) <= 1:
                    new_partitions.append(group)
                    continue

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

                        # CORRECTION : On cherche l'indice dans la partition STABLE (partitions)
                        target_partition_idx = -1
                        for i, p in enumerate(partitions):
                            if next_state in p:
                                target_partition_idx = i
                                break
                        signature.append(target_partition_idx)
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
        new_initial_states = []
        new_final = []

        # on crée les listes pour le nouvel automate et on s'aprete a recalculer le nouvel état initial

        for i, group in enumerate(new_states):
            if any(s in self.initial_states for s in group):
                new_initial_states.append(i)
                # on cherche l'ancien état initial dans les nouveaux états

            if any(s in self.final_states for s in group):
                new_final.append(i)
                # meme chose pour les états finaux

            # On prend un représentant du groupe pour déterminer les transitions
            representative = next(iter(group))
            for symbol in alphabet:
                # On cherche toutes les transitions correspondantes
                next_states = [
                    t[2] for t in self.transitions
                    if t[0] == representative and t[1] == symbol
                ]

                # Sécurité : on ne cherche le groupe que si une transition existe
                if next_states:
                    destination = next_states[0]
                    for j, g in enumerate(new_states):
                        if destination in g:
                            new_transitions.append((i, symbol, j))
                            break  # On a trouvé le groupe, on passe au symbole suivant

        # Sauvegarde correspondance
        self.minimized_partitions = new_states

        nouveau_SFA=Automaton(
            self.num_symbols,
            len(new_states),
            new_initial_states,
            new_final,
            new_transitions
        )
        nouveau_SFA.minimized_partitions = new_states

        return nouveau_SFA

    def display_minimal(self):
        print("\n── Automate minimal ──────────────────────")
        print("États (groupes fusionnés) :")
        if hasattr(self, 'minimized_partitions'):
            for i, group in enumerate(self.minimized_partitions):
                print(f"  {i} -> {sorted(list(group))}")

        self.display()


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



def is_deterministic(AF):
    print("\n── Test : déterministe ? ──────────────────")
    raisons = []

    # un automate doit avoir exactement 1 état initial
    if len(AF.initial_states) != 1:
        raisons.append(
            f"  → Nombre d'états initiaux : {len(AF.initial_states)} (doit être 1)"
        )

    # pour chaque état et chaque lettre, il doit y avoir au plus 1 transition
    for etat in range(AF.num_states):
        for symbole in sorted(AF.alphabet):
            if symbole == '&':
                continue  # on ignore epsilon

            # on compte combien de transitions partent de (etat, symbole)
            destinations = []
            for (depart, sym, arrivee) in AF.transitions:
                if depart == etat and sym == symbole:
                    destinations.append(arrivee)

            # s'il y en a plus d'une, c'est non déterministe
            if len(destinations) > 1:
                raisons.append(
                    f"  → Depuis l'état {etat} avec '{symbole}' : "
                    f"{len(destinations)} transitions → {destinations}"
                )

    if raisons:
        print("  L'automate N'EST PAS déterministe :")
        for r in raisons:
            print(r)
        return False
    else:
        print("  L'automate EST déterministe.")
        return True



def is_complete(AF):
    print("\n── Test : complet ? ───────────────────────")
    
    # On part du principe que l'automate est complet
    # Si on trouve un trou, on passera ça à False
    est_complet = True

    # Boucle sur chaque état de l'automate
    # range(AF.num_states) donne [0, 1, 2, ...] jusqu'au nombre d'états
    for etat in range(AF.num_states):

        # Boucle sur chaque lettre de l'alphabet
        for symbole in sorted(AF.alphabet):

            # On cherche si une transition existe pour (etat, symbole)
            # On parcourt toutes les transitions et on regarde si l'une d'elles
            # part de 'etat' avec le bon 'symbole'
            transition_trouvee = False
            for (depart, sym, arrivee) in AF.transitions:
                if depart == etat and sym == symbole:
                    transition_trouvee = True
                    break  # pas besoin de continuer, on a trouvé

            # Si on n'a rien trouvé, c'est un trou !
            if not transition_trouvee:
                print(f"  → Pas de transition depuis l'état {etat} avec '{symbole}'")
                est_complet = False

    # Affichage du résultat final
    if est_complet:
        print("  L'automate EST complet.")
    else:
        print("  L'automate N'EST PAS complet.")

    return est_complet





def complete(AF):
    print("\n── Complétion ─────────────────────────────")

    # On copie les transitions existantes dans une nouvelle liste
    # On ne veut pas modifier l'automate original, on en crée un nouveau
    nouvelles_transitions = list(AF.transitions)

    # L'état poubelle aura le numéro juste après le dernier état existant
    # Par exemple si l'automate a 4 états (0,1,2,3), la poubelle sera l'état 4
    etat_poubelle = AF.num_states

    # Ce booléen nous servira à savoir si on a vraiment eu besoin de la poubelle
    poubelle_utilisee = False

    # Boucle sur chaque état — exactement comme dans is_complete
    for etat in range(AF.num_states):

        # Boucle sur chaque lettre de l'alphabet
        for symbole in sorted(AF.alphabet):

            # On cherche si une transition existe pour (etat, symbole)
            transition_trouvee = False
            for (depart, sym, arrivee) in AF.transitions:
                if depart == etat and sym == symbole:
                    transition_trouvee = True
                    break

            # Si la transition est manquante, on la crée vers la poubelle
            if not transition_trouvee:
                nouvelles_transitions.append((etat, symbole, etat_poubelle))
                print(f"  → Transition ajoutée : {etat} --{symbole}--> {etat_poubelle} (poubelle)")
                poubelle_utilisee = True

    # Si on a utilisé la poubelle, il faut qu'elle boucle sur elle-même
    # pour chaque lettre (sinon elle-même ne serait pas complète !)
    if poubelle_utilisee:
        for symbole in sorted(AF.alphabet):
            nouvelles_transitions.append((etat_poubelle, symbole, etat_poubelle))
        print(f"  → État poubelle {etat_poubelle} créé, il boucle sur lui-même.")

        # On retourne un nouvel automate avec un état de plus
        return Automaton(
            num_symbols=AF.num_symbols,
            num_states=AF.num_states + 1,   # +1 pour la poubelle
            initial_states=AF.initial_states,
            final_states=AF.final_states,    # la poubelle n'est PAS finale
            transitions=nouvelles_transitions
        )
    else:
        # Cas où l'automate était déjà complet (ne devrait pas arriver
        # si on a bien appelé is_complete avant, mais au cas où)
        print("  Aucune transition manquante, l'automate était déjà complet.")
        return AF




def epsilon_fermeture(etats, transitions):
    """
    Calcule l'epsilon-fermeture d'un ensemble d'états.
    C'est l'ensemble de tous les états atteignables
    en suivant uniquement des flèches epsilon (&).
    """

    # on part des états donnés, ils font partie de leur propre fermeture
    fermeture = set(etats)

    # liste des états qu'on n'a pas encore explorés
    a_explorer = list(etats)

    while a_explorer:

        # on prend le prochain état à explorer
        etat_courant = a_explorer.pop(0)

        # on cherche toutes les transitions epsilon depuis cet état
        for (depart, sym, arrivee) in transitions:
            if depart == etat_courant and sym == '&':

                # si on n'a pas encore cet état dans la fermeture, on l'ajoute
                if arrivee not in fermeture:
                    fermeture.add(arrivee)
                    a_explorer.append(arrivee)  # on devra l'explorer aussi

    return frozenset(fermeture)


def determinize_and_complete(AF):
    """
    Construit l'automate déterministe et complet équivalent.
    Gère aussi les epsilon-transitions (&).
    """
    print("\n── Déterminisation et complétion ──────────")

    # on enlève epsilon de l'alphabet car ce n'est pas une vraie lettre
    alphabet = sorted(sym for sym in AF.alphabet if sym != '&')

    # ─── ÉTAPE 1 : premier super-état ────────────────────────────────
    # le premier super-état c'est l'epsilon-fermeture des états initiaux
    # ex : depuis {0}, en suivant les epsilon on peut atteindre {0,1,2,3...}
    premier_super_etat = epsilon_fermeture(AF.initial_states, AF.transitions)

    # dictionnaire qui fait le lien entre un super-état et son numéro
    # ex : {frozenset({0,1,2}): 0, frozenset({3,4}): 1, ...}
    super_etat_vers_numero = {premier_super_etat: 0}

    # compteur pour numéroter les nouveaux états : 0, 1, 2, ...
    compteur = 1

    # liste des super-états qu'on n'a pas encore traités
    # au début il n'y a que le premier
    a_traiter = [premier_super_etat]

    # transitions du nouvel automate qu'on va construire
    nouvelles_transitions = []

    # ─── ÉTAPES 2 & 3 : on remplit le tableau ────────────────────────
    # tant qu'il reste des super-états à explorer...
    while a_traiter:

        # on prend le prochain super-état à traiter (la prochaine ligne du tableau)
        super_etat_courant = a_traiter.pop(0)
        numero_courant = super_etat_vers_numero[super_etat_courant]

        print(f"\n  Traitement de l'état {numero_courant} "
              f"= {set(super_etat_courant)}")

        # pour chaque lettre de l'alphabet (sans epsilon)...
        for symbole in alphabet:

            # ── calcul des destinations ──────────────────────────────
            # on cherche tous les états atteignables depuis ce super-état
            # avec cette lettre
            destinations = set()
            for etat in super_etat_courant:
                for (depart, sym, arrivee) in AF.transitions:
                    if depart == etat and sym == symbole:
                        destinations.add(arrivee)

            # si on a trouvé des destinations, on calcule leur epsilon-fermeture
            # ex : on arrive en {4}, mais depuis 4 on peut aller en {4,5,8}
            # via epsilon → les destinations réelles sont {4,5,8}
            if destinations:
                destinations = epsilon_fermeture(destinations, AF.transitions)

            # si le sac est vide → pas de transition → on gère avec la poubelle après
            if not destinations:
                print(f"    avec '{symbole}' → RIEN")
                continue

            # si ce super-état est nouveau, on lui donne un numéro
            # et on l'ajoute à a_traiter pour le traiter plus tard
            if destinations not in super_etat_vers_numero:
                super_etat_vers_numero[destinations] = compteur
                compteur += 1
                a_traiter.append(destinations)

            numero_destination = super_etat_vers_numero[destinations]

            # on ajoute la transition dans le nouvel automate
            nouvelles_transitions.append(
                (numero_courant, symbole, numero_destination)
            )
            print(f"    avec '{symbole}' → {set(destinations)} "
                  f"= état {numero_destination}")

    # ─── ÉTATS FINAUX ────────────────────────────────────────────────
    # un super-état est final s'il contient au moins un état final de l'original
    nouveaux_finaux = []
    for super_etat, numero in super_etat_vers_numero.items():
        for etat in super_etat:
            if etat in AF.final_states:
                nouveaux_finaux.append(numero)
                break  # pas besoin de continuer, on a trouvé

    # ─── COMPLÉTION : ajout de la poubelle ───────────────────────────
    # on cherche les transitions manquantes et on les redirige vers la poubelle
    etat_poubelle = compteur
    poubelle_utilisee = False

    for super_etat, numero in super_etat_vers_numero.items():
        for symbole in alphabet:

            # est-ce qu'une transition existe depuis ce super-état ?
            transition_trouvee = False
            for (depart, sym, arrivee) in nouvelles_transitions:
                if depart == numero and sym == symbole:
                    transition_trouvee = True
                    break

            # si non → on redirige vers la poubelle
            if not transition_trouvee:
                nouvelles_transitions.append((numero, symbole, etat_poubelle))
                poubelle_utilisee = True

    # la poubelle boucle sur elle-même pour chaque lettre
    if poubelle_utilisee:
        for symbole in alphabet:
            nouvelles_transitions.append((etat_poubelle, symbole, etat_poubelle))
        print(f"\n  État poubelle créé : {etat_poubelle}")

    # ─── AFFICHAGE DE LA CORRESPONDANCE ──────────────────────────────
    # on montre à l'utilisateur quel super-état correspond à quel numéro
    print("\n  Correspondance des états :")
    for super_etat, numero in sorted(super_etat_vers_numero.items(), key=lambda x: x[1]):
        # on formate le nom : {0, 1, 2} devient "0.1.2"
        etats_originaux = ".".join(str(e) for e in sorted(super_etat))
        est_final = "(T)" if numero in nouveaux_finaux else ""
        print(f"    État {numero} ← {{{etats_originaux}}} {est_final}")
    if poubelle_utilisee:
        print(f"    État {etat_poubelle} ← {{poubelle}}")

    # ─── RETOUR ──────────────────────────────────────────────────────
    num_states_total = compteur + (1 if poubelle_utilisee else 0)

    return Automaton(
        num_symbols=AF.num_symbols,
        num_states=num_states_total,
        initial_states=[0],           # toujours l'état 0, le premier super-état
        final_states=nouveaux_finaux,
        transitions=nouvelles_transitions
    )