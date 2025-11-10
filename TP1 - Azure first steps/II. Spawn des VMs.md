## 1. Depuis la WebUI¶

`➜ Faites du cliclic partout dans la WebUI Azure pour créer une VM dans Azure.`

- choisissez un nom de user custom
- utilisez la clé publique générée pendant les prérequis

## 🌞 Connectez-vous en SSH à la VM pour preuve

- cette connexion ne doit demander aucun password : votre clé a été ajoutée à votre Agent SSH

```bash
PS C:\Users\jerem> ssh israel@4.178.170.153
Welcome to Ubuntu 24.04.3 LTS (GNU/Linux 6.14.0-1012-azure x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Fri Oct 31 13:47:17 UTC 2025

  System load:  0.0               Processes:             113
  Usage of /:   7.2% of 28.02GB   Users logged in:       0
  Memory usage: 36%               IPv4 address for eth0: 172.17.0.4
  Swap usage:   0%


Expanded Security Maintenance for Applications is not enabled.

15 updates can be applied immediately.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


*** System restart required ***
Last login: Fri Oct 31 13:45:04 2025 from 37.67.81.202
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

israel@israel1:~$

```

## 🌞 Créez une VM depuis le Azure CLI : azure1.tp1

- en utilisant uniquement la commande az donc
- je vous laisse faire vos recherches pour créer une VM avec la commande az
- vous devrez préciser :

- quel utilisateur doit être créé à la création de la VM
- le fichier de clé utilisé pour se connecter à cet utilisateur
- comme ça, dès que la VM pop, on peut se co en SSH !

```bash
PS C:\Users\jerem> az group create --location FranceCentral --name azure-tp1
{
  "id": "/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/azure-tp1",
  "location": "francecentral",
  "managedBy": null,
  "name": "azure-tp1",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": "Microsoft.Resources/resourceGroups"
}

```

```bash
PS C:\Users\jerem> az vm create -g azure-tp1 -n azure1.tp1 --image Ubuntu2204 --admin-username israel --ssh-key-values C:\Users\jerem\.ssh\cloud_tp.pub --size Standard_B1s
The default value of '--size' will be changed to 'Standard_D2s_v5' from 'Standard_DS1_v2' in a future release.
Selecting "northeurope" may reduce your costs. The region you've selected may cost more for the same services. You can disable this message in the future with the command "az config set core.display_region_identified=false". Learn more at https://go.microsoft.com/fwlink/?linkid=222571

{
  "fqdns": "",
  "id": "/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/azure-tp1/providers/Microsoft.Compute/virtualMachines/azure1.tp1",
  "location": "francecentral",
  "macAddress": "7C-ED-8D-6D-46-65",
  "powerState": "VM running",
  "privateIpAddress": "10.0.0.4",
  "publicIpAddress": "52.143.163.228",
  "resourceGroup": "azure-tp1"
}
```

🌞 Assurez-vous que vous pouvez vous connecter à la VM en SSH sur son IP publique

```bash
ssh israel@52.143.163.228
The authenticity of host '52.143.163.228 (52.143.163.228)' can't be established.
ED25519 key fingerprint is SHA256:mvzbSULiOZr00Gr84EePTKzjfMhfPnQUuUu/W3jndU0.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '52.143.163.228' (ED25519) to the list of known hosts.
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-1041-azure x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Fri Oct 31 14:23:58 UTC 2025

  System load:  0.08              Processes:             106
  Usage of /:   5.5% of 28.89GB   Users logged in:       0
  Memory usage: 31%               IPv4 address for eth0: 10.0.0.4
  Swap usage:   0%

Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

israel@azure1:~$
```

## 🌞 Une fois connecté, prouvez la présence...

- ...du service walinuxagent.service

