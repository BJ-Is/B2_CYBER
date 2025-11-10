# III. Gestion de secrets

## Créer un Key Vault

```bash
israel@hpvictusBJI:~$ az keyvault create -g azure-tp1 -n kv-is-tp2 --locatio
n francecentral --enable-rbac-authorization false
{
  "id": "/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/azure-tp1/providers/Microsoft.KeyVault/vaults/kv-is-tp2",
  "location": "francecentral",
  "name": "kv-is-tp2",
  "properties": {
    "accessPolicies": [
      {
        "applicationId": null,
        "objectId": "79472219-4fff-4bcc-9490-1a5e8951248a",
        "permissions": {
          "certificates": [
            "all"
          ],
          "keys": [
            "all"
          ],
          "secrets": [
            "all"
          ],
          "storage": [
            "all"
          ]
        },
        "tenantId": "413600cf-bd4e-4c7c-8a61-69e73cddf731"
      }
    ],
    "createMode": null,
    "enablePurgeProtection": null,
    "enableRbacAuthorization": false,
    "enableSoftDelete": true,
    "enabledForDeployment": false,
    "enabledForDiskEncryption": false,
    "enabledForTemplateDeployment": false,
    "hsmPoolResourceId": null,
    "networkAcls": null,
    "privateEndpointConnections": null,
    "provisioningState": "Succeeded",
    "publicNetworkAccess": "Enabled",
    "sku": {
      "family": "A",
      "name": "standard"
    },
    "softDeleteRetentionInDays": 90,
    "tenantId": "413600cf-bd4e-4c7c-8a61-69e73cddf731",
    "vaultUri": "https://kv-is-tp2.vault.azure.net/"
  },
  "resourceGroup": "azure-tp1",
  "systemData": {
    "createdAt": "2025-11-10T11:39:24.307000+00:00",
    "createdBy": "jeremie.beugre@efrei.net",
    "createdByType": "User",
    "lastModifiedAt": "2025-11-10T11:39:24.307000+00:00",
    "lastModifiedBy": "jeremie.beugre@efrei.net",
    "lastModifiedByType": "User"
  },
  "tags": {},
  "type": "Microsoft.KeyVault/vaults"
}
```

## ➜ Créer un secret

```bash
israel@hpvictusBJI:~$ az keyvault secret set --vault-name kv-is-tp2 --name T
estSecret --value "on va tester voir, si cela fonctionne ou pas"
{
  "attributes": {
    "created": "2025-11-10T11:46:41+00:00",
    "enabled": true,
    "expires": null,
    "notBefore": null,
    "recoverableDays": 90,
    "recoveryLevel": "Recoverable+Purgeable",
    "updated": "2025-11-10T11:46:41+00:00"
  },
  "contentType": null,
  "id": "https://kv-is-tp2.vault.azure.net/secrets/TestSecret/c01aedcd6011427d93f3330ddb9fd52c",
  "kid": null,
  "managed": null,
  "name": "TestSecret",
  "tags": {
    "file-encoding": "utf-8"
  },
  "value": "on va tester voir, si cela fonctionne ou pas"
}
```

```bash
israel@hpvictusBJI:~$ az vm identity assign -g azure-tp1 -n azure1.tp1
{
  "systemAssignedIdentity": "950d1126-cab8-4b0c-9ec0-992e97e77a47",
  "userAssignedIdentities": {}
}
```

## Configurer une Access policy

