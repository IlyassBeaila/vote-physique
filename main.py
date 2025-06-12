import os
import sys

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def wait():
    input("\nAppuyez sur Entrée pour continuer...")

def header(title):
    #clear()
    print(f"==== {title} ====")

def run_script(path):
    os.system(f"python3 {path}")

def menu():
    while True:
        header("Système de Vote Électronique - Menu Principal")
        print("""
1. 🏛️ Générer l'autorité de certification (CA)
2. 👤 Inscrire les électeurs
3. 🔐 Authentifier un électeur
4. 🗳️ Voter
5. 🧮 Dépouiller les votes
6. 📤 Exporter les résultats signés
7. 🔍 Auditer les bulletins
8. 📄 Voir le procès-verbal
9. 🚪 Quitter
""")
        choice = input("Votre choix : ").strip()

        if choice == '1':
            run_script("authority/generate_ca.py")
        elif choice == '2':
            run_script("register/generate_electeurs.py")
            run_script("register/generate_cert.py")
            run_script("register/generate_cert_voter2.py")
            run_script("register/generate_cert_voter3.py")
        elif choice == '3':
            run_script("auth/challenge.py")
        elif choice == '4':
            run_script("vote/vote.py")
        elif choice == '5':
            run_script("tally/tally.py")
        elif choice == '6':
            run_script("tally/export_resultats.py")
        elif choice == '7':
            run_script("audit/audit.py")
        elif choice == '8':
            os.system("cat register/pv.json")
            wait()
        elif choice == '9':
            print("👋 Au revoir !")
            sys.exit()
        else:
            print("❌ Choix invalide.")
            wait()

if __name__ == "__main__":
    menu()
