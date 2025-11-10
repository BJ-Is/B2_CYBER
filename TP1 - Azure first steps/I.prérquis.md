## A. Choix de l'algorithme de chiffrement¶

## 🌞 Déterminer quel algorithme de chiffrement utiliser pour vos clés

\*vous n'utiliserez PAS RSA, vous choisirez un autre algorithme

\*donner un lien vers une source fiable qui explique pourquoi on évite RSA désormais (pour les connexions SSH notamment)

\*donner un lien vers une source fiable qui recommande un autre algorithme de chiffrement (pour les connexions SSH notamment)

## B. Génération de votre paire de clés¶

### 🌞 Générer une paire de clés pour ce TP

\* la clé privée doit s'appeler cloud_tp \* elle doit utiliser l'algorithme que vous avez choisi à l'étape précédente (donc, pas de RSA)
\*elle est protégée par un mot de passe (passphrase) de votre choix

```bash
PS C:\Users\jerem> ssh-keygen -t ed25519
Generating public/private ed25519 key pair.
Enter file in which to save the key (C:\Users\jerem/.ssh/id_ed25519): C:\Users\jerem/.ssh/cloud_tp
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in C:\Users\jerem/.ssh/cloud_tp
Your public key has been saved in C:\Users\jerem/.ssh/cloud_tp.pub
The key fingerprint is:
SHA256:NdSJNxPNmLM94YU2DM+zrtIbofoSOxN/umRgV4QAh5c jerem@hpvictusBJI
The key's randomart image is:
+--[ED25519 256]--+
|      .ooo.++X . |
|      ..E.o.XoO .|
|       .  o..O++ |
|         . o. +o |
|        S . . .. |
|       .oo . o   |
|         =+.. .  |
|        =+o oo   |
|        .=+=o.   |
+----[SHA256]-----+
```

\*elle doit se situer dans le dossier standard pour votre utilisateur (c'est ~/.ssh)
`Dans le compte-rendu, donnez toutes les commandes de génération de la clé. Prouvez aussi avec un ls sur votre clé qu'elle existe bien, au bon endroit.`

```bash

PS C:\Users\jerem> Get-ChildItem -Path C:\Users\jerem\.ssh


    Répertoire : C:\Users\jerem\.ssh


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        29/10/2025     22:25            464 cloud_tp
-a----        29/10/2025     22:25            100 cloud_tp.pub
```

C. Agent SSH

### 🌞 Configurer un agent SSH sur votre poste

- on ne saisit le mot de passe (passphrase) qui protège la clé qu'une seule fois : au moment du ssh-add
- détaillez-moi toute la conf ici que vous aurez fait

```bash
PS C:\Users\jerem> start-service ssh-agent
PS C:\Users\jerem> Get-Service "ssh-agent"

Status   Name               DisplayName
------   ----               -----------
Running  ssh-agent          OpenSSH Authentication Agent

PS C:\Users\jerem> ssh-add .\.ssh\cloud_tp
Enter passphrase for .\.ssh\cloud_tp:
Identity added: .\.ssh\cloud_tp (jerem@hpvictusBJI)
```
