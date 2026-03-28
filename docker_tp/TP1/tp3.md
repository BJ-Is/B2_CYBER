**🌞 Installez un WikiJS en utilisant Docker**

- WikiJS a besoin d'une base de données pour fonctionner
- il faudra donc deux conteneurs : un pour WikiJS et un pour la base de données
- référez-vous à la doc officielle de WikiJS, c'est tout guidé

```bash
azureuser@docis:~/wiki$ cat docker-compose.yaml
version: "3"
services:

  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: wiki
      POSTGRES_PASSWORD: wikijsrocks
      POSTGRES_USER: wikijs
    logging:
      driver: "none"
    restart: unless-stopped
    volumes:
      - db-data:/var/lib/postgresql/data

  wiki:
    image: ghcr.io/requarks/wiki:2
    depends_on:
      - db
    environment:
      DB_TYPE: postgres
      DB_HOST: db
      DB_PORT: 5432
      DB_USER: wikijs
      DB_PASS: wikijsrocks
      DB_NAME: wiki
    restart: unless-stopped
    ports:
      - "80:3000"

volumes:
  db-data:
```

```bash
azureuser@docis:~/wiki$ docker ps
CONTAINER ID   IMAGE                     COMMAND                  CREATED          STATUS          PORTS                                               NAMES
ea1d4b9eb6a5   ghcr.io/requarks/wiki:2   "docker-entrypoint.s…"   26 minutes ago   Up 26 minutes   3443/tcp, 0.0.0.0:80->3000/tcp, [::]:80->3000/tcp   wiki-wiki-1
2ae904236d3b   postgres:17-alpine        "docker-entrypoint.s…"   26 minutes ago   Up 26 minutes   5432/tcp                                            wiki-db-1
cd63f35ea976   img_test                  "apache2 -D FOREGROU…"   3 hours ago      Up 3 hours      0.0.0.0:8888->80/tcp, [::]:8888->80/tcp             practical_zhukovsky
```

```bash
PS C:\Users\jerem> curl http://20.216.163.11:80

Avertissement de sécurité : risque d’exécution de script
Invoke-WebRequest analyse le contenu de la page web. Il se peut que le code de script de la page web s’exécute lors de l’analyse de la page.
      ACTION RECOMMANDÉE :
      Utilisez le commutateur -UseBasicParsing pour éviter l’exécution du code de script.

      Voulez-vous continuer ?

[O] Oui  [T] Oui pour tout  [N] Non  [U] Non pour tout  [S] Suspendre  [?] Aide (la valeur par défaut est « N ») : o


StatusCode        : 200
StatusDescription : OK
Content           : <!DOCTYPE html><html><head><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta charset="UTF-8"><meta name="viewport"
                    content="user-scalable=yes, width=device-width, initial-scale=1, maximum-sca...
RawContent        : HTTP/1.1 200 OK
                    Vary: Accept-Encoding
                    Connection: keep-alive
                    Keep-Alive: timeout=5
                    Content-Length: 1315
                    Content-Type: text/html; charset=utf-8
                    Date: Mon, 23 Mar 2026 11:16:40 GMT
                    ETag: W/"523-1...
Forms             : {}
Headers           : {[Vary, Accept-Encoding], [Connection, keep-alive], [Keep-Alive, timeout=5], [Content-Length, 1315]...}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 1315
```

**🌞 Vous devez :**

- construire une image qui
  - contient python3

  - contient l'application et ses dépendances
  - lance l'application au démarrage du conteneur

```bash
azureuser@docis:~/wiki$ cat apps/Dockerfile
FROM python

COPY ./apps /apps

WORKDIR /apps

RUN pip install -r requirements.txt

CMD ["python","app.py"]
```

- écrire un docker-compose.yml qui définit le lancement de deux conteneurs :
  - l'app python
  - le Redis dont il a besoin

```bash
azureuser@docis:~/wiki$ cat docker-compose.yaml
services:
  app:
    image: app_py
    restart: always
    ports:
      - "8888:80"

  db:
    image: redis
    restart: always
    ports:
      - "6379:6379"
```

