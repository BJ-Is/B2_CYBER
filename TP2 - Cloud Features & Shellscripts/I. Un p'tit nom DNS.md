# I. Un p'tit nom DNS

Mini-partie pour définir un nom DNS à votre machine.

➔ **Définissez un nom de domaine pour joindre notre** azure1.tp2

- WebUI ou CLI donc
- le nom de domaine est associé à l'IP publique portée par l'interface de azure1.tp2 (genre il est pas associé à la VM directement)
- le nom que vous choisissez doit contenir `meow`

  **Prouvez que c'est effectif**

- une ou plusieurs commande(s) az qui retourne(nt) :

  - la VM (genre au moins son nom)
  - l'IP publique
  - le nom DNS associé

```bash
PS C:\Users\jerem> az network public-ip show -g azure-tp1 --name azure1.tp1PublicIP --query "{IP_Publique:ipAddress, Nom_DNS:dnsSettings.fqdn, VM_Associee:ipConfiguration.id}" -o table
IP_Publique     Nom_DNS                                           VM_Associee
--------------  ------------------------------------------------  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
52.143.163.228  meow-israel-tp2.francecentral.cloudapp.azure.com  /subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/azure-tp1/providers/Microsoft.Network/networkInterfaces/azure1.tp1VMNic/ipConfigurations/ipconfigazure1.tp1
```

- un `curl` fonctionnel vers le nom de domaine
  - comme d'hab, juste quelques lignes de la sortie, mettez pas tout :d

```bash
PS C:\Users\jerem> curl http://meow-israel-tp2.francecentral.cloudapp.azure.com:8000


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
                    Date: Sat, 01 Nov 2025 19:08:19 GMT
                    Server: Werkzeug/3.1.3 Python/3.10.12

                    <!DOCTYPE html>
                    <html l...
Forms             : {messageForm}
Headers           : {[Connection, close], [Content-Length, 12566], [Content-Type, text/html; charset=utf-8], [Date, Sat, 01 Nov 2025
                    19:08:19 GMT]...}
Images            : {}
InputFields       : {@{innerHTML=; innerText=; outerHTML=<INPUT id=username class=form-input maxLength=50 required placeholder="Your
                    name...">; outerText=; tagName=INPUT; id=username; class=form-input; maxLength=50; required=; placeholder=Your
                    name...}}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 12566
```