```bash
israel@hpvictusBJI:~$ az keyvault set-policy --name kv-is-tp2 --object-id 950d1126-cab8-4b0c-9ec0-992e97e77a47 --secret-permissions get
{
  "id": "/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/azure-tp1/providers/Microsoft.KeyVault/vaults/kv-is-tp2",
  "location": "francecentral",
  "name": "kv-is-tp2",
  "properties": {
    "accessPolicies": [
      {
        "applicationId": null,
        "objectId": "79472219-4fff-4bcc-9490-1a5e8951248a",
        "permissions": {
          "certificates": [
            "all"
          ],
          "keys": [
            "all"
          ],
          "secrets": [
            "all"
          ],
          "storage": [
            "all"
          ]
        },
        "tenantId": "413600cf-bd4e-4c7c-8a61-69e73cddf731"
      },
      {
        "applicationId": null,
        "objectId": "950d1126-cab8-4b0c-9ec0-992e97e77a47",
        "permissions": {
          "certificates": null,
          "keys": null,
          "secrets": [
            "get"
          ],
          "storage": null
        },
        "tenantId": "413600cf-bd4e-4c7c-8a61-69e73cddf731"
      }
    ],
    "createMode": null,
    "enablePurgeProtection": null,
    "enableRbacAuthorization": false,
    "enableSoftDelete": true,
    "enabledForDeployment": false,
    "enabledForDiskEncryption": false,
    "enabledForTemplateDeployment": false,
    "hsmPoolResourceId": null,
    "networkAcls": null,
    "privateEndpointConnections": null,
    "provisioningState": "Succeeded",
    "publicNetworkAccess": "Enabled",
    "sku": {
      "family": "A",
      "name": "standard"
    },
    "softDeleteRetentionInDays": 90,
    "tenantId": "413600cf-bd4e-4c7c-8a61-69e73cddf731",
    "vaultUri": "https://kv-is-tp2.vault.azure.net/"
  },
  "resourceGroup": "azure-tp1",
  "systemData": {
    "createdAt": "2025-11-10T11:39:24.307000+00:00",
    "createdBy": "jeremie.beugre@efrei.net",
    "createdByType": "User",
    "lastModifiedAt": "2025-11-10T11:52:38.270000+00:00",
    "lastModifiedBy": "jeremie.beugre@efrei.net",
    "lastModifiedByType": "User"
  },
  "tags": {},
  "type": "Microsoft.KeyVault/vaults"
}
```

## 1. Un premier secret

- **🌞 Récupérer votre secret depuis la VM**

  - vous vous connectez en SSH à azure1.tp2

