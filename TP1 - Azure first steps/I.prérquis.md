## A. Choix de l'algorithme de chiffrement¶

## 🌞 Déterminer quel algorithme de chiffrement utiliser pour vos clés

vous n'utiliserez PAS RSA, vous choisirez un autre algorithme
donner un lien vers une source fiable qui explique pourquoi on évite RSA désormais (pour les connexions SSH notamment)
donner un lien vers une source fiable qui recommande un autre algorithme de chiffrement (pour les connexions SSH notamment)
Ca peut être le même lien pour les deux bien sûr, s'il parle des deux.

## B. Génération de votre paire de clés¶

### 🌞 Générer une paire de clés pour ce TP

la clé privée doit s'appeler cloud_tp
elle doit se situer dans le dossier standard pour votre utilisateur (c'est ~/.ssh)
elle doit utiliser l'algorithme que vous avez choisi à l'étape précédente (donc, pas de RSA)
elle est protégée par un mot de passe (passphrase) de votre choix
Dans le compte-rendu, donnez toutes les commandes de génération de la clé. Prouvez aussi avec un ls sur votre clé qu'elle existe bien, au bon endroit.

C. Agent SSH
