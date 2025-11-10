# II. cloud-init

## 1. Intro

## 2. GO

➔ Sur votre PC, créez un fichier cloud-init.txt avec le contenu suivant :

### Tester cloud-init

- passer sur _wsl_

```bash
israel@hpvictusBJI:~$ chmod 400 ~/.ssh/cloud_tp
israel@hpvictusBJI:~$ eval $(ssh-agent -s)
Agent pid 697
israel@hpvictusBJI:~$ ssh-add ~/.ssh/cloud_tp
Enter passphrase for /home/israel/.ssh/cloud_tp:
Identity added: /home/israel/.ssh/cloud_tp (jerem@hpvictusBJI)
```

- en créant une nouvelle VM et en lui passant ce fichier cloud-init.txt au démarrage
- pour ça, utilisez une commande az vm create
- utilisez l'option `--custom-data /path/to/cloud-init.txt`

```bash
israel@hpvictusBJI:~$ az vm create -g azure-tp1 -n vm-cloudinit --image Ubuntu2404 --size Standard_B1s --location francecentral --ssh-key-
values /mnt/c/Users/jerem/.ssh/cloud_tp.pub --custom-data ~/cloud-init.txt
The default value of '--size' will be changed to 'Standard_D2s_v5' from 'Standard_DS1_v2' in a future release.
Selecting "northeurope" may reduce your costs. The region you've selected may cost more for the same services. You can disable this message in the future with the command "az config set core.display_region_identified=false". Learn more at https://go.microsoft.com/fwlink/?linkid=222571

{
  "fqdns": "",
  "id": "/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/azure-tp1/providers/Microsoft.Compute/virtualMachines/vm-cloudinit",
  "location": "francecentral",
  "macAddress": "60-45-BD-1A-92-F8",
  "powerState": "VM running",
  "privateIpAddress": "10.0.0.6",
  "publicIpAddress": "4.211.254.220",
  "resourceGroup": "azure-tp1"
}
```

### Vérifier que cloud-init a bien fonctionné

- connectez-vous en SSH à la VM nouvellement créée, directement sur le nouvel utilisateur créé par cloud-init

```bash
israel@hpvictusBJI:~$ cat cloud-init.txt
#cloud-config
users:
  - default
  - name: israel
    sudo: ALL=(ALL) NOPASSWD:ALL
    groups: sudo
    homedir: /home/israel
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIInis33LqQPGikPKLWayKlxM7UfQ1RjfgC09TNkk/sQv jerem@hpvictusBJI
  - name: admin
    sudo: ALL=(ALL) NOPASSWD:ALL
    homedir: /home/admin
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIInis33LqQPGikPKLWayKlxM7UfQ1RjfgC09TNkk/sQv jerem@hpvictusBJI

system_info:
  default_user:
    name: ""
```

```bash
israel@hpvictusBJI:~$ ssh -i .ssh/cloud_tp 4.211.254.220
The authenticity of host '4.211.254.220 (4.211.254.220)' can't be established.
ED25519 key fingerprint is SHA256:QJa9A/hD8FNgwxlvH1Wx95uLx6SJJnvP/3UXyLYqmMQ.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '4.211.254.220' (ED25519) to the list of known hosts.
Welcome to Ubuntu 24.04.3 LTS (GNU/Linux 6.14.0-1012-azure x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Tue Nov  4 21:54:42 UTC 2025

  System load:  0.19              Processes:             115
  Usage of /:   5.6% of 28.02GB   Users logged in:       0
  Memory usage: 29%               IPv4 address for eth0: 10.0.0.6
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
```

```bash
israel@vm-cloudinit:~$ cloud-init status
status: error
```

## 3. Write your own

Utilisez cloud-init pour preconfigurer une VM comme azure2.tp2 :

- ajoutez un user qui porte votre pseudo
  - il a un password défini
  - clé SSH publique déposée
  - il a accès aux droits de `root` via `sudo`

```bash
israel@hpvictusBJI:~$ cat cloud-init-db.txt
#cloud-config
users:
  - name: israel
    passwd: $6$y5DdzymQ0kBfib6f$quh4qmxjPrGThdLDDYgUyDmOVNo2dUCuVOS/Rl49zBn6AHL67kJ3OqHhUSyHlM/xcGBYlivlBCmdtAZ9/EXVu1
    sudo: ALL=(ALL) NOPASSWD:ALL
    groups: [sudo, adm]
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIInis33LqQPGikPKLWayKlxM7UfQ1RjfgC09TNkk/sQv jerem@hpvictusBJI
package_update: true
packages:
  - mariadb-server
write_files:
  - path: /tmp/init.sql
    content: |
      CREATE DATABASE meow_database;
      CREATE USER 'meow'@'%' IDENTIFIED BY 'meow';
      GRANT ALL ON meow_database.* TO 'meow'@'%';
      FLUSH PRIVILEGES;
runcmd:
  - 'sed -i "s/bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/mariadb.conf.d/50-server.cnf'
  - 'systemctl enable --now mariadb.service'
  - 'sleep 5'
  - 'mysql < /tmp/init.sql'
```

