## Construisez votre propre Dockerfile

**🌞 Construire votre propre image**

- image de base (celle que vous voulez : debian, alpine, ubuntu, etc.)
  - une image du Docker Hub
  - qui ne porte aucune application par défaut

- vous ajouterez
  - mise à jour du système
  - installation de Apache (pour les systèmes debian, le serveur Web apache - - s'appelle apache2 et non pas httpd comme sur Rocky)
  - page d'accueil Apache HTML personnalisée

**➜** Pour vous aider, voilà un fichier de conf minimal pour Apache (à positionner dans /etc/apache2/apache2.conf) :

```bash
azureuser@docis:~/workfiles$ ls
apache2.conf  dockerfile  index.html
azureuser@docis:~/workfiles$ cat index.html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>TP Parc Infos</title>
</head>
<body>
  <h1>Bonjour</h1>
  <p>image build avec pour nom imgtest</p>
</body>
</html>
azureuser@docis:~/workfiles$ cat Dockerfile
FROM ubuntu
RUN apt update
RUN apt install -y apache2
RUN mkdir /etc/apache2/logs/
COPY index.html /var/www/html
COPY apache2.conf /etc/apache2/apache2.conf
CMD ["apache2", "-D", "FOREGROUND"]
azureuser@docis:~/workfiles$ cat apache2.conf
# on définit un port sur lequel écouter
Listen 80

# on charge certains modules Apache strictement nécessaires à son bon fonctionnement
LoadModule mpm_event_module "/usr/lib/apache2/modules/mod_mpm_event.so"
LoadModule dir_module "/usr/lib/apache2/modules/mod_dir.so"
LoadModule authz_core_module "/usr/lib/apache2/modules/mod_authz_core.so"

# on indique le nom du fichier HTML à charger par défaut
DirectoryIndex index.html
# on indique le chemin où se trouve notre site
DocumentRoot "/var/www/html/"

# quelques paramètres pour les logs
ErrorLog "logs/error.log"
LogLevel warn

azureuser@docis:~/workfiles$
```

```bash
azureuser@docis:~/workfiles$ docker build . -t img_test
[+] Building 45.9s (10/10) FINISHED                                                                                        docker:default
 => [internal] load build definition from dockerfile                                                                                 0.0s
 => => transferring dockerfile: 203B                                                                                                 0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                                                                     0.4s
 => [internal] load .dockerignore                                                                                                    0.0s
 => => transferring context: 2B                                                                                                      0.0s
 => CACHED [1/5] FROM docker.io/library/ubuntu:latest@sha256:186072bba1b2f436cbb91ef2567abca677337cfc786c86e107d25b7072feef0c        0.1s
 => => resolve docker.io/library/ubuntu:latest@sha256:186072bba1b2f436cbb91ef2567abca677337cfc786c86e107d25b7072feef0c               0.1s
 => [internal] load build context                                                                                                    0.0s
 => => transferring context: 64B                                                                                                     0.0s
 => [2/5] RUN apt update                                                                                                             6.4s
 => [3/5] RUN apt install -y apache2                                                                                                21.3s
 => [4/5] COPY index.html /var/www/html                                                                                              0.4s
 => [5/5] COPY apache2.conf /etc/apache2/apache2.conf                                                                                0.2s
 => exporting to image                                                                                                              16.4s
 => => exporting layers                                                                                                             12.3s
 => => exporting manifest sha256:60066a250ba7ca747a63cab5980e3a0b24f650d75c84096c4d2c3b5442020633                                    0.0s
 => => exporting config sha256:e7588bb30ee1b2e9a764f1b293af111826f323457aefe87170d533e92ae9f4cf                                      0.0s
 => => exporting attestation manifest sha256:933721045ea54ef0db4da48eee49836ebb47f8e5be35e6f7da72f778306320ec                        0.1s
 => => exporting manifest list sha256:4bc8f6762cd712fb24abc61499e434a520b32cad4e8083e38bfcd895a38f487a                               0.0s
 => => naming to docker.io/library/img_test:latest                                                                                   0.0s
 => => unpacking to docker.io/library/img_test:latest                                                                                3.8s
azureuser@docis:~/workfiles$
```

```bash
azureuser@docis:~/workfiles$ docker images
                                                                                                                      i Info →   U  In Use
IMAGE                ID             DISK USAGE   CONTENT SIZE   EXTRA
hello-world:latest   85404b3c5395       25.9kB         9.52kB
img_test:latest      4bc8f6762cd7        371MB          107MB
nginx:latest         dec7a90bd097        240MB         65.8MB    U
azureuser@docis:~/workfiles$
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
