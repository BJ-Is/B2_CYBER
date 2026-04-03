# Clipboard Manager

Gestionnaire d'historique du presse-papiers en Python terminal.
Sauvegarde tout ce que tu copie dans un fichier texte.

---

## Installation

```bash
pip install pyperclip
```

---

## Lancer le script

```bash
python presse-papier.py
```

---

## Menu

**presse-papier**

- 1 - Surveiller le presse-papiers
  2 - Voir l'historique
  3 - Vider l'historique

- **1** → Lance la surveillance. Copie du texte n'importe où, il sera sauvegardé automatiquement. Arrêter avec `Ctrl+C`.
- **2** → Affiche tout l'historique numéroté.
- **3** → Supprime le fichier historique.

---

## Fichiers

| Fichier            | Rôle                                         |
| ------------------ | -------------------------------------------- |
| `presse-papier.py` | Script principal                             |
| `historique.txt`   | Historique des copies (créé automatiquement) |

---

## Compatibilité

| OS              | Fonctionne               |
| --------------- | ------------------------ |
| Windows         | **ok**                   |
| macOS           | **ok**                   |
| Linux (X11)     | **ok**                   |
| Linux (Wayland) | Nécessite `wl-clipboard` |

```bash
# Linux Wayland uniquement
sudo apt install wl-clipboard
```

---

## Projet

- Cours : Scripting Python B2 CS
- Librairie externe : `pyperclip`
