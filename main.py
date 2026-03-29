from automaton import read_txt, non_standard, standardisation, is_deterministic, is_complete, complete, determinize_and_complete, automate_complementaire


def main():
    while True:
        numero = input("\nNuméro de l'automate à charger (ou 'q' pour quitter) : ").strip()

        if numero.lower() == 'q':
            print("Au revoir !")
            break

        filename = f"../Projet_automate_python/automates_de_tests/A{numero}.txt"
        automaton = read_txt(filename)

        automaton.display()

        automate_a_utiliser = automaton
        AFDC = None

        while True:
            print("\n── Que voulez-vous faire ? ─────────────────")
            print("  1. Standardiser l'automate")
            print("  2. Déterminiser et compléter l'automate")
            print("  3. Minimiser l'automate")
            print("  4. Construire l'automate complémentaire")
            print("  5. Rechercher un mot")
            print("  6. Tout faire automatiquement")
            print("  7. Changer d'automate")
            print("  q. Quitter")

            choix = input("\nVotre choix : ").strip().lower()

            if choix == '1':
                if non_standard(automate_a_utiliser):
                    SFA = standardisation(automate_a_utiliser)
                    SFA.display()
                    automate_a_utiliser = SFA
                    print("Automate standardisé avec succès!")
                else:
                    print("L'automate est déjà standard, pas besoin de le standardiser.")

            elif choix == '2':
                a_des_epsilon = any(
                    sym == '&'
                    for (depart, sym, arrivee) in automate_a_utiliser.transitions
                )
                if a_des_epsilon:
                    print("\n  L'automate contient des epsilon-transitions.")
                    print("  → Déterminisation et complétion directe.")
                    AFDC = determinize_and_complete(automate_a_utiliser)
                    print("\nAutomate déterminisé et complété avec succès!")
                    AFDC.display()
                    automate_a_utiliser = AFDC
                else:
                    deterministe = is_deterministic(automate_a_utiliser)
                    if deterministe:
                        complet = is_complete(automate_a_utiliser)
                        if complet:
                            AFDC = automate_a_utiliser
                            print("\nL'automate est déjà déterministe et complet.")
                        else:
                            AFDC = complete(automate_a_utiliser)
                            print("\nAutomate complété avec succès!")
                            AFDC.display()
                            automate_a_utiliser = AFDC
                    else:
                        AFDC = determinize_and_complete(automate_a_utiliser)
                        print("\nAutomate déterminisé et complété avec succès!")
                        AFDC.display()
                        automate_a_utiliser = AFDC

            elif choix == '3':
                if not is_deterministic(automate_a_utiliser) or any(
                        sym == '&' for (_, sym, _) in automate_a_utiliser.transitions):
                    automate_a_utiliser = determinize_and_complete(automate_a_utiliser)
                elif not is_complete(automate_a_utiliser):
                    automate_a_utiliser = complete(automate_a_utiliser)

                automate_minimise = automate_a_utiliser.minimize()
                automate_minimise.display_minimal()
                automate_a_utiliser = automate_minimise

            elif choix == '4':
                A_comp = automate_complementaire(automate_a_utiliser)
                print("\nAutomate complémentaire construit avec succès !")
                A_comp.display()
                automate_a_utiliser = A_comp

            elif choix == '5':
                print(f"\nAlphabet reconnu : {automate_a_utiliser.alphabet}")
                while True:
                    mot = input("Entrez un mot à tester (ou 'c' pour revenir au menu) : ").strip()
                    if mot.lower() == 'c':
                        break
                    if not mot:
                        print("Veuillez entrer un mot non vide.")
                        continue
                    automate_a_utiliser.reconnaitre_mot(mot)

            elif choix == '6':
                print("\n══ Traitement automatique complet ══════════")

                print("\n── Automate de base ────────────────────────")
                automaton.display()

                # Étape 1 : Standardisation si nécessaire
                print("\n── Étape 1 : Standardisation ───────────────")
                if non_standard(automate_a_utiliser):
                    automate_a_utiliser = standardisation(automate_a_utiliser)
                    automate_a_utiliser.display()

                # Étape 2 : Déterminisation et complétion
                print("\n── Étape 2 : Déterminisation et complétion ─")
                a_des_epsilon = any(
                    sym == '&'
                    for (depart, sym, arrivee) in automate_a_utiliser.transitions
                )
                if a_des_epsilon:
                    AFDC = determinize_and_complete(automate_a_utiliser)
                else:
                    deterministe = is_deterministic(automate_a_utiliser)
                    if deterministe:
                        complet = is_complete(automate_a_utiliser)
                        if complet:
                            AFDC = automate_a_utiliser
                            print("L'automate est déjà déterministe et complet.")
                        else:
                            AFDC = complete(automate_a_utiliser)
                    else:
                        AFDC = determinize_and_complete(automate_a_utiliser)
                AFDC.display()
                automate_a_utiliser = AFDC

                # Étape 3 : Minimisation
                print("\n── Étape 3 : Minimisation ──────────────────")
                automate_a_utiliser = automate_a_utiliser.minimize()
                automate_a_utiliser.display_minimal()

                # Étape 4 : Automate complémentaire
                print("\n── Étape 4 : Automate complémentaire ───────")
                automate_a_utiliser = automate_complementaire(automate_a_utiliser)
                automate_a_utiliser.display()

                # Étape 5 : Reconnaissance de mots
                print("\n── Étape 5 : Reconnaissance de mots ────────")
                print(f"Alphabet reconnu : {automate_a_utiliser.alphabet}")
                while True:
                    mot = input("Entrez un mot à tester (ou 'c' pour revenir au menu) : ").strip()
                    if mot.lower() == 'c':
                        break
                    if not mot:
                        print("Veuillez entrer un mot non vide.")
                        continue
                    automate_a_utiliser.reconnaitre_mot(mot)

            elif choix == '7':
                break

            elif choix == 'q':
                print("Au revoir !")
                exit()

            else:
                print("Choix invalide, réessayez.")


if __name__ == "__main__":
    main()