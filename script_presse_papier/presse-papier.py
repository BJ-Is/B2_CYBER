"""Gestionnaire d'historique du presse-papiers."""

import os
import time

import pyperclip  

FICHIER_HISTORIQUE = "historique.txt"
SEPARATEUR = "---"
INTERVALLE = 1  



def sauvegarder(texte):
    """Ajoute un texte copié dans le fichier historique."""
    with open(FICHIER_HISTORIQUE, "a", encoding="utf-8") as f:
        f.write(texte + "\n" + SEPARATEUR + "\n")


def afficher_historique():
    """Lit et affiche tout l'historique."""
    if not os.path.exists(FICHIER_HISTORIQUE):
        print("Aucun historique trouvé.")
        return

    with open(FICHIER_HISTORIQUE, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    numero = 1
    bloc = []
    for ligne in lignes:
        if ligne.strip() == SEPARATEUR: # if " ---\n" == "---"
            contenu = " ".join(bloc).strip() # permet de mettre bout à bout chaque items de la listes en sup les "\n" 
            print(f"\n[{numero}] {contenu}") # on associe chaque numéro dans l'ordre avec le texte copier
            numero += 1 
            bloc = []
        else:
            bloc.append(ligne) # qui correspond à "notre séparateur en haut"


def surveiller():
    """Surveille le presse-papiers et sauvegarde les nouveaux textes."""
    print("Surveillance en cours... (Ctrl+C pour arrêter)\n")
    dernier = ""

    try:
        while True:
            contenu = pyperclip.paste() # correspond au texte qu'on n'a copier
            if contenu and contenu != dernier: # voir si ils sont les même
                dernier = contenu
                sauvegarder(contenu)
                apercu = contenu[:50].replace("\n", " ")
                print(f"Sauvegardé : {apercu}")
            time.sleep(INTERVALLE)

    except KeyboardInterrupt:
        print("\nSurveillance arrêtée.")


def vider_historique():
    """Supprime tout le fichier historique."""
    try:
        os.remove(FICHIER_HISTORIQUE)
        print("Historique supprimé.")
    except FileNotFoundError:
        print("Aucun historique à supprimer.")


def menu():
    """Affiche le menu principal."""
    print("=== presse-papier ===")
    print("1 - Surveiller le presse-papiers")
    print("2 - Voir l'historique")
    print("3 - Vider l'historique")
    return input("Choix : ").strip()



if __name__ == "__main__":
    choix = menu()

    if choix == "1":
        surveiller()
    elif choix == "2":
        afficher_historique()
    elif choix == "3":
        vider_historique()
    else:
        print("Choix invalide.")