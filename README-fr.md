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
  * Champ personnalisé dans ServiceNow pour stocker le nom de l'objet Visual TOM (Traitements, Applications, Agents, etc.)
  * Python 3.10 ou supérieur ou PowerShell 7.0 ou supérieur
    * La gestion des logs n'est pas disponible sur les serveurs Windows

# Consignes

Le script peut être personnalisé pour répondre à vos besoins concernant les champs ServiceNow. Vous pouvez trouver les champs dans le REST API explorer de votre instance ServiceNow ([[https://YOUR-INSTANCE.service-now.com/now/nav/ui/classic/params/target/%24restapi.do]]).

Vous pouvez choisir entre le script PowerShell ou le script Python en fonction de votre environnement.
Vous devez remplacer FULL_PATH_TO_SCRIPT, BUSINESS_SERVICE, SHORT_DESCRIPTION, ASSIGNMENT_GROUP, CATEGORY et CALLER_ID par vos valeurs.

### Script PowerShell
1. Modifier le fichier config.ps1 avec vos identifiants ServiceNow et les noms des champs spécifiques
2. Créer une alarme dans Visual TOM pour déclencher le script (exemple ci-dessous pour un traitement à adapter)
  ```powershell
  powershell.exe -file FULL_PATH_TO_SCRIPT\ServiceNow_CreateTicket.ps1 -businessService "BUSINESS_SERVICE" -shortDescription "Job {VT_JOB_FULLNAME} has failed" -assignmentGroup "ASSIGNMENT_GROUP" -category "CATEGORY" -callerId "absyss.vtom" -objectName "{VT_FULL_JOBNAME}"
  ```

### Script Python
1. Modifier le fichier config.py avec vos identifiants ServiceNow et les noms des champs spécifiques
2. Créer une alarme dans Visual TOM pour déclencher le script (exemple ci-dessous pour un traitement à adapter)
Pour les serveurs Unix, vous pouvez utiliser la commande suivante pour exécuter le script :
  ```bash
# Générer un nom de fichier aléatoire
filename_out=$(mktemp "file_XXXXXX.txt")
echo "$filename_out"
# Créer un fichier avec EOF
cat << EOF > /tmp/$filename_out
{VT_JOB_LOG_OUT_CONTENT}
EOF

# Afficher le nom du fichier
echo "Std out file: $filename_out"

# Générer un nom de fichier aléatoire
filename_err=$(mktemp "file_XXXXXX.txt")

# Créer un fichier avec EOF
cat << EOF > "/tmp/$filename_err"
{VT_JOB_LOG_ERR_CONTENT}
EOF

# Afficher le nom du fichier
echo "Error out file: $filename_err"
python3 FULL_PATH_TO_SCRIPT/ServiceNow_CreateTicket.py --businessService BUSINESS_SERVICE --shortDescription "Job {VT_JOB_FULLNAME} has failed" --assignmentGroup ASSIGNMENT_GROUP --category CATEGORY --callerId "absyss.vtom" --objectName {VT_JOB_FULLNAME} --outAttachmentFile /tmp/$filename_out --outAttachmentName {VT_JOB_LOG_OUT_NAME}  --errorAttachmentFile /tmp/$filename_err --errorAttachmentName {VT_JOB_LOG_ERR_NAME}

rm /tmp/$filename_out /tmp/$filename_err
```

Pour les serveurs Windows, vous pouvez utiliser la commande suivante pour exécuter le script :
  ```shell
  python3 FULL_PATH_TO_SCRIPT/ServiceNow_CreateTicket.py --businessService BUSINESS_SERVICE --shortDescription "Job {VT_JOB_FULLNAME} has failed" --assignmentGroup ASSIGNMENT_GROUP --category CATEGORY --callerId "absyss.vtom" --objectName {VT_JOB_FULLNAME}
  ```

# Licence
Ce projet est sous licence Apache 2.0. Voir le fichier [LICENCE](license) pour plus de détails.


# Code de conduite
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg)](code-of-conduct.md)  
Absyss SAS a adopté le [Contributor Covenant](CODE_OF_CONDUCT.md) en tant que Code de Conduite et s'attend à ce que les participants au projet y adhère également. Merci de lire [document complet](CODE_OF_CONDUCT.md) pour comprendre les actions qui seront ou ne seront pas tolérées.
