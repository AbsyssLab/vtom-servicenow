# Intégration Visual TOM ServiceNow
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE.md)&nbsp;
[![fr](https://img.shields.io/badge/lang-en-red.svg)](README.md)  

Ce projet fournit des scripts pour créer et gérer des tickets ServiceNow à partir de Visual TOM.
Pour éviter la création de trop de tickets, le script vérifie si un ticket existe déjà pour le nom du traitement et n'est pas fermé.
Si c'est le cas, il créera un ticket enfant avec les nouvelles informations.
Si ce n'est pas le cas, il créera un nouveau ticket.

# Disclaimer
Aucun support ni garanties ne seront fournis par Absyss SAS pour ce projet et fichiers associés. L'utilisation est à vos propres risques.

Absyss SAS ne peut être tenu responsable des dommages causés par l'utilisation d'un des fichiers mis à disposition dans ce dépôt Github.

Il est possible de faire appel à des jours de consulting pour l'implémentation.

# Prérequis

  * Visual TOM 7.1.2 or supérieur
  * Instance ServiceNow avec API REST activée
  * Champ personnalisé dans ServiceNow pour stocker le nom du traitement complet depuis Visual TOM

# Consignes

Le script peut être personnalisé pour répondre à vos besoins concernant les champs ServiceNow. Vous pouvez trouver les champs dans le REST API explorer de votre instance ServiceNow ([[https://YOUR-INSTANCE.service-now.com/now/nav/ui/classic/params/target/%24restapi.do]]).

Vous pouvez choisir entre le script PowerShell ou le script Python en fonction de votre environnement.

### Script PowerShell
1. Modifier le fichier config.ps1 avec vos identifiants ServiceNow et les noms des champs spécifiques
2. Créer une alarme dans Visual TOM pour déclencher le script (exemple ci-dessous à adapter)
  ```powershell
  powershell.exe -file FULL_PATH_TO_SCRIPT\ServiceNow_CreateTicket.ps1 -businessService "My Service" -shortDescription "Job has failed" -assignmentGroup "SAP L2" -category "1F Other Unknown Bugs / Errors" -callerId "charles.beckley@example.com" -jobName "{VT_FULL_JOBNAME}"
  ```

### Script Python
1. Modifier le fichier config.py avec vos identifiants ServiceNow et les noms des champs spécifiques
2. Créer une alarme dans Visual TOM pour déclencher le script (exemple ci-dessous à adapter)
  ```python
  python FULL_PATH_TO_SCRIPT/ServiceNow_CreateTicket.py -businessService "My Service" -shortDescription "Job has failed" -assignmentGroup "SAP L2" -category "1F Other Unknown Bugs / Errors" -callerId "charles.beckley@example.com" -jobName "{VT_FULL_JOBNAME}"
  ```

# Licence
Ce projet est sous licence Apache 2.0. Voir le fichier [LICENCE](license) pour plus de détails.


# Code de conduite
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg)](code-of-conduct.md)  
Absyss SAS a adopté le [Contributor Covenant](CODE_OF_CONDUCT.md) en tant que Code de Conduite et s'attend à ce que les participants au projet y adhère également. Merci de lire [document complet](CODE_OF_CONDUCT.md) pour comprendre les actions qui seront ou ne seront pas tolérées.
