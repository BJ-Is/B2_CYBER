## 2. Une paire de clés SSH

On parle dans cette section uniquement de **votre paire de clés** à générer depuis votre poste, pour sécuriser vos connexions SSH.

Ha et on va aussi **configurer un Agent SSH**.

**ON VA BOSSER CORRECTEMENT QUOI** 👀

### A. Choix de l'algorithme de chiffrement

**Déterminer quel algorithme de chiffrement utiliser pour vos clés**

- vous n'utiliserez **PAS RSA**
- donner une source fiable qui explique pourquoi on évite RSA désormais (pour les connexions SSH notamment)
- donner une source fiable qui recommande un autre algorithme de chiffrement (pour les connexions SSH notamment)

### B. Génération de votre paire de clés

**Générer une paire de clés pour ce TP**

- la clé privée doit s'appeler `cloud_tp1`
- elle doit se situer dans le dossier standard pour votre utilisateur
- elle doit utiliser l'algorithme que vous avez choisi à l'étape précédente (donc pas de RSA)
- elle est protégée par un mot de passe de votre choix

### C. Agent SSH

Afin de ne pas systématiquement saisir le mot de passe d'une clé à chaque fois qu'on l'utilise, parce que **c'est très chiant**, on peut utiliser un **Agent SSH**.

Un programme qui tourne en fond, auquel on ajoute nos clés SSH, qui peuvent ensuite être utilisées dès qu'on fait une connexion SSH.

L'avantage est qu'on ne saisit le password qu'au moment de l'ajout de la clé SSH à l'agent !

**???+ info**

Oh et y'a moyen de le faire sous tous les OS. Comme d'hab, sous Linux/MacOS, moins relou :d  
Peu importe l'OS, ça finira par taper un petit `ssh-add` pour ajouter votre clé à l'agent normalement !

**Configurer un agent SSH sur votre poste**

- détaillez-moi toute la conf que vous aurez fait

```bash
israel@hpvictusBJI:~$ ssh-keygen -t ed25519 -f ~/.ssh/cloud_tp1 -C "cloud_tp1"
Generating public/private ed25519 key pair.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/israel/.ssh/cloud_tp1
Your public key has been saved in /home/israel/.ssh/cloud_tp1.pub
```

```bash
israel@hpvictusBJI:~/terraform$ ls ~/.ssh/cloud_tp1*
/home/israel/.ssh/cloud_tp1  /home/israel/.ssh/cloud_tp1.pub
```

```bash
israel@hpvictusBJI:~$ eval "$(ssh-agent -s)"
Agent pid 2432
israel@hpvictusBJI:~$ ssh-add ~/.ssh/cloud_tp1
Enter passphrase for /home/israel/.ssh/cloud_tp1:
Identity added: /home/israel/.ssh/cloud_tp1 (cloud_tp1)
```

```bash
israel@hpvictusBJI:~$ cat ~/.local/bin/az
#!/bin/bash
declare -r CT_PUBKEY_DIR='/tmp/ssh'
declare -r TEMP_SSH="$(mktemp -d)"
cp ~/.ssh/*.pub "${TEMP_SSH}"
chmod 755 "${TEMP_SSH}" -R

TTY_DOCKER_ARGS=''
if [[ -t 1 ]]; then
  TTY_DOCKER_ARGS='-it'
fi

docker run \
  -v "${TEMP_SSH}":"${CT_PUBKEY_DIR}" \
  -v az_login_volume:/home/nonroot \
  -u 65532 \
  --dns 8.8.8.8 \
  ${TTY_DOCKER_ARGS} \
  --rm \
  mcr.microsoft.com/azure-cli \
  az "$@"
israel@hpvictusBJI:~$
```