```bash
israel@azure1:~$ systemctl status walinuxagent.service
● walinuxagent.service - Azure Linux Agent
     Loaded: loaded (/lib/systemd/system/walinuxagent.service; enabled; vendor preset: enabled)
    Drop-In: /usr/lib/systemd/system/walinuxagent.service.d
             └─10-Slice.conf
             /run/systemd/system.control/walinuxagent.service.d
             └─50-CPUAccounting.conf, 50-MemoryAccounting.conf
     Active: active (running) since Fri 2025-10-31 14:16:32 UTC; 10min ago
   Main PID: 786 (python3)
      Tasks: 7 (limit: 1009)
     Memory: 48.6M
        CPU: 2.747s
     CGroup: /system.slice/walinuxagent.service
             ├─ 786 /usr/bin/python3 -u /usr/sbin/waagent -daemon
             └─1081 python3 -u bin/WALinuxAgent-2.15.0.1-py3.12.egg -run-exthandlers

Oct 31 14:16:42 azure1 python3[1081]:        0        0 ACCEPT     tcp  --  *      *       0.0.0.0/0            168.63.129.16        tcp >
Oct 31 14:16:42 azure1 python3[1081]:        5     1415 ACCEPT     tcp  --  *      *       0.0.0.0/0            168.63.129.16        owne>
Oct 31 14:16:42 azure1 python3[1081]:        0        0 DROP       tcp  --  *      *       0.0.0.0/0            168.63.129.16        ctst>
Oct 31 14:16:42 azure1 python3[1081]: 2025-10-31T14:16:42.754120Z INFO ExtHandler ExtHandler Looking for existing remote access users.
Oct 31 14:16:42 azure1 python3[1081]: 2025-10-31T14:16:42.762043Z INFO ExtHandler ExtHandler [HEARTBEAT] Agent WALinuxAgent-2.15.0.1 is r>
Oct 31 14:21:42 azure1 python3[1081]: 2025-10-31T14:21:42.589078Z INFO CollectLogsHandler ExtHandler WireServer endpoint 168.63.129.16 re>
Oct 31 14:21:42 azure1 python3[1081]: 2025-10-31T14:21:42.589308Z INFO CollectLogsHandler ExtHandler Wire server endpoint:168.63.129.16
Oct 31 14:21:42 azure1 python3[1081]: 2025-10-31T14:21:42.589455Z INFO CollectLogsHandler ExtHandler Starting log collection...
Oct 31 14:21:55 azure1 python3[1081]: 2025-10-31T14:21:55.858569Z INFO CollectLogsHandler ExtHandler Successfully collected logs. Archive>
Oct 31 14:21:55 azure1 python3[1081]: 2025-10-31T14:21:55.879661Z INFO CollectLogsHandler ExtHandler Successfully uploaded logs.
lines 1-25/25 (END)
```

- ...du service cloud-init.service

```bash
israel@azure1:~$ systemctl status cloud-init.service
● cloud-init.service - Cloud-init: Network Stage
     Loaded: loaded (/lib/systemd/system/cloud-init.service; enabled; vendor preset: enabled)
     Active: active (exited) since Fri 2025-10-31 14:16:32 UTC; 12min ago
   Main PID: 521 (code=exited, status=0/SUCCESS)
        CPU: 2.631s

Oct 31 14:16:32 azure1 cloud-init[525]: |          o      |
Oct 31 14:16:32 azure1 cloud-init[525]: |           o     |
Oct 31 14:16:32 azure1 cloud-init[525]: |          +      |
Oct 31 14:16:32 azure1 cloud-init[525]: |     .. So o    E|
Oct 31 14:16:32 azure1 cloud-init[525]: |     ++*. o .. ..|
Oct 31 14:16:32 azure1 cloud-init[525]: |   o+*O+o.. ..o =|
Oct 31 14:16:32 azure1 cloud-init[525]: |   +BB==o+ ..o oo|
Oct 31 14:16:32 azure1 cloud-init[525]: |   oB*+ +oo ..  .|
Oct 31 14:16:32 azure1 cloud-init[525]: +----[SHA256]-----+
Oct 31 14:16:32 azure1 systemd[1]: Finished Cloud-init: Network Stage.
```

## 3. Spawn moar moar moaaar VMs¶

## A. Another VM another friend :d¶

## 🌞 Créez une deuxième VM : azure2.tp1

- avec une commande az
- elle ne doit PAS avoir d'adresse IP publique

