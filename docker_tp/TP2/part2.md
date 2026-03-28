**🌞 Connectez-vous en SSH à la VM pour preuve**

- cette connexion ne doit demander aucun password : votre clé a été ajoutée à votre Agent SSH

```bash
israel@hpvictusBJI:~$ ssh -i ~/.ssh/cloud_tp1 israel@20.199.89.150
The authenticity of host '20.199.89.150 (20.199.89.150)' can't be established.
ED25519 key fingerprint is SHA256:TSZpFnb8JlHSYK8gnGJ+jGiHwnvbpbrmAoCfWFhYaxY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '20.199.89.150' (ED25519) to the list of known hosts.
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.17.0-1008-azure x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Thu Mar 12 04:26:30 UTC 2026

  System load:    0.87      Processes:             22
  Usage of /home: unknown   Users logged in:       0
  Memory usage:   5%        IPv4 address for eth0: 10.10.10.2
  Swap usage:     0%

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

israel@terraform:~$
```

## 2. az : a programmatic approach

**Créez une VM depuis le Azure CLI**

- en utilisant uniquement la commande **az**
- je vous laisse faire vos recherches pour créer une VM avec la commande **az**
- utilisez cette image **Alma 10**

**Vous devrez préciser :**

- quel utilisateur doit être créé à la création de la VM
- le fichier de clé utilisé pour se connecter à cet utilisateur
- comme ça, dès que la VM pop, on peut se co en SSH !

```bash
israel@hpvictusBJI:~$ az group create --location francecentral --name meo
{
  "id": "/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/meo",
  "location": "francecentral",
  "managedBy": null,
  "name": "meo",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": "Microsoft.Resources/resourceGroups"
}
```

```bash
israel@hpvictusBJI:~$ az vm create \
  -g meo \
  -n super_vm \
  --image almalinux:almalinux-x86_64:10-gen2:10.1.202512150 \
  --admin-username israel \
  --ssh-key-values /tmp/ssh/cloud_tp1.pub \
  --location francecentral \
  --size Standard_B1s
The default value of '--size' will be changed to 'Standard_D2s_v5' from 'Standard_DS1_v2' in a future release.
Selecting "northeurope" may reduce your costs. The region you've selected may cost more for the same services. You can disable this message in the future with the command "az config set core.display_region_identified=false". Learn more at https://go.microsoft.com/fwlink/?linkid=222571

Consider upgrading security for your workloads using Azure Trusted Launch VMs. To know more about Trusted Launch, please visit https://aka.ms/TrustedLaunch.
{
  "fqdns": "",
  "id": "/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/meo/providers/Microsoft.Compute/virtualMachines/super_vm",
  "location": "francecentral",
  "macAddress": "60-45-BD-6D-17-EF",
  "powerState": "VM running",
  "privateIpAddress": "10.0.0.4",
  "publicIpAddress": "20.111.50.8",
  "resourceGroup": "meo"
}
```

**🌞 Assurez-vous que vous pouvez vous connecter à la VM en SSH sur son IP publique**

```bash
israel@hpvictusBJI:~$ ssh -i ~/.ssh/cloud_tp1 israel@20.111.50.8
The authenticity of host '20.111.50.8 (20.111.50.8)' can't be established.
ED25519 key fingerprint is SHA256:dczKrjISy7Zrijys5baJx35TQNl2ycS3MtST1KTUWcI.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '20.111.50.8' (ED25519) to the list of known hosts.

1 device has a firmware upgrade available.
Run `fwupdmgr get-upgrades` for more information.

[israel@supervm ~]$
```

**🌞 Une fois connecté, prouvez la présence...**

- ...du service waagent.service

