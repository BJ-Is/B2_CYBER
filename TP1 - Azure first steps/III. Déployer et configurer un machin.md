# Machine azure2.tp1

Oui, on commence par **azure2.tp1**. Ce n'est pas une erreur.

Nous allons configurer un serveur de base de données sur **azure2.tp1**.  
En effet, mon application (que nous lancerons plus tard sur **azure1.tp1**) a besoin d'une base SQL classique pour fonctionner.

---

## 🌞 Installer MySQL/MariaDB sur azure2.tp1

Faites vos recherches pour cela, en fonction de l'OS que vous avez choisi.

```bash

```

---

## 🌞 Démarrer le service MySQL/MariaDB sur azure2.tp1

Utilisez une commande `systemctl` pour démarrer le service.

```bash
israel@azure2:~$ sudo systemctl enable mariadb.service
Synchronizing state of mariadb.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable mariadb
```

---

## 🌞 Ajouter un utilisateur dans la base de données pour que mon app puisse s'y connecter

Connectez-vous à la base de données pour pouvoir l'administrer en SQL.

### Caractéristiques attendues de l'utilisateur :

- Nom d'utilisateur : `meow`
- Mot de passe : `meow`
- Connexion autorisée depuis **n'importe quelle machine**
- Droits : **tous les droits** sur la base de données `meow_database`

```bash

MariaDB [(none)]> CREATE DATABASE meow_database;
Query OK, 1 row affected (0.001 sec)
MariaDB [(none)]> CREATE USER 'meow'@'%' IDENTIFIED BY 'meow';
Query OK, 0 rows affected (0.011 sec)

MariaDB [(none)]> GRANT ALL ON meow_database.* TO 'meow'@'%';
Query OK, 0 rows affected (0.004 sec)

MariaDB [(none)]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.001 sec)

MariaDB [(none)]> EXIT;
Bye
```
