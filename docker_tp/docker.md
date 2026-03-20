### 1. Install

🌞 **Installer Docker votre machine Azure**

- en suivant la doc officielle

- démarrer le service docker avec une commande systemctl

- ajouter votre utilisateur au groupe docker
  - cela permet d'utiliser Docker sans avoir besoin de l'identité de root

  - avec la commande : sudo usermod -aG docker $(whoami)

  - déconnectez-vous puis relancez une session pour que le changement prenne effet

```bash
azureuser@docis:~$ sudo systemctl status docker
● docker.service - Docker Application Container Engine
     Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; prese>
     Active: active (running) since Thu 2026-03-19 14:24:33 UTC; 17h ago
TriggeredBy: ● docker.socket
       Docs: https://docs.docker.com
   Main PID: 913 (dockerd)
      Tasks: 11
     Memory: 116.0M (peak: 152.2M)
        CPU: 8.646s
     CGroup: /system.slice/docker.service
             └─913 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/c>

Mar 19 14:27:04 docis dockerd[913]: time="2026-03-19T14:27:04.614341599Z" l>
Mar 19 14:27:06 docis dockerd[913]: time="2026-03-19T14:27:06.297675675Z" l>
Mar 19 14:34:39 docis dockerd[913]: time="2026-03-19T14:34:39.073735153Z" l>
Mar 19 15:03:05 docis dockerd[913]: time="2026-03-19T15:03:05.364245452Z" l>
Mar 19 15:03:05 docis dockerd[913]: time="2026-03-19T15:03:05.433860800Z" l>
Mar 19 15:04:55 docis dockerd[913]: time="2026-03-19T15:04:55.006819563Z" l>
Mar 19 15:05:48 docis dockerd[913]: time="2026-03-19T15:05:48.219576548Z" l>
Mar 20 07:28:15 docis dockerd[913]: time="2026-03-20T07:28:15.600871148Z" l>
Mar 20 07:31:56 docis dockerd[913]: time="2026-03-20T07:31:56.611308318Z" l>
Mar 20 07:33:01 docis dockerd[913]: time="2026-03-20T07:33:01.141242530Z" l>
lines 1-22/22 (END)
```

```bash
azureuser@docis:~$ groups azureuser
azureuser : azureuser docker
```

## 3. Lancement de conteneurs

**🌞 Utiliser la commande docker run**

- lancer un conteneur nginx
  - conf par défaut étou étou, simple pour le moment
  - par défaut il écoute sur le port 80 et propose une page d'accueil

- le conteneur doit être lancé avec un partage de port
  - le port 9999 de la machine hôte doit rediriger vers le port 80 du conteneur

```bash
azureuser@docis:~/work$ sudo docker run -d --name web -v "/home/azureuser/work/sites:/usr/share/nginx/html" -p 9999:80 nginx
8db30c7a1c72f61372547d9911f7beb01fbf99c56cf171eb74a75390e190b83b
```

**🌞 Rendre le service dispo sur internet**

