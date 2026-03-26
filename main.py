from automaton import  read_txt

def main():
    # Nom du fichier à lire
    filename = "../Projet_automate_python/automates_de_tests/A3.txt"

    # Lecture du fichier et création de l’automate
    automaton = read_txt(filename)

    # Affichage de l’automate
    automaton.display()

if __name__ == "__main__":
    main()