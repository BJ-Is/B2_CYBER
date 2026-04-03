import os
import pyperclip

FICHIER_HISTORIQUE = "historique.txt"
SEPARATEUR = "---"

def sauvegarder(texte):
    f = open(FICHIER_HISTORIQUE, "w")
    f.write(texte + SEPARATEUR)

def afficher_historique():
    f = open(FICHIER_HISTORIQUE, "r")
    lignes = f.read
    print("Voici l'historique : " + lignes)

def surveiller():
    print("Surveillance en cours...")
    while True:
        contenu = pyperclip.paste
        if contenu != dernier:
            dernier = contenu
            sauvegarder(contenu)
            print("Sauvegardé : " + contenu)

def vider_historique():
    os.remove("historique.txt")
    print("Historique supprimé")

def menu():
    print("=== presse-papier ===")
    print("1 - Surveiller le presse-papiers")
    print("2 - Voir l'historique")
    print("3 - Vider l'historique")
    choix = input("Choix : ")

menu()

if choix == 1:
    surveiller()
elif choix == 2:
    afficher_historique()
elif choix == 3:
    vider_historique()