```bash
PS C:\Users\jerem> az vm create -g azure-tp1 -n azure2.tp1 --image Ubuntu2204 --admin-username israel --ssh-key-values C:\Users\jerem\.ssh\cloud_tp.pub --size Standard_B1s --public-ip-address '""'
The default value of '--size' will be changed to 'Standard_D2s_v5' from 'Standard_DS1_v2' in a future release.
Selecting "northeurope" may reduce your costs. The region you've selected may cost more for the same services. You can disable this message in the future with the command "az config set core.display_region_identified=false". Learn more at https://go.microsoft.com/fwlink/?linkid=222571

{
  "fqdns": "",
  "id": "/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/azure-tp1/providers/Microsoft.Compute/virtualMachines/azure2.tp1",
  "location": "francecentral",
  "macAddress": "7C-ED-8D-6D-7A-DF",
  "powerState": "VM running",
  "privateIpAddress": "10.0.0.5",
  "publicIpAddress": "",
  "resourceGroup": "azure-tp1"
}
```

## 🌞 Affichez des infos au sujet de vos deux VMs

- avec une/des commande(s) az
- on doit voir :

- que azure1.tp1 a une adresse IP publique et une adresse IP privée
- que azure2.tp1 n'a PAS d'adresse IP publique mais a une adresse IP privée

```bash
PS C:\Users\jerem> az vm list-ip-addresses --resource-group azure-tp1 -o table
VirtualMachine    PublicIPAddresses    PrivateIPAddresses
----------------  -------------------  --------------------
azure1.tp1        52.143.163.228       10.0.0.4
azure2.tp1                             10.0.0.5
```

B. Config SSH client

## 🌞 Configuration SSH client pour les deux machines

- 📁 dans le compte-rendu, livez-moi juste votre fichier config et les deux commandes SSH fonctionnelles

