from automaton import  *

def main():
    while True:
        numero = input("\nNuméro de l'automate à charger (ou 'q' pour quitter) : ").strip()

        if numero.lower() == 'q':
            print("Au revoir !")
            break

        filename = f"../Projet_automate_python/automates_de_tests/A{numero}.txt"
        automaton = read_txt(filename)

        # Affichage de l'automate
        automaton.display()


        if non_standard(automaton):
            reponse = input("\nVoulez-vous standardiser l'automate ? (o/n) : ").strip().lower()
            if reponse == 'o':
                SFA = standardisation(automaton)
                SFA.display()
                automaton = SFA






if __name__ == "__main__":
    main()