```bash
[israel@supervm ~]$ systemctl status waagent.service
● waagent.service - Azure Linux Agent
     Loaded: loaded (/usr/lib/systemd/system/waagent.service; enabled; preset: enabled)
     Active: active (running) since Sat 2026-03-28 14:46:18 UTC; 4h 8min ago
 Invocation: 9bd6dc4a8a4d45469bfc4e0fb13ac7b1
   Main PID: 1315 (python3)
      Tasks: 6 (limit: 5238)
     Memory: 48.5M (peak: 50.8M)
        CPU: 22.550s
     CGroup: /azure.slice/waagent.service
             ├─1315 /usr/bin/python3 -u /usr/sbin/waagent -daemon
             └─1447 /usr/bin/python3 -u bin/WALinuxAgent-2.15.1.3-py3.12.egg -run-exthandlers

Mar 28 15:46:26 supervm python3[1447]: 2026-03-28T15:46:26.572977Z INFO ExtHandler ExtHandler [HEARTBEAT] Agent WALinuxAgent-2.15>
Mar 28 16:16:27 supervm python3[1447]: 2026-03-28T16:16:27.887446Z INFO ExtHandler ExtHandler [HEARTBEAT] Agent WALinuxAgent-2.15>
Mar 28 16:46:28 supervm python3[1447]: 2026-03-28T16:46:28.591539Z INFO ExtHandler ExtHandler Downloading agent manifest
Mar 28 16:46:28 supervm python3[1447]: 2026-03-28T16:46:28.632817Z INFO ExtHandler ExtHandler [HEARTBEAT] Agent WALinuxAgent-2.15>
Mar 28 17:16:29 supervm python3[1447]: 2026-03-28T17:16:29.549923Z INFO ExtHandler ExtHandler [HEARTBEAT] Agent WALinuxAgent-2.15>
Mar 28 17:46:30 supervm python3[1447]: 2026-03-28T17:46:30.165559Z INFO ExtHandler ExtHandler Downloading agent manifest
Mar 28 17:46:30 supervm python3[1447]: 2026-03-28T17:46:30.200148Z INFO ExtHandler ExtHandler [HEARTBEAT] Agent WALinuxAgent-2.15>
Mar 28 18:16:30 supervm python3[1447]: 2026-03-28T18:16:30.662341Z INFO ExtHandler ExtHandler [HEARTBEAT] Agent WALinuxAgent-2.15>
Mar 28 18:46:31 supervm python3[1447]: 2026-03-28T18:46:31.273976Z INFO ExtHandler ExtHandler Downloading agent manifest
Mar 28 18:46:31 supervm python3[1447]: 2026-03-28T18:46:31.312944Z INFO ExtHandler ExtHandler [HEARTBEAT] Agent WALinuxAgent-2.15>
lines 1-22/22 (END)
```

- ...du service cloud-init.service

```bash
[israel@supervm ~]$ systemctl status cloud-init.service
● cloud-init.service - Cloud-init: Network Stage
     Loaded: loaded (/usr/lib/systemd/system/cloud-init.service; enabled; preset: enabled)
     Active: active (exited) since Sat 2026-03-28 14:46:18 UTC; 4h 9min ago
 Invocation: 2ac8bfab937f4a75add68744688aae6d
   Main PID: 937 (code=exited, status=0/SUCCESS)
   Mem peak: 49.5M
        CPU: 1.019s

Mar 28 14:46:18 supervm cloud-init[956]: |    o o *.=+E.   |
Mar 28 14:46:18 supervm cloud-init[956]: |   . . o .oo+    |
Mar 28 14:46:18 supervm cloud-init[956]: |    .   oo.o     |
Mar 28 14:46:18 supervm cloud-init[956]: |     .  Soo      |
Mar 28 14:46:18 supervm cloud-init[956]: |    . .  .       |
Mar 28 14:46:18 supervm cloud-init[956]: |.... +    .      |
Mar 28 14:46:18 supervm cloud-init[956]: |.B+.O o  .       |
Mar 28 14:46:18 supervm cloud-init[956]: |==B*o= o.        |
Mar 28 14:46:18 supervm cloud-init[956]: +----[SHA256]-----+
Mar 28 14:46:18 supervm systemd[1]: Finished cloud-init.service - Cloud-init: Network Stage.
```

```bash
[israel@supervm ~]$ cloud-init status
status: done
```

## 3. Terraforming planets infrastructures

Une dernière section pour jouer avec Terraform, on se contente là encore de simplement créer une VM Azure.
**Utilisez Terraform pour créer une VM dans Azure**

- J'veux la suite de commande `terraform` utilisée dans le compte-rendu