- il faut peut-être ouvrir un port firewall dans votre VM (suivant votre OS, ptet y'en a un, ptet pas)
- il faut ouvrir un port dans l'interface web de Azure (appelez moi si vous trouvez pas)
- vous devez pouvoir le visiter avec votre navigateur (un curl m'ira bien pour le compte-rendu)

```bash
PS C:\Users\jerem> curl http://20.216.163.11:9999/

Avertissement de sécurité : risque d’exécution de script
Invoke-WebRequest analyse le contenu de la page web. Il se peut que le code
 de script de la page web s’exécute lors de l’analyse de la page.
      ACTION RECOMMANDÉE :
      Utilisez le commutateur -UseBasicParsing pour éviter l’exécution du
code de script.

      Voulez-vous continuer ?

[O] Oui  [T] Oui pour tout  [N] Non  [U] Non pour tout  [S] Suspendre
[?] Aide(la valeur par défaut est « N ») : o


StatusCode        : 200
StatusDescription : OK
Content           : <!DOCTYPE html>
                    <html lang="fr">
                    <head>
                      <meta charset="UTF-8">
                      <title>TP Parc Infos</title>
                    </head>
                    <body>
                      <h1>Bonjour</h1>
                      <p>Voici le TP Parc Infos</p>
                    </body>
                    </html>

RawContent        : HTTP/1.1 200 OK
                    Connection: keep-alive
                    Accept-Ranges: bytes
                    Content-Length: 178
                    Content-Type: text/html
                    Date: Fri, 20 Mar 2026 09:35:26 GMT
                    ETag: "69bd0e0d-b2"
                    Last-Modified: Fri, 20 Mar 2026 0...
Forms             : {}
Headers           : {[Connection, keep-alive], [Accept-Ranges, bytes],
                    [Content-Length, 178], [Content-Type, text/html]...}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 178
```

**🌞 Custom un peu le lancement du conteneur**

- l'app NGINX doit avoir un fichier de conf personnalisé pour écouter sur le port 7777 (pas le port 80 par défaut)
- l'app NGINX doit servir un fichier index.html personnalisé (pas le site par défaut)
- l'application doit être joignable grâce à un partage de ports (vers le port 7777)
- vous limiterez l'utilisation de la RAM du conteneur à 512M
- le conteneur devra avoir un nom : meow

> Tout se fait avec des options de la commande docker run.

Petit rappel de fonctionnement sur l'application NGINX :

- le fichier de conf par défaut se trouve dans /etc/nginx/nginx.conf
- si vous ouvrez ce fichier, vous constaterez qu'il inclut tout ce qu'il y a dans /etc/nginx/conf.d
  - pour que les fichiers de ce dossier soient inclus, ils doivent porter l'extension .conf

- il "suffit" donc
  - de créer un fichier de conf NGINX sur l'hôte
    - il porte l'extension .conf

    - il comporte une conf minimale pour écouter sur un port et servir un site dans un dossier précis

  - grâce à une option -v ... sur le docker run
    - de poser votre fichier de conf dans /etc/nginx/conf.d/

- un fichier de conf NGINX minimal pour faire ça est aussi simple que :

```bash
azureuser@docis:~/work$ cat toto.conf
server {
  # on définit le port où NGINX écoute dans le conteneur
  listen 7777;

  # on définit le chemin vers la racine web
  # dans ce dossier doit se trouver un fichier index.html
  root /var/www/tp_docker;
}
```

```bash
azureuser@docis:~$ sudo docker run -v /etc/nginx/nginx.conf:/etc/nginx/nginx.conf nginx
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2026/03/20 10:41:43 [emerg] 1#1: "listen" directive is not allowed here in /etc/nginx/nginx.conf:1
nginx: [emerg] "listen" directive is not allowed here in /etc/nginx/nginx.conf:1
```

```bash
azureuser@docis:~$ sudo docker run --name meow -d -v ~/work/sites/:/var/www/tp_docker -v ~/work/toto.conf:/etc/nginx/conf.d/toto.conf -p 9
999:7777 nginx
27eb37ee0b4c6f457821c8139e02ea7f2cdcecf989171e3740cb74708fbcb30d
azureuser@docis:~$ sudo docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                                 NAMES
32c76273a1cb   nginx     "/docker-entrypoint.…"   12 seconds ago   Up 11 seconds   80/tcp, 0.0.0.0:9999->7777/tcp, [::]:9999->7777/tcp   meow
```

```bash
azureuser@docis:~$ sudo docker exec -it meow bash
root@27eb37ee0b4c:/# cat /etc/nginx/conf.d/toto.conf
server {
  # on définit le port où NGINX écoute dans le conteneur
  listen 7777;

  # on définit le chemin vers la racine web
  # dans ce dossier doit se trouver un fichier index.html
  root /var/www/tp_docker;
}

root@27eb37ee0b4c:/# cat /var/www/tp_docker/index.html
<!DOCTYPE html>
<html>
<body>

<h1>VALIDE</h1>
<p> Voici le test avec le port 7777 edit.</p>

</body>
</html>
root@27eb37ee0b4c:/#
```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```
