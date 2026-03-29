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
        AFDC = None  # contiendra l'automate déterministe complet une fois calculé

        while True:
            print("\n── Que voulez-vous faire ? ─────────────────")
            print("  1. Standardiser l'automate")
            print("  2. Déterminiser et compléter l'automate")  # nouvelle option
            print("  3. Minimiser l'automate")
            print("  4. Construire l'automate complémentaire")
            print("  5. Rechercher un mot")
            print("  6. Changer d'automate")
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
                # on vérifie d'abord s'il y a des epsilon-transitions
                a_des_epsilon = any(
                    sym == '&'
                    for (depart, sym, arrivee) in automate_a_utiliser.transitions
                )

                if a_des_epsilon:
                    # epsilon → on déterminise et complète directement
                    print("\n  L'automate contient des epsilon-transitions.")
                    print("  → Déterminisation et complétion directe.")
                    AFDC = determinize_and_complete(automate_a_utiliser)
                    print("\n Automate déterminisé et complété avec succès!")
                    AFDC.display()
                    automate_a_utiliser = AFDC

                else:
                    # pas d'epsilon → on teste normalement
                    deterministe = is_deterministic(automate_a_utiliser)

                    if deterministe:
                        complet = is_complete(automate_a_utiliser)
                        if complet:
                            # déjà déterministe et complet, rien à faire
                            AFDC = automate_a_utiliser
                            print("\n✅ L'automate est déjà déterministe et complet.")
                        else:
                            # déterministe mais pas complet → on complète
                            AFDC = complete(automate_a_utiliser)
                            print("\n✅ Automate complété avec succès!")
                            AFDC.display()
                            automate_a_utiliser = AFDC
                    else:
                        # pas déterministe → on déterminise et complète
                        AFDC = determinize_and_complete(automate_a_utiliser)
                        print("\n✅ Automate déterminisé et complété avec succès!")
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
                print("\n✅ Automate complémentaire construit avec succès !")
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
                break

            elif choix == 'q':
                print("Au revoir !")
                exit()

            else:
                print("⚠️ Choix invalide, réessayez.")


if __name__ == "__main__":
    main()