```bash
israel@hpvictusBJI:~/terraform$ terraform init
Initializing the backend...
Initializing provider plugins...
- Finding latest version of hashicorp/azurerm...
- Installing hashicorp/azurerm v4.66.0...
- Installed hashicorp/azurerm v4.66.0 (signed by HashiCorp)
Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

israel@hpvictusBJI:~/terraform$ terraform plan
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following
symbols:
  + create

Terraform will perform the following actions:

  # azurerm_linux_virtual_machine.main will be created
  + resource "azurerm_linux_virtual_machine" "main" {
      + admin_username                                         = "israel"
      + allow_extension_operations                             = (known after apply)
      + bypass_platform_safety_checks_on_user_schedule_enabled = false
      + computer_name                                          = (known after apply)
      + disable_password_authentication                        = (known after apply)
      + disk_controller_type                                   = (known after apply)
      + extensions_time_budget                                 = "PT1H30M"
      + id                                                     = (known after apply)
      + location                                               = "francecentral"
      + max_bid_price                                          = -1
      + name                                                   = "super-vm"
      + network_interface_ids                                  = (known after apply)
      + os_managed_disk_id                                     = (known after apply)
      + patch_assessment_mode                                  = (known after apply)
      + patch_mode                                             = (known after apply)
      + platform_fault_domain                                  = -1
      + priority                                               = "Regular"
      + private_ip_address                                     = (known after apply)
      + private_ip_addresses                                   = (known after apply)
      + provision_vm_agent                                     = (known after apply)
      + public_ip_address                                      = (known after apply)
      + public_ip_addresses                                    = (known after apply)
      + resource_group_name                                    = "tp1_terraform"
      + size                                                   = "Standard_B1s"
      + virtual_machine_id                                     = (known after apply)
      + vm_agent_platform_updates_enabled                      = (known after apply)

      + admin_ssh_key {
          + public_key = <<-EOT
                ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINwv4hLNfexz23UO/krC/xs3KI1Nho+0xVCUnmLmn5fW cloud_tp1
            EOT
          + username   = "israel"
        }

      + os_disk {
          + caching                   = "ReadWrite"
          + disk_size_gb              = (known after apply)
          + id                        = (known after apply)
          + name                      = "vm-os-disk"
          + storage_account_type      = "Standard_LRS"
          + write_accelerator_enabled = false
        }

      + source_image_reference {
          + offer     = "almalinux-x86_64"
          + publisher = "almalinux"
          + sku       = "10-gen2"
          + version   = "latest"
        }

      + termination_notification (known after apply)
    }

  # azurerm_network_interface.main will be created
  + resource "azurerm_network_interface" "main" {
      + accelerated_networking_enabled = false
      + applied_dns_servers            = (known after apply)
      + id                             = (known after apply)
      + internal_domain_name_suffix    = (known after apply)
      + ip_forwarding_enabled          = false
      + location                       = "francecentral"
      + mac_address                    = (known after apply)
      + name                           = "vm-nic"
      + private_ip_address             = (known after apply)
      + private_ip_addresses           = (known after apply)
      + resource_group_name            = "tp1_terraform"
      + virtual_machine_id             = (known after apply)

      + ip_configuration {
          + gateway_load_balancer_frontend_ip_configuration_id = (known after apply)
          + name                                               = "internal"
          + primary                                            = (known after apply)
          + private_ip_address                                 = (known after apply)
          + private_ip_address_allocation                      = "Dynamic"
          + private_ip_address_version                         = "IPv4"
          + public_ip_address_id                               = (known after apply)
          + subnet_id                                          = (known after apply)
        }
    }

  # azurerm_public_ip.main will be created
  + resource "azurerm_public_ip" "main" {
      + allocation_method       = "Static"
      + ddos_protection_mode    = "VirtualNetworkInherited"
      + fqdn                    = (known after apply)
      + id                      = (known after apply)
      + idle_timeout_in_minutes = 4
      + ip_address              = (known after apply)
      + ip_version              = "IPv4"
      + location                = "francecentral"
      + name                    = "vm-ip"
      + resource_group_name     = "tp1_terraform"
      + sku                     = "Standard"
      + sku_tier                = "Regional"
    }

  # azurerm_resource_group.main will be created
  + resource "azurerm_resource_group" "main" {
      + id       = (known after apply)
      + location = "francecentral"
      + name     = "tp1_terraform"
    }

  # azurerm_subnet.main will be created
  + resource "azurerm_subnet" "main" {
      + address_prefixes                              = [
          + "10.0.1.0/24",
        ]
      + default_outbound_access_enabled               = true
      + id                                            = (known after apply)
      + name                                          = "vm-subnet"
      + private_endpoint_network_policies             = "Disabled"
      + private_link_service_network_policies_enabled = true
      + resource_group_name                           = "tp1_terraform"
      + virtual_network_name                          = "vm-vnet"
    }

  # azurerm_virtual_network.main will be created
  + resource "azurerm_virtual_network" "main" {
      + address_space                  = [
          + "10.0.0.0/16",
        ]
      + dns_servers                    = (known after apply)
      + guid                           = (known after apply)
      + id                             = (known after apply)
      + location                       = "francecentral"
      + name                           = "vm-vnet"
      + private_endpoint_vnet_policies = "Disabled"
      + resource_group_name            = "tp1_terraform"
      + subnet                         = (known after apply)
    }

Plan: 6 to add, 0 to change, 0 to destroy.

─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run
"terraform apply" now.
```