```bash
azureuser@docis:~/wiki$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
azureuser@docis:~/wiki$ docker compose up
Attaching to app-1, db-1
db-1  | Starting Redis Server
db-1  | 1:C 24 Mar 2026 08:37:15.555 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
db-1  | 1:C 24 Mar 2026 08:37:15.555 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
db-1  | 1:C 24 Mar 2026 08:37:15.556 * Redis version=8.6.1, bits=64, commit=00000000, modified=1, pid=1, just started
db-1  | 1:C 24 Mar 2026 08:37:15.557 * Configuration loaded
db-1  | 1:M 24 Mar 2026 08:37:15.558 * Increased maximum number of open files to 10032 (it was originally set to 1024).
db-1  | 1:M 24 Mar 2026 08:37:15.558 * monotonic clock: POSIX clock_gettime
db-1  | 1:M 24 Mar 2026 08:37:15.562 * Running mode=standalone, port=6379.
db-1  | 1:M 24 Mar 2026 08:37:15.568 * <bf> RedisBloom version 8.6.0 (Git=unknown)
db-1  | 1:M 24 Mar 2026 08:37:15.569 * <bf> Registering configuration options: [
db-1  | 1:M 24 Mar 2026 08:37:15.569 * <bf>     { bf-error-rate       :      0.01 }
db-1  | 1:M 24 Mar 2026 08:37:15.569 * <bf>     { bf-initial-size     :       100 }
db-1  | 1:M 24 Mar 2026 08:37:15.569 * <bf>     { bf-expansion-factor :         2 }
db-1  | 1:M 24 Mar 2026 08:37:15.570 * <bf>     { cf-bucket-size      :         2 }
db-1  | 1:M 24 Mar 2026 08:37:15.570 * <bf>     { cf-initial-size     :      1024 }
db-1  | 1:M 24 Mar 2026 08:37:15.570 * <bf>     { cf-max-iterations   :        20 }
db-1  | 1:M 24 Mar 2026 08:37:15.570 * <bf>     { cf-expansion-factor :         1 }
db-1  | 1:M 24 Mar 2026 08:37:15.570 * <bf>     { cf-max-expansions   :        32 }
db-1  | 1:M 24 Mar 2026 08:37:15.570 * <bf> ]
db-1  | 1:M 24 Mar 2026 08:37:15.570 * Module 'bf' loaded from /usr/local/lib/redis/modules//redisbloom.so
db-1  | 1:M 24 Mar 2026 08:37:15.854 * <search> Redis version found by RedisSearch : 8.6.1 - oss
db-1  | 1:M 24 Mar 2026 08:37:15.855 * <search> RediSearch version 8.6.0 (Git=7782b97)
db-1  | 1:M 24 Mar 2026 08:37:15.856 * <search> Low level api version 1 initialized successfully
db-1  | 1:M 24 Mar 2026 08:37:15.858 * <search> gc: ON, prefix min length: 2, min word length to stem: 4, prefix max expansions: 200, query timeout (ms): 500, timeout policy: return, oom policy: return, cursor read size: 1000, cursor max idle (ms): 300000, max doctable size: 1000000, max number of search results:  1000000, default scorer: BM25STD,
db-1  | 1:M 24 Mar 2026 08:37:15.859 * <search> Initialized thread pools!
db-1  | 1:M 24 Mar 2026 08:37:15.859 * <search> Disabled workers threadpool of size 0
db-1  | 1:M 24 Mar 2026 08:37:15.860 * <search> Subscribe to config changes
db-1  | 1:M 24 Mar 2026 08:37:15.860 * <search> Subscribe to cluster slot migration events
db-1  | 1:M 24 Mar 2026 08:37:15.860 * <search> Enabled role change notification
db-1  | 1:M 24 Mar 2026 08:37:15.860 * <search> Cluster configuration: AUTO partitions, type: 0, coordinator timeout: 0ms
db-1  | 1:M 24 Mar 2026 08:37:15.860 * Module 'search' loaded from /usr/local/lib/redis/modules//redisearch.so
db-1  | 1:M 24 Mar 2026 08:37:15.898 * <timeseries> RedisTimeSeries version 80600, git_sha=05fd355db748676861dc4c17d19c8c1ca74c0154
db-1  | 1:M 24 Mar 2026 08:37:15.899 * <timeseries> Redis version found by RedisTimeSeries : 8.6.1 - oss
db-1  | 1:M 24 Mar 2026 08:37:15.899 * <timeseries> Registering configuration options: [
db-1  | 1:M 24 Mar 2026 08:37:15.900 * <timeseries>     { ts-compaction-policy   :              }
db-1  | 1:M 24 Mar 2026 08:37:15.900 * <timeseries>     { ts-num-threads         :            3 }
db-1  | 1:M 24 Mar 2026 08:37:15.900 * <timeseries>     { ts-retention-policy    :            0 }
db-1  | 1:M 24 Mar 2026 08:37:15.900 * <timeseries>     { ts-duplicate-policy    :        block }
db-1  | 1:M 24 Mar 2026 08:37:15.901 * <timeseries>     { ts-chunk-size-bytes    :         4096 }
db-1  | 1:M 24 Mar 2026 08:37:15.901 * <timeseries>     { ts-encoding            :   compressed }
db-1  | 1:M 24 Mar 2026 08:37:15.901 * <timeseries>     { ts-ignore-max-time-diff:            0 }
db-1  | 1:M 24 Mar 2026 08:37:15.901 * <timeseries>     { ts-ignore-max-val-diff :     0.000000 }
db-1  | 1:M 24 Mar 2026 08:37:15.902 * <timeseries> ]
db-1  | 1:M 24 Mar 2026 08:37:15.902 * <timeseries> Detected redis oss
db-1  | 1:M 24 Mar 2026 08:37:15.903 * <timeseries> Subscribe to ASM events
db-1  | 1:M 24 Mar 2026 08:37:15.903 * <timeseries> Enabled diskless replication
db-1  | 1:M 24 Mar 2026 08:37:15.904 * Module 'timeseries' loaded from /usr/local/lib/redis/modules//redistimeseries.so
db-1  | 1:M 24 Mar 2026 08:37:16.102 * <ReJSON> Created new data type 'ReJSON-RL'
db-1  | 1:M 24 Mar 2026 08:37:16.103 * <ReJSON> version: 80600 git sha: unknown branch: unknown
db-1  | 1:M 24 Mar 2026 08:37:16.103 * <ReJSON> Exported RedisJSON_V1 API
db-1  | 1:M 24 Mar 2026 08:37:16.103 * <ReJSON> Exported RedisJSON_V2 API
db-1  | 1:M 24 Mar 2026 08:37:16.103 * <ReJSON> Exported RedisJSON_V3 API
db-1  | 1:M 24 Mar 2026 08:37:16.103 * <ReJSON> Exported RedisJSON_V4 API
db-1  | 1:M 24 Mar 2026 08:37:16.103 * <ReJSON> Exported RedisJSON_V5 API
db-1  | 1:M 24 Mar 2026 08:37:16.103 * <ReJSON> Exported RedisJSON_V6 API
db-1  | 1:M 24 Mar 2026 08:37:16.103 * <ReJSON> Enabled diskless replication
db-1  | 1:M 24 Mar 2026 08:37:16.103 * <ReJSON> Initialized shared string cache, thread safe: true.
db-1  | 1:M 24 Mar 2026 08:37:16.103 * Module 'ReJSON' loaded from /usr/local/lib/redis/modules//rejson.so
db-1  | 1:M 24 Mar 2026 08:37:16.103 * <search> Acquired RedisJSON_V6 API
db-1  | 1:M 24 Mar 2026 08:37:16.104 * Server initialized
db-1  | 1:M 24 Mar 2026 08:37:16.105 * <search> Changing workers threadpool size from 0 to 4
db-1  | 1:M 24 Mar 2026 08:37:16.107 * <search> Enabled workers threadpool of size 4
db-1  | 1:M 24 Mar 2026 08:37:16.107 * <search> Loading event started
db-1  | 1:M 24 Mar 2026 08:37:16.199 * Loading RDB produced by version 8.6.1
db-1  | 1:M 24 Mar 2026 08:37:16.199 * RDB age 343 seconds
db-1  | 1:M 24 Mar 2026 08:37:16.199 * RDB memory usage when created 1.26 Mb
db-1  | 1:M 24 Mar 2026 08:37:16.199 * Done loading RDB, keys loaded: 0, keys expired: 0.
db-1  | 1:M 24 Mar 2026 08:37:16.199 * <search> Changing workers threadpool size from 4 to 0
db-1  | 1:M 24 Mar 2026 08:37:16.199 * <search> Scheduling config_reduce_threads_job to remove all 4 threads when empty
db-1  | 1:M 24 Mar 2026 08:37:16.199 * <search> Disabled workers threadpool of size 4
db-1  | 1:M 24 Mar 2026 08:37:16.199 * <search> Loading event ended successfully
db-1  | 1:M 24 Mar 2026 08:37:16.199 * DB loaded from disk: 0.094 seconds
db-1  | 1:M 24 Mar 2026 08:37:16.199 * Ready to accept connections tcp
db-1  | 1:M 24 Mar 2026 08:37:16.199 # WARNING: Redis does not require authentication and is not protected by network restrictions. Redis will accept connections from any IP address on any network interface.
azureuser@docis:~/wiki$
```

```bash
azureuser@docis:~$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED      STATUS          PORTS                                         NAMES
dea681b3251b   redis     "docker-entrypoint.s…"   4 days ago   Up 10 seconds   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp   wiki-db-1
ad5882d169fd   app_py    "python app.py"          4 days ago   Up 10 seconds   0.0.0.0:8888->80/tcp, [::]:8888->80/tcp       wiki-app-1
```