- installer MySQL sur la machine
- déposer un fichier `init.sql` qui contient les commandes SQL du TPI
- lance une commande `mysql` pour exécuter le contenu du script `init.sql`

```bash
israel@azure2:~$ systemctl status mariadb.service
● mariadb.service - MariaDB 10.11.13 database server
     Loaded: loaded (/usr/lib/systemd/system/mariadb.service; enabled; pres>
     Active: active (running) since Tue 2025-11-04 22:48:41 UTC; 5 days ago
       Docs: man:mariadbd(8)
             https://mariadb.com/kb/en/library/systemd/
   Main PID: 2668 (mariadbd)
     Status: "Taking your SQL requests now..."
      Tasks: 10 (limit: 6554)
     Memory: 86.4M (peak: 86.6M)
        CPU: 47.267s
     CGroup: /system.slice/mariadb.service
             └─2668 /usr/sbin/mariadbd

Nov 04 22:48:41 azure2 mariadbd[2668]: 2025-11-04 22:48:41 0 [Note] InnoDB:>
Nov 04 22:48:41 azure2 mariadbd[2668]: 2025-11-04 22:48:41 0 [Note] InnoDB:>
Nov 04 22:48:41 azure2 mariadbd[2668]: 2025-11-04 22:48:41 0 [Warning] You >
Nov 04 22:48:41 azure2 mariadbd[2668]: 2025-11-04 22:48:41 0 [Note] Server >
Nov 04 22:48:41 azure2 mariadbd[2668]: 2025-11-04 22:48:41 0 [Note] /usr/sb>
Nov 04 22:48:41 azure2 mariadbd[2668]: Version: '10.11.13-MariaDB-0ubuntu0.>
Nov 04 22:48:41 azure2 systemd[1]: Started mariadb.service - MariaDB 10.11.>
Nov 04 22:48:41 azure2 /etc/mysql/debian-start[2685]: Upgrading MariaDB tab>
Nov 04 22:48:41 azure2 /etc/mysql/debian-start[2696]: Checking for insecure>
Nov 04 22:48:41 azure2 /etc/mysql/debian-start[2701]: Triggering myisam-rec>

israel@azure2:~$ ls -l /tmp/init.sql
-rw-r--r-- 1 root root 138 Nov  4 22:47 /tmp/init.sql
```

### Testez que ça fonctionne

- un déploiement avec un `az vm create` en passant votre fichier `cloud-init.txt`
- connectez-vous en SSH, vérifiez que vous pouvez vous connecter au serveur de db (commande `mysql`) et que la base est créée

```bash
israel@hpvictusBJI:~$ az vm create -g azure-tp1 -n azure2.tp2 --image Ubuntu2404 --size Standard_B1s --public-ip-address "" --ssh-key-values ~/.ssh/cloud_tp.pub --custom-data ~/cloud-init-db.txt
The default value of '--size' will be changed to 'Standard_D2s_v5' from 'Standard_DS1_v2' in a future release.
Selecting "northeurope" may reduce your costs. The region you've selected may cost more for the same services. You can disable this message in the future with the command "az config set core.display_region_identified=false". Learn more at https://go.microsoft.com/fwlink/?linkid=222571

{
  "fqdns": "",
  "id": "/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/azure-tp1/providers/Microsoft.Compute/virtualMachines/azure2.tp2",
  "location": "francecentral",
  "macAddress": "7C-ED-8D-6D-4E-25",
  "powerState": "VM running",
  "privateIpAddress": "10.0.0.7",
  "publicIpAddress": "",
  "resourceGroup": "azure-tp1"
}
israel@hpvictusBJI:~$ ssh az2
The authenticity of host '10.0.0.7 (<no hostip for proxy command>)' can't be established.
ED25519 key fingerprint is SHA256:GBoaA0a3B9peOaIoZDE2pPhQDIRKdHw+34KSplX0oFo.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.0.0.7' (ED25519) to the list of known hosts.
Welcome to Ubuntu 24.04.3 LTS (GNU/Linux 6.14.0-1012-azure x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Wed Nov  5 22:16:39 UTC 2025

  System load:  0.04              Processes:             115
  Usage of /:   8.4% of 28.02GB   Users logged in:       0
  Memory usage: 42%               IPv4 address for eth0: 10.0.0.7
  Swap usage:   0%

 * Strictly confined Kubernetes makes edge and IoT secure. Learn how MicroK8s
   just raised the bar for easy, resilient and secure K8s cluster deployment.

   https://ubuntu.com/engage/secure-kubernetes-at-the-edge

Expanded Security Maintenance for Applications is not enabled.

15 updates can be applied immediately.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


*** System restart required ***

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
israel@azure2:~$ mysql -u meow -pmeow -h 127.0.0.1 -D meow_database -e "SHOW TABLES;"
israel@azure2:~$
```
