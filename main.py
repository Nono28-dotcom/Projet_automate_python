from automaton import read_txt, non_standard, standardisation  # Import explicite


def main():
    while True:
        numero = input("\nNuméro de l'automate à charger (ou 'q' pour quitter) : ").strip()

        if numero.lower() == 'q':
            print("Au revoir !")
            break

        filename = f"../Projet_automate_python/automates_de_tests/A{numero}.txt"
        automaton = read_txt(filename)  # automaton est une instance de la classe Automaton

        # Affichage de l'automate
        automaton.display()

        # Variable pour stocker l'automate à utiliser
        automate_a_utiliser = automaton

        # Gestion de la standardisation
        if non_standard(automaton):
            reponse = input("\nVoulez-vous standardiser l'automate ? (o/n) : ").strip().lower()
            if reponse == 'o':
                SFA = standardisation(automaton)
                SFA.display()
                automate_a_utiliser = SFA  # SFA est aussi une instance de la classe Automaton
                print("✅ Automate standardisé avec succès!")

        # Recherche de mot
        choix_recherche = input("\nSouhaitez-vous rechercher un mot dans l'automate ? (oui/non) : ")

        if choix_recherche.lower() == 'oui':
            print(f"\n🔍 Alphabet reconnu : {automate_a_utiliser.alphabet}")

            while True:
                mot = input("Entrez un mot à tester (ou 'c' pour changer d'automate) : ").strip()

                if mot.lower() == 'c':
                    print("↩️ Retour à la sélection...")
                    break

                if not mot:
                    print("⚠️ Veuillez entrer un mot non vide.")
                    continue

                # Appel de la méthode reconnaitre_mot de la classe Automaton
                resultat = automate_a_utiliser.reconnaitre_mot(mot)

                if resultat:
                    print(f"✅ Le mot '{mot}' est reconnu.")
                else:
                    print(f"❌ Le mot '{mot}' n'est pas reconnu.")
        else:
            print("D'accord, au revoir !")
            break


if __name__ == "__main__":
    main()