```bash
israel@hpvictusBJI:~/terraform$ terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following
symbols:
  + create

Terraform will perform the following actions:

  # azurerm_linux_virtual_machine.main will be created
  + resource "azurerm_linux_virtual_machine" "main" {
      + admin_username                                         = "israel"
      + allow_extension_operations                             = (known after apply)
      + bypass_platform_safety_checks_on_user_schedule_enabled = false
      + computer_name                                          = (known after apply)
      + disable_password_authentication                        = (known after apply)
      + disk_controller_type                                   = (known after apply)
      + extensions_time_budget                                 = "PT1H30M"
      + id                                                     = (known after apply)
      + location                                               = "francecentral"
      + max_bid_price                                          = -1
      + name                                                   = "super-vm"
      + network_interface_ids                                  = (known after apply)
      + os_managed_disk_id                                     = (known after apply)
      + patch_assessment_mode                                  = (known after apply)
      + patch_mode                                             = (known after apply)
      + platform_fault_domain                                  = -1
      + priority                                               = "Regular"
      + private_ip_address                                     = (known after apply)
      + private_ip_addresses                                   = (known after apply)
      + provision_vm_agent                                     = (known after apply)
      + public_ip_address                                      = (known after apply)
      + public_ip_addresses                                    = (known after apply)
      + resource_group_name                                    = "tp1_terraform"
      + size                                                   = "Standard_B1s"
      + virtual_machine_id                                     = (known after apply)
      + vm_agent_platform_updates_enabled                      = (known after apply)

      + admin_ssh_key {
          + public_key = <<-EOT
                ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINwv4hLNfexz23UO/krC/xs3KI1Nho+0xVCUnmLmn5fW cloud_tp1
            EOT
          + username   = "israel"
        }

      + os_disk {
          + caching                   = "ReadWrite"
          + disk_size_gb              = (known after apply)
          + id                        = (known after apply)
          + name                      = "vm-os-disk"
          + storage_account_type      = "Standard_LRS"
          + write_accelerator_enabled = false
        }

      + source_image_reference {
          + offer     = "almalinux-x86_64"
          + publisher = "almalinux"
          + sku       = "10-gen2"
          + version   = "latest"
        }

      + termination_notification (known after apply)
    }

  # azurerm_network_interface.main will be created
  + resource "azurerm_network_interface" "main" {
      + accelerated_networking_enabled = false
      + applied_dns_servers            = (known after apply)
      + id                             = (known after apply)
      + internal_domain_name_suffix    = (known after apply)
      + ip_forwarding_enabled          = false
      + location                       = "francecentral"
      + mac_address                    = (known after apply)
      + name                           = "vm-nic"
      + private_ip_address             = (known after apply)
      + private_ip_addresses           = (known after apply)
      + resource_group_name            = "tp1_terraform"
      + virtual_machine_id             = (known after apply)

      + ip_configuration {
          + gateway_load_balancer_frontend_ip_configuration_id = (known after apply)
          + name                                               = "internal"
          + primary                                            = (known after apply)
          + private_ip_address                                 = (known after apply)
          + private_ip_address_allocation                      = "Dynamic"
          + private_ip_address_version                         = "IPv4"
          + public_ip_address_id                               = (known after apply)
          + subnet_id                                          = (known after apply)
        }
    }

  # azurerm_public_ip.main will be created
  + resource "azurerm_public_ip" "main" {
      + allocation_method       = "Static"
      + ddos_protection_mode    = "VirtualNetworkInherited"
      + fqdn                    = (known after apply)
      + id                      = (known after apply)
      + idle_timeout_in_minutes = 4
      + ip_address              = (known after apply)
      + ip_version              = "IPv4"
      + location                = "francecentral"
      + name                    = "vm-ip"
      + resource_group_name     = "tp1_terraform"
      + sku                     = "Standard"
      + sku_tier                = "Regional"
    }

  # azurerm_resource_group.main will be created
  + resource "azurerm_resource_group" "main" {
      + id       = (known after apply)
      + location = "francecentral"
      + name     = "tp1_terraform"
    }

  # azurerm_subnet.main will be created
  + resource "azurerm_subnet" "main" {
      + address_prefixes                              = [
          + "10.0.1.0/24",
        ]
      + default_outbound_access_enabled               = true
      + id                                            = (known after apply)
      + name                                          = "vm-subnet"
      + private_endpoint_network_policies             = "Disabled"
      + private_link_service_network_policies_enabled = true
      + resource_group_name                           = "tp1_terraform"
      + virtual_network_name                          = "vm-vnet"
    }

  # azurerm_virtual_network.main will be created
  + resource "azurerm_virtual_network" "main" {
      + address_space                  = [
          + "10.0.0.0/16",
        ]
      + dns_servers                    = (known after apply)
      + guid                           = (known after apply)
      + id                             = (known after apply)
      + location                       = "francecentral"
      + name                           = "vm-vnet"
      + private_endpoint_vnet_policies = "Disabled"
      + resource_group_name            = "tp1_terraform"
      + subnet                         = (known after apply)
    }

Plan: 6 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

azurerm_resource_group.main: Creating...
azurerm_resource_group.main: Still creating... [00m10s elapsed]
azurerm_resource_group.main: Still creating... [00m20s elapsed]
azurerm_resource_group.main: Still creating... [00m30s elapsed]
azurerm_resource_group.main: Creation complete after 32s [id=/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/tp1_terraform]
azurerm_virtual_network.main: Creating...
azurerm_public_ip.main: Creating...
azurerm_virtual_network.main: Still creating... [00m11s elapsed]
azurerm_public_ip.main: Still creating... [00m11s elapsed]
azurerm_public_ip.main: Creation complete after 14s [id=/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/tp1_terraform/providers/Microsoft.Network/publicIPAddresses/vm-ip]
azurerm_virtual_network.main: Creation complete after 17s [id=/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/tp1_terraform/providers/Microsoft.Network/virtualNetworks/vm-vnet]
azurerm_subnet.main: Creating...
azurerm_subnet.main: Still creating... [00m10s elapsed]
azurerm_subnet.main: Creation complete after 14s [id=/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/tp1_terraform/providers/Microsoft.Network/virtualNetworks/vm-vnet/subnets/vm-subnet]
azurerm_network_interface.main: Creating...
azurerm_network_interface.main: Creation complete after 8s [id=/subscriptions/667b0098-1b06-4151-a849-d0a09926709c/resourceGroups/tp1_terraform/providers/Microsoft.Network/networkInterfaces/vm-nic]
azurerm_linux_virtual_machine.main: Creating...
azurerm_linux_virtual_machine.main: Still creating... [00m11s elapsed]
azurerm_linux_virtual_machine.main: Still creating... [00m21s elapsed]
azurerm_linux_virtual_machine.main: Still creating... [00m31s elapsed]
azurerm_linux_virtual_machine.main: Still creating... [00m41s elapsed]
azurerm_linux_virtual_machine.main: Still creating... [00m51s elapsed]
```