- téléchargez le CLI az (suivez la doc officielle, y'a un paquet normalement)
- puis :

```bash
israel@azure1:~$ az login --identity --allow-no-subscriptions
[
  {
    "environmentName": "AzureCloud",
    "id": "413600cf-bd4e-4c7c-8a61-69e73cddf731",
    "isDefault": true,
    "name": "N/A(tenant level account)",
    "state": "Enabled",
    "tenantId": "413600cf-bd4e-4c7c-8a61-69e73cddf731",
    "user": {
      "assignedIdentityInfo": "MSI",
      "name": "systemAssignedIdentity",
      "type": "servicePrincipal"
    }
  }
]
israel@azure1:~$ az keyvault secret show --vault-name kv-is-tp2 --name TestSecret
{
  "attributes": {
    "created": "2025-11-10T11:46:41+00:00",
    "enabled": true,
    "expires": null,
    "notBefore": null,
    "recoverableDays": 90,
    "recoveryLevel": "Recoverable+Purgeable",
    "updated": "2025-11-10T11:46:41+00:00"
  },
  "contentType": null,
  "id": "https://kv-is-tp2.vault.azure.net/secrets/TestSecret/c01aedcd6011427d93f3330ddb9fd52c",
  "kid": null,
  "managed": null,
  "name": "TestSecret",
  "tags": {
    "file-encoding": "utf-8"
  },
  "value": "on va tester voir, si cela fonctionne ou pas"
}
```

## 2. Gérer les secrets de l'application

- Créer un nouveau secret dans votre Key Vault

- appelez-le DBPASSWORD (on a pas le doirt à \_ dans les noms)
- le secret c'est donc "meow" (super secret :d)

```bash

```

### A. Script pour récupérer les secrets

- **Coder un piti script** bash : get_secrets.sh

- il commence probablement par un `az login --identity`
- il récupère le secret DBPASSWORD (commande az, stocke dans une variable)
- il l'injecte dans le fichier .env

  - commande sed ou autres
  - il remplace la valeur de `DB_PASSWORD=` par le secret récupéré avec la commande az

```bash
israel@azure1:~$ cat  /usr/local/bin/get_secrets.sh
#!/bin/bash
set -e
VAULT_NAME="kv-is-tp2"
ENV_FILE="/opt/meow/.env"
az login --identity --allow-no-subscriptions > /dev/null 2>&1
DB_PASS=$(az keyvault secret show --vault-name $VAULT_NAME --name DBPASSWORD --query "value" -o tsv)
sed -i "s|^DB_PASSWORD=.*|DB_PASSWORD=${DB_PASS}|" $ENV_FILE
```

- **Environnement du script** get_secrets.sh, il doit :

  - être stocké dans /usr/local/bin sur azure1.tp2 (commande `mv`)
  - appartenir à l'utilisateur webapp (commande `chown`)
  - être exécutable (commande `chmod`)
  - être inutilisable par les "autres" (ni r, ni w, ni x)

➔ Au cas où j'ai besoin de préciser... TU TESTES TON SCRIPT

- tu changes à la main la ligne DB_PASSWORD dans le .env
- tu relances ton script
- tu vérifies que le .env est bien mis à jour

```bash
israel@azure1:~$ sudo sed -i "s|^DB_PASSWORD=.*|DB_PASSWORD=nimportequoi|" /opt/meow/.env
israel@azure1:~$ sudo cat /opt/meow/.env
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
DB_PASSWORD=nimportequoi
israel@azure1:~$ sudo -u webapp HOME=/opt/meow /usr/local/bin/get_secrets.sh
[
  {
    "environmentName": "AzureCloud",
    "id": "413600cf-bd4e-4c7c-8a61-69e73cddf731",
    "isDefault": true,
    "name": "N/A(tenant level account)",
    "state": "Enabled",
    "tenantId": "413600cf-bd4e-4c7c-8a61-69e73cddf731",
    "user": {
      "assignedIdentityInfo": "MSI",
      "name": "systemAssignedIdentity",
      "type": "servicePrincipal"
    }
  }
]
israel@azure1:~$ sudo cat /opt/meow/.env
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

### B. Exécution automatique

**🌞 Ajouter le script en `ExecStartPre=` dans webapp.service**

- éditer le fichier webapp.service
- ajouter une ligne `ExecStartPre=/usr/local/bin/get_secrets.sh` dans la section [Service]
- exécuter une commande `sudo systemctl daemon-reload` pour indiquer au système qu'on a modifié un service
- relancer le service webapp

### Note

Ce qu'on indique en `ExecStartPre=` sera exécuté systématiquement avant `ExecStart=`.  
Euh et au cas où `ExecStart=` indique la commande à lancer quand tu tapes `systemctl start <ton_service>`.

```bash
israel@azure1:~$ sudo nano /etc/systemd/system/webapp.service
israel@azure1:~$ sudo systemctl daemon-reload
israel@azure1:~$ sudo cat nano /etc/systemd/system/webapp.service
cat: nano: No such file or directory
[Unit]
Description=Super Webapp MEOW

[Service]
User=webapp
Group=webapp
WorkingDirectory=/opt/meow
ExecStart=/opt/meow/bin/python app.py
Environment="HOME=/opt/meow"
ExecStartPre=/usr/local/bin/get_secrets.sh

[Install]
WantedBy=multi-user.target
```

➔ **Prouvez que la ligne en ExecStartPre= a bien été exécutée**

- on le voit dans `systemctl status <ton_service>`
- tu peux voir le .env mis à jour aussi si tu fais une modif manuelle avant

```bash
israel@azure1:~$ sudo sed -i "s|^DB_PASSWORD=.*|DB_PASSWORD=casse_sys|" /opt
/meow/.env
israel@azure1:~$ sudo cat /opt/meow/.env
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
DB_PASSWORD=casse_sys

israel@azure1:~$ sudo systemctl restart webapp.service
israel@azure1:~$ sudo cat /opt/meow/.env
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
israel@azure1:~$ systemctl status webapp.service
● webapp.service - Super Webapp MEOW
     Loaded: loaded (/etc/systemd/system/webapp.service; enabled; vendor pr>
     Active: active (running) since Mon 2025-11-10 12:46:20 UTC; 1min 29s a>
    Process: 94641 ExecStartPre=/usr/local/bin/get_secrets.sh (code=exited,>
   Main PID: 94665 (python)
      Tasks: 1 (limit: 1009)
     Memory: 56.1M
        CPU: 2.676s
     CGroup: /system.slice/webapp.service
             └─94665 /opt/meow/bin/python app.py

Nov 10 12:46:20 azure1 systemd[1]: webapp.service: Found left-over process >
Nov 10 12:46:20 azure1 systemd[1]: This usually indicates unclean terminati>
Nov 10 12:46:20 azure1 systemd[1]: Started Super Webapp MEOW.
Nov 10 12:46:21 azure1 python[94665]:  * Serving Flask app 'app'
Nov 10 12:46:21 azure1 python[94665]:  * Debug mode: off
Nov 10 12:46:21 azure1 python[94665]: WARNING: This is a development server>
Nov 10 12:46:21 azure1 python[94665]:  * Running on all addresses (0.0.0.0)
Nov 10 12:46:21 azure1 python[94665]:  * Running on http://127.0.0.1:8000
Nov 10 12:46:21 azure1 python[94665]:  * Running on http://10.0.0.4:8000
Nov 10 12:46:21 azure1 python[94665]: Press CTRL+C to quit
```

## C. Secret Flask

- **Intéprez la gestion du secret Flask dans votre script** get_secrets.sh

- créez un nouveau secret dans le _Key Vault_ pour stocker ça

  - vous en profiterez pour générer un nouveau secret que celui que j'ai mis
  - comme ça il sera vraiment... secret dukoo .d
  - vous utiliserez une commande shell pour générer ce nouveau secret, je la veux dans le compte-rendu

- votre script doit récupérer ce secret aussi, et l'injecter aussi dans le .env

```bash
israel@hpvictusBJI:~$ openssl rand -hex 32
1e9f90ff5344bed55dfe5c1ff6626a01c7a4a7e12085e4d3fbb0847bb66f33e0
israel@hpvictusBJI:~$ az keyvault secret set --vault-name kv-is-tp2 --name FLASKSECRETKEY --value 1e9f90ff5344bed55dfe5c1ff6626a01c7a4a7e12085e4d3fbb084
7bb66f33e0
{
  "attributes": {
    "created": "2025-11-10T12:51:01+00:00",
    "enabled": true,
    "expires": null,
    "notBefore": null,
    "recoverableDays": 90,
    "recoveryLevel": "Recoverable+Purgeable",
    "updated": "2025-11-10T12:51:01+00:00"
  },
  "contentType": null,
  "id": "https://kv-is-tp2.vault.azure.net/secrets/FLASKSECRETKEY/e735a5d3ab0f42948b6921391740a769",
  "kid": null,
  "managed": null,
  "name": "FLASKSECRETKEY",
  "tags": {
    "file-encoding": "utf-8"
  },
  "value": "1e9f90ff5344bed55dfe5c1ff6626a01c7a4a7e12085e4d3fbb0847bb66f33e0"
}
```

```bash
israel@azure1:~$ sudo cat nano /usr/local/bin/get_secrets.sh
cat: nano: No such file or directory
#!/bin/bash
set -e
VAULT_NAME="kv-is-tp2"
ENV_FILE="/opt/meow/.env"
az login --identity --allow-no-subscriptions
DB_PASS=$(az keyvault secret show --vault-name $VAULT_NAME --name DBPASSWORD --query "value" -o tsv)
sed -i "s|^DB_PASSWORD=.*|DB_PASSWORD=${DB_PASS}|" $ENV_FILE
FLASK_KEY=$(az keyvault secret show --vault-name $VAULT_NAME --name FLASKSECRETKEY --query "value" -o tsv)
sed -i "s|^FLASK_SECRET_KEY=.*|FLASK_SECRET_KEY=${FLASK_KEY}|" $ENV_FILE
israel@azure1:~$ sudo systemctl restart webapp.service
israel@azure1:~$ sudo sed -i "s|^DB_PASSWORD=.*|DB_PASSWORD=casse|" /opt/meow/.env
israel@azure1:~$ sudo sed -i "s|^FLASK_SECRET_KEY=.*|FLASK_SECRET_KEY=casse_aussi|" /opt/meow/.env
israel@azure1:~$ sudo cat /opt/meow/.env
# Flask Configuration
FLASK_SECRET_KEY=casse_aussi
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=8000

# Database Configuration
DB_HOST=10.0.0.5
DB_PORT=3306
DB_NAME=meow_database
DB_USER=meow
DB_PASSWORD=casse
```

- **Redémarrer le service**

- prouver que le script a été run et que le changement de secret a fonctionné

Stylé non. Du coup si tu crées la même app à l'autre bout du monde, elle peut récupérer le même secret np, de façon sécurisée. Si tu refais ta machine, t'as pas besoin de conserver le secret j'sais pas où pour le remettre après. Si tu dév, tu stockes pas le secret dans ton dépôt git. Etc etc etc.

- **Dans le dépôt git : votre dernière version de** get_secrets.sh

```bash
israel@azure1:~$ sudo systemctl restart webapp.servic
israel@azure1:~$ sudo cat /opt/meow/.env
# Flask Configuration
FLASK_SECRET_KEY=1e9f90ff5344bed55dfe5c1ff6626a01c7a4a7e12085e4d3fbb0847bb66f33e0
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
