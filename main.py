from automaton import read_txt, non_standard, standardisation  # Import explicite


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

        while True:
            print("\n── Que voulez-vous faire ? ─────────────────")
            print("  1. Standardiser l'automate")
            print("  2. Minimiser l'automate")
            print("  3. Rechercher un mot")
            print("  4. Changer d'automate")
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
                automate_minimise = automate_a_utiliser.minimize()
                automate_minimise.display_minimal()
                automate_a_utiliser = automate_minimise

            elif choix == '3':
                print(f"\nAlphabet reconnu : {automate_a_utiliser.alphabet}")
                while True:
                    mot = input("Entrez un mot à tester (ou 'c' pour revenir au menu) : ").strip()
                    if mot.lower() == 'c':
                        break
                    if not mot:
                        print("Veuillez entrer un mot non vide.")
                        continue
                    automate_a_utiliser.reconnaitre_mot(mot)

            elif choix == '4':
                break

            elif choix == 'q':
                print("Au revoir !")
                exit()

            else:
                print("⚠️ Choix invalide, réessayez.")


if __name__ == "__main__":
    main()