* vous devez rebondir sur azure1.tp1 (car c'est la seule exposée sur internet) pour

- accéder à azure2.tp1

* vous devez utiliser un fichier config SSH client, pour que ces deux commandes
* fonctionnent juste :

```bash
PS C:\Users\jerem> ssh az1
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-1041-azure x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Fri Oct 31 17:51:18 UTC 2025

  System load:  0.0               Processes:             104
  Usage of /:   5.6% of 28.89GB   Users logged in:       0
  Memory usage: 29%               IPv4 address for eth0: 10.0.0.4
  Swap usage:   0%


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
New release '24.04.3 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


Last login: Fri Oct 31 15:34:31 2025 from 37.67.81.202
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

israel@azure1:~$
```

```bash
PS C:\Users\jerem> ssh az2
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-1041-azure x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Fri Oct 31 17:55:24 UTC 2025

  System load:  0.08              Processes:             106
  Usage of /:   5.5% of 28.89GB   Users logged in:       0
  Memory usage: 30%               IPv4 address for eth0: 10.0.0.5
  Swap usage:   0%

Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

israel@azure2:~$
```

```bash
PS C:\Users\jerem> get-content .\.ssh\config
Host pano
  HostName 4.178.170.153
  User israel
  Port 22
  IdentityFile C:\Users\jerem\.ssh\cloud_tp
  StrictHostKeyChecking no

Host az1
    HostName 52.143.163.228
    User israel
    Port 22
    ForwardAgent yes

Host az2
    HostName 10.0.0.5
    User israel
    Port 22
    ProxyJump az1
```

## 🌞 Ouvrez un port firewall si nécessaire

- pour rappel vous pouvez faire un sudo ss -lnpt pour savoir sur quel \* \* port tourne votre serveur de base de données
- ce port doit être joignable par la machine azure1.tp1

```bash
israel@azure2:~$ sudo ss -lnpt | grep 3306
LISTEN 0      80         127.0.0.1:3306      0.0.0.0:*    users:(("mariadbd",pid=2954,fd=21))
israel@azure2:~$ sudo ss -lnpt | grep 3306
LISTEN 0      80           0.0.0.0:3306
israel@azure2:~$ sudo ufw allow from 10.0.0.4 to any port 3306 proto tcp
Rules updated
```

## 2. Machine azure1.tp1

'Ici on va déployer le site web.'

Au menuuu :

1. récupération de l'application sur la machine
2. installation des dépendances de l'application
3. configuration de l'application
4. gestion de users et de droits
5. création d'un service webapp.service pour lancer l'application
6. ouverture du port dans le firewall si nécessaire
7. lancement du service
8. Let's goooo 🔥🔥

```bash
israel@azure1:/opt/meow$ ls -la /opt/meow
total 52
drwxr-xr-x 7 root root 4096 Nov  1 10:57 .
drwxr-xr-x 3 root root 4096 Nov  1 09:39 ..
-rw-r--r-- 1 root root  313 Nov  1 10:55 .env
drwxr-xr-x 8 root root 4096 Nov  1 10:18 .git
-rw-r--r-- 1 root root   15 Nov  1 10:18 .gitignore
-rw-r--r-- 1 root root  213 Nov  1 10:18 .gitlab-ci.yml
-rw-r--r-- 1 root root 3827 Nov  1 10:56 app.py
drwxr-xr-x 2 root root 4096 Nov  1 10:57 bin
drwxr-xr-x 2 root root 4096 Nov  1 10:57 include
drwxr-xr-x 3 root root 4096 Nov  1 10:57 lib
lrwxrwxrwx 1 root root    3 Nov  1 10:57 lib64 -> lib
-rw-r--r-- 1 root root   71 Nov  1 10:57 pyvenv.cfg
-rw-r--r-- 1 root root   58 Nov  1 10:55 requirements.txt
drwxr-xr-x 2 root root 4096 Nov  1 10:57 templates
```

## B. Installation des dépendances de l'application

## 🌞 Installation des dépendances de l'application

- déplacez-vous dans le dossier de l'application
- exécutez les commandes suivantes :

```bash
israel@azure1:/opt/meow$ sudo python3 -m venv .
israel@azure1:/opt/meow$ sudo ./bin/pip install -r requirements.txt
Collecting Flask
  Downloading flask-3.1.2-py3-none-any.whl (103 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 103.3/103.3 KB 3.1 MB/s eta 0:00:00
Collecting Flask-SQLAlchemy
  Downloading flask_sqlalchemy-3.1.1-py3-none-any.whl (25 kB)
Collecting PyMySQL
  Downloading pymysql-1.1.2-py3-none-any.whl (45 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 45.3/45.3 KB 6.3 MB/s eta 0:00:00
Collecting python-dotenv
  Downloading python_dotenv-1.2.1-py3-none-any.whl (21 kB)
Collecting cryptography
  Downloading cryptography-46.0.3-cp38-abi3-manylinux_2_34_x86_64.whl (4.5 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.5/4.5 MB 16.4 MB/s eta 0:00:00
Collecting itsdangerous>=2.2.0
  Downloading itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Collecting markupsafe>=2.1.1
  Downloading markupsafe-3.0.3-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (20 kB)
Collecting blinker>=1.9.0
  Downloading blinker-1.9.0-py3-none-any.whl (8.5 kB)
Collecting werkzeug>=3.1.0
  Downloading werkzeug-3.1.3-py3-none-any.whl (224 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 224.5/224.5 KB 23.6 MB/s eta 0:00:00
Collecting jinja2>=3.1.2
  Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 134.9/134.9 KB 21.0 MB/s eta 0:00:00
Collecting click>=8.1.3
  Downloading click-8.3.0-py3-none-any.whl (107 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 107.3/107.3 KB 13.6 MB/s eta 0:00:00
Collecting sqlalchemy>=2.0.16
  Downloading sqlalchemy-2.0.44-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.2/3.2 MB 30.4 MB/s eta 0:00:00
Collecting typing-extensions>=4.13.2
  Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 44.6/44.6 KB 5.4 MB/s eta 0:00:00
Collecting cffi>=2.0.0
  Downloading cffi-2.0.0-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (216 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 216.5/216.5 KB 23.2 MB/s eta 0:00:00
Collecting pycparser
  Downloading pycparser-2.23-py3-none-any.whl (118 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 118.1/118.1 KB 13.9 MB/s eta 0:00:00
Collecting greenlet>=1
  Downloading greenlet-3.2.4-cp310-cp310-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (584 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 584.4/584.4 KB 27.6 MB/s eta 0:00:00
Installing collected packages: typing-extensions, python-dotenv, PyMySQL, pycparser, markupsafe, itsdangerous, greenlet, click, blinker, werkzeug, sqlalchemy, jinja2, cffi, Flask, cryptography, Flask-SQLAlchemy
Successfully installed Flask-3.1.2 Flask-SQLAlchemy-3.1.1 PyMySQL-1.1.2 blinker-1.9.0 cffi-2.0.0 click-8.3.0 cryptography-46.0.3 greenlet-3.2.4 itsdangerous-2.2.0 jinja2-3.1.6 markupsafe-3.0.3 pycparser-2.23 python-dotenv-1.2.1 sqlalchemy-2.0.44 typing-extensions-4.15.0 werkzeug-3.1.3
```

C. Configuration de l'application¶
🌞 Configuration de l'application

modifier le fichier /opt/meow/.env
modifier uniquement la valeur de DB_HOST pour indiquer l'adresse IP de azure2.tp1

```bash
israel@azure1:/opt/meow$ cat .env
# Flask Configuration
FLASK_SECRET_KEY=ewnFw95H7qBeGiVvkQl9YmnJohW6NCMMqR0arxfnWYASeCDvzwQwzLxMCboAOi3e
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=8000

# Database Configuration
DB_HOST=10.0.0.5
DB_PORT=3306
DB_NAME=meow_database
DB_USER=meow
DB_PASSWORD=meow
```

D. Gestion de users et de droits¶
🌞 Gestion de users et de droits

créez un utilisateur webapp (commande useradd)
le dossier /opt/meow et tout son contenu doivent appartenir (commande chown) :

au user webapp
au groupe webapp
les "autres" ne doivent avoir aucun droit sur ce dossier et son contenu (commande chmod)

```bash
israel@azure1:/opt/meow$ sudo useradd webapp
israel@azure1:/opt/meow$ sudo chown -R webapp:webapp /opt/meow
israel@azure1:/opt/meow$ sudo chmod -R 770 /opt/meow
```

E. Création d'un service webapp.service pour lancer l'application¶
🌞 Création d'un service webapp.service pour lancer l'application

créez le fichier /etc/systemd/system/webapp.service
il doit avoir le contenu suivant :

```bash
israel@azure1:/opt/meow$
sudo nano /etc/systemd/system/webapp.service
israel@azure1:/opt/meow$ sudo systemctl daemon-reload
israel@azure1:/opt/meow$ cat /etc/systemd/system/webapp.service
[Unit]
Description=Super Webapp MEOW

[Service]
User=webapp
Group=webapp
WorkingDirectory=/opt/meow
ExecStart=/opt/meow/bin/python app.py

[Install]
WantedBy=multi-user.target
```

F. Ouverture du port dans le(s) firewall(s)¶
🌞 Ouverture du port80 dans le(s) firewall(s)

vous pouvez voir le port utilisé par l'application :

dans ses logs (journalctl)
ou en demandant à l'OS (ss)
ou en regardant sa conf (fichier .env)
suivant l'OS que vous avez choisi, la commande pourra changer pour ouvrir le port, je vous laisse chercher

probablement une commande ufw sur Ubuntu
probablement une commande firewall-cmd sur Rocky
etc.
n'oubliez pas d'ouvrir aussi le port dans le firewall Azure

faites-le depuis la WebUI

```bash
israel@azure1:/opt/meow$ sudo ufw allow 8000/tcp
Rules updated
Rules updated (v6)
```

3. Visitez l'application¶
   🌞 L'application devrait être fonctionnelle sans soucis à partir de là

vous pouvez visiter http://<\_IP_PUBLIQUE_DE_azure1.tp1>:8000
vérifier que l'app fonctionne en postant un message
mettez-moi un curl vers l'URL dans le compte-rendu (juste les premières lignes svp ça ira)

```bash
israel@azure1:/opt/meow$ exit
logout
Connection to 52.143.163.228 closed.
PS C:\Users\jerem> curl http://52.143.163.228:8000


StatusCode        : 200
StatusDescription : OK
Content           : <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Purr Messages - Cat Message Board</title>
                        <...
RawContent        : HTTP/1.1 200 OK
                    Connection: close
                    Content-Length: 12566
                    Content-Type: text/html; charset=utf-8
                    Date: Sat, 01 Nov 2025 13:56:20 GMT
                    Server: Werkzeug/3.1.3 Python/3.10.12

                    <!DOCTYPE html>
                    <html l...
Forms             : {messageForm}
Headers           : {[Connection, close], [Content-Length, 12566], [Content-Type, text/html; charset=utf-8], [Date, Sat, 01 Nov 2025
                    13:56:20 GMT]...}
Images            : {}
InputFields       : {@{innerHTML=; innerText=; outerHTML=<INPUT id=username class=form-input maxLength=50 required placeholder="Your
                    name...">; outerText=; tagName=INPUT; id=username; class=form-input; maxLength=50; required=; placeholder=Your
                    name...}}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 12566
```

```bash

```