**🌞 Prouvez avec une connexion SSH sur l'IP publique que la VM est up**

```bash
israel@hpvictusBJI:~/terraform$ ssh -i ~/.ssh/cloud_tp1 israel@20.199.99.249
The authenticity of host '20.199.99.249 (20.199.99.249)' can't be established.
ED25519 key fingerprint is SHA256:VAiduo6Bc4DFx7v65iFc1DJNoep6o3oy9atTeSKkpB4.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '20.199.99.249' (ED25519) to the list of known hosts.
[israel@super-vm ~]$
```

### Fichiers à rendre

- `main.tf`
- tout autre fichier utilisé par Terraform (je vous propose des fichiers de base plus bas)

```bash
israel@hpvictusBJI:~/terraform$ cat main.tf
# main.tf

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_virtual_network" "main" {
  name                = "vm-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "main" {
  name                 = "vm-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_network_interface" "main" {
  name                = "vm-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main.id
  }
}

resource "azurerm_public_ip" "main" {
  name                = "vm-ip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_linux_virtual_machine" "main" {
  name                = "super-vm"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_B1s"
  admin_username      = var.admin_username
  network_interface_ids = [
    azurerm_network_interface.main.id,
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = file(var.public_key_path)
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
    name                 = "vm-os-disk"
  }

  source_image_reference {
    publisher = "almalinux"
    offer     = "almalinux-x86_64"
    sku       = "10-gen2"
    version   = "latest"
  }
}
```
