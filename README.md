---
title: Manuel utilisateur autotester2 - Professeurs
numbersections: true
lang: fr-FR
---

Ce manuel est destiné à être utilisé par les professeurs qui souhaiteraient
utiliser le framework autotester2. Il explique comment installer le framework sur
une machine et/ou le configurer avec gitlab-ci, comment utiliser les différentes commandes que feat3p propose et
comment configurer les fichiers nécessaires au bon fonctionnement du framework.


Le diagramme de classe est disponible à l'URL :
tinyurl.com/v53amb9x  // mettre le nouveau diagramme de classe

### Table des matières

I. [Installation du framework](#installation)
II. [Architecture du framework](#architecture)
III. [Commandes](#commandes)
    A. [Récupérer le travail sur demande d'un élève](#mill)
    B. [Lancer un cycle de tests](#evaluate)
    C. [Lancer un cycle de tests sur une promo](#evaluateAll)
IV. [Documents utiles](#documents)
	A. [Fichier de configuration : config.py](#config)
	B. [Fichiers relatifs aux scripts de tests](#script)
	C. [Fichier de modalités : modalites.txt](#modalites)


# I. Installation du framework  <a id='installation'></a>

## Prérequis 
- ### Sur Machine
Les seuls prérequis pour l'installation sous une machine sont au niveau de Python. Pour le bon fonctionnement des
programmes, il faut avoir une version de Python 3 ou supérieure, avec la
majorité des modules classiques (os, sys, etc.) importés via Anaconda, par
exemple.

On précise toutefois ici que seule une machine Linux pourra accéder à la
fonctionnalité "isolate" qui permet d'exécuter des codes inconnus en toute
sécurité. Le reste de l'application fonctionne sur tous les systèmes
d'exploitation.
- ### Sur Gitlab - ci
Pour utiliser le framework sur Gitlab-ci avec une pipeline executant un runner, il est important d'utiliser l'image docker que nous avons creé et qui est meni de touts les dependances necessiares. 
il est à telecharger sur le lien suivant : 
// lien


## Comment installer  feat3p ?

* Pour télécharger le code source, et donc l'application, il suffit de rentrer
la commande suivante, en vous plaçant dans un répertoire vierge qui deviendra
feat3p.

```bash
git init
git clone https://gitlab.com/projet-long/AutoTester2
```
* Pour l'utilisation sous Gitlab-ci il suffit d'avoir accés au projet situé sur le meme lien gitlab : https://gitlab.com/projet-long/AutoTester2, et se rendre dans la section CI/CD -> Pipelines



# II. Architecture du framework <a id='architecture'></a>

Le diagramme de classe est disponible à l'URL :

tinyurl.com/v53amb9x // mettre le nouveau lien

# III. Commandes  <a id='commandes'></a>

Il vous faudra configurer l'environnement de feat3p. L'application a besoin de connaître plusieurs informations :
- username : celui du professeur utilisant le framework et qui a accés au projet AutoTester2 et aux dépots de tous les étudiants.
- password : Personal Access Tokens du professeur. 
- mail : son email
- gitlabArbre : Arboressance de groupes contenant les dépots des étudiants.
Pour chaque matiere : 
- le chemin du dossier (ou le lien du depot git à voir aprés) où tous vos projets seront créés, stockés puis depuis lequel ils seront envoyés.

Pour cela vous devez configurer le fichier "variables.json" situé au chemin "./autotester/src/variables.json", de la manière suivante :

```json
{   
    "username" : "kimokipo",
    "password" : "token",
    "mail" : "hammi.kamal.mpsi@hotmail.com",
    "gitlabArbre" : "projetlong1/2022-sn/tp-b1/",

    "pim": {
        "config_path" : "repository/projects/pim"
    },

    "tob": {
        "config_path" : "repository/projects/tob"
    }
}

```

Attention :

- il ne faut pas modifier les noms en noir comme "username" et "config_path" ect, cela engendrerait des erreurs


### A. Récupérer le travail sur demande d'un élève  <a id='mill'></a>

Une fois que tout a été configuré, l'utilisateur n'a plus qu'à lancer la commande suivante pour activer la détection automatique des demandes d'évaluation :

```bash
feat3p mill <matiere> <nom_projet>
```

Arguments :

* `matiere` : Le nom de la matiere dans `variables.json`.
* `nom_projet` : Il s'agit du nom du dossier dans lequel se trouve le fichier de configuration `config.py` concernant le projet que le professeur souhaite tester chez l'élève.

Dans les faits, cette commande va régulièrement effectuer les commandes **git pull** et **git log** sur le fichier modalites.txt afin de mettre à jour les
dépôts, puis de vérifier si le fichier de modalités a été modifié depuis le
dernier cycle de tests, auquel cas un cycle de tests est lancé. Le délai
d'attente entre deux vérifications des sources des élèves est de 5 secondes par
défaut. Celui-ci peut être changé depuis la variable **WAIT_TIME** dans le
fichier `mill.py`.

**TODO :** Il serait préférable que WAIT_TIME soit un argument de la commande : `--period`.

## B. Lancer un cycle de tests  <a id='evaluate'></a>

Il est possible pour le professeur de lancer un cycle de test pour un élève
sans tenir compte de ses contraintes (**XXX:** les quelles ? le fichier
`modalites.txt` afin de vérifier ce que l'élève a produit à la main. Pour cela
il faut utiliser la commande suivante :

```bash
./feat3p evaluate <matiere> <nom_projet> <etudiant> <retour> <scenario1> <scenario2> ...
```

Options :

* --commit : Ajouter cette option pour déposer le fichier retour sur depot git de l'etudiant.

Arguments :

* `nom_projet` : Il s'agit du nom du dossier dans lequel se trouve le fichier de configuration `config.py` concernant le projet que le professeur souhaite tester chez l'élève.

* `matiere` : Le nom de la matiere dans `variables.json`.

* `etudiant` : le nom du dépôt git de l'étudiant (en général son login).

* `retour` : nom du fichier retour

* `scenarios` : une liste de noms de scenario que le professeur souhaite voir testé chez l'élève.


## C. Lancer un cycle de tests sur une promo <a id='evaluateAll'></a>

Il est possible pour le professeur de lancer un cycle de test pour une promo. Pour cela il faut utiliser la commande suivante :

```bash
feat3p evaluateAll <matiere> <nom_projet> <students_info> <scenario1> <scenario2> ...
```

Options :

* --commit : Ajouter cette option pour déposer le fichier retour sur sur depot git des étudiants.

Arguments :

* `nom_projet` : Il s'agit du nom du dossier dans lequel se trouve le fichier de configuration `config.py` concernant le projet que le professeur souhaite tester chez l'élève.

* `matiere` : Le nom de la matiere auquel (dans `variables.json`).

* `students_info` : Un fichier .csv qui contient les informations des etudiants (login, nom, prenom, adresse mail)

* `retour` : nom du fichier retour

* `scenarios` : une liste de noms de scenario que le professeur souhaite voir testé chez les élèves.


# IV. Documents utiles <a id='documents'></a>

## A. Fichier de configuration : config.py  <a id='config'></a>

Le fichier de configuration d'un projet est la principale interface entre
feat3p et le professeur. Il s'agit d'un fichier python `config.py` dont un
exemple est donné lors de l'initialisation du projet. Il commence par les
importations nécessaires à son bon fonctionnement. A noter que `from tools
import *` permet d'importer tous les outils fournis par feat3p.

```
from Scenario import Scenario
from tools import *
from Text import Text
```

Puis il faut instancier les outils qui vont servir pour le projet, par exemple :

```
javaCompiler = JavaCompiler() 
blackBox = Blackbox()
```

Puis le professeur doit définir des scénarios de test. Pour cela il doit créer
une fonction python par scénario. Cette fonction permet de définir concrètement
quel test exécute le scénario et dans quel ordre. 

Le professeur est libre d'utiliser la syntaxe python pour y mettre des conditionnels par exemple.

En voici un exemple de compilation de programme en ADA:

```
def compilationada(project_env):
    results = [Section("Compilation des fichiers en ADA", _title_Lvl = 1)]
    for file in compile_files_ada:
        run = adacompiler.run(project_env, file)
        run.penalty = 1 if (run.result == "ERROR") else 0
        results.append(run)
    return results
```

Le professeur peut ajouter des sections avec des niveaux pour mieux structurer
le fichier retour.

Voici un example de différents niveaux de sections:

Niveau 1:
```
#########################################
# Modification des fichiers fournis
#########################################
```

Niveau 2:
```
===============================================
# Fichiers qui NE devaient PAS être modifiés
===============================================
```


Le professeur peut ajouter des pénalités selon les résultats des différents
tests comme on peut le voir dans l'exemple précédent.

Afin d'être le plus flexible possible, le professeur peut se renseigner sur
les différents attributs des différents objets dans le `README_DEV.md`


Après avoir défini l'ensemble de ces fonctions, le professeur doit créer les
scénarios à proprement parler et les ajouter dans une liste à la fin du fichier
de configuration. 

Pour créer un scénario, il y a plusieurs paramètres :

* **_run**, une fonction (celle définie préalablement) qui correspond à ce que fait concrètement le scénario.

* **_nb_attempts**, un entier correspondant au nombre de fois maximum qu'un élève peut demander à exécuter ce scénario. Par défaut fixé à l'infini.

* **_delay**, un entier correspondant au nombre de secondes définissant le délai minimum entre deux exécutions de ce scénario. Par défaut fixé à une variable globale DELAY = 5 (minutes).

* **_visible**, un booléen indiquant si le scénario sera ou non visible pour l'étudiant. Cela peut être utile pour des tests particuliers, d'évaluation par exemple. Par défaut fixé à vrai. 

* **_mark**, un entier indiquant combien de points au total représente le scénario, utile si le professeur décide d'utiliser des pénalités. Par défaut fixé à 0.

Ainsi, à la fin du fichier de configuration, on trouve deux listes. La première
correspond aux scenarios qui vont réellement faire partie du projet : 

```
SCENARIOS = [
    Scenario(scenario1),
    Scenario(scenario2),
    Scenario(scenario_example, _visible = false, _mark = 5)
]
```

La seconde correspond aux scenarios utilisés par le professeur pour tester ses propres fichiers en interne avec la commande **runtests** : 

```
SCENARIOS_TESTS = SCENARIOS + [
    Scenario(scenario_test),
    Scenario(bad_scenario_test),
]
```


### Note concernant la sécurité de la machine lors de l'exécution du code d'un étudiant

Cette section n'a d'intérêt que lorsque le besoin de redéfinir ponctuellement
la fonction `run()` d'un outil se présente (ce qui devrait ne se produire que
peu). Hors de ce cas de figure, cette section peut être ignorée. Cette section
relève plus du développement que de l'utilisation, mais présente des problèmes
pouvant être rencontrés par les enseignants.

Afin d'assurer la sécurité des machines des enseignants, tout code auquel on ne
peut pas faire confiance (notamment celui des étudiants) doit être exécuté dans
un environnement isolé.
Ainsi, si la fonction `run()` d'un outil exécutant un code auquel on ne fait
pas confiance est redéfinie, les appels d'exécution de ce code doivent se faire
avec la fonction `isolate_run(id, options, prog)` définie dans le fichier
`isolate.py`, `id` étant accessible depuis l'attribut `ProjectEnv.isolate_id`,
`options` permettant de contrôler les restrictions appliquées sur le code
exécuté (cf. http://www.ucw.cz/moe/isolate.1.html), et `prog` contenant un
appel en ligne de commande de syntaxe similaire à celui de `SubProcess.run()`.

À noter cependant que toutes les sources et les fichiers avec lesquels le code
doit interagir au cours de son exécution doivent avoir été déplacés dans le
dossier correspondant à l'environnement isolé avant l'exécution. L'intégralité
du dossier source de l'étudiant est déplacée au début du cycle de tests,
cependant tout fichier nécessaire et extérieur au dossier source de l'étudiant
doit être déplacé à l'aide de la fonction `isolate_mv(isolated_dir, files)`,
`isolated_dir` étant accessible depuis l'attribut
`ProjectEnv.path_to_isolate_env`, et `files` étant une liste de chemins
(absolus ou relatifs à l'environnement d'exécution de FEAT++) vers les
fichiers/dossiers à déplacer.

À noter également que les appels de commandes externes à l'environnement isolé
(par exemple `sh` ou `java`) par la fonction `isolate_run(id, options, prog)`
doivent être fait avec le chemin absolu de l'exécutable (par exemple :
`/usr/bin/sh` ou `/usr/bin/java`), et que les chemins vers des fichiers dans
l'environnement isolé dans la commande passée dans le paramètre `prog` doivent
être relatifs à la racine de l'environnement isolé (par exemple :
"src/TP_java/HelloWorld.java").

Un problème peut survenir dans le cas où le chemin absolu donné pour un
exécutable est en réalité un lien symbolique. Le problème peut être contourné
en utilisant la commande `realpath` ou `readlink` (par exemple :
`$(/usr/bin/realpath /usr/bin/java)`), ou en remplaçant le chemin par le
contenu d'une variable d'environnement dans laquelle le chemin réel a été
enregistré au préalable (par exemple : `PATHTOJAVA=$(realpath $(which java))`).


## B. Fichiers relatifs aux scripts de tests  <a id='script'></a>

### B.1 Les fichiers du dossier ScriptsTests  <a id='ScriptsTests'></a>

Ce dossier contient tous les fichiers qui vont devoir être appelé par les outils et qui ne seront pas chez l'étudiant. Par exemple pour les tests en boîte noire, on trouvera ici les fichiers qui permettront de comparer le résultat et qui doivent se terminer par `.expected` et les fichiers qui permettent de décrire ce que doit executer le test en boite noire, ceux-ci doivent se terminer par `.run`. En voici deux exemples :

__exempleConfiantTricheurSujet.run__

```bash
!/bin/bash
/usr/lib/jvm/java-11-openjdk-amd64/bin/java allumettes.Partie -confiant Ordinateur@rapide Tricheur@tricheur << EOF
EOF
```

Pour l'instant, il faut mettre le chemin complet pour appeler des logiciels.

__exempleConfiantTricheurSujet.expected__

```
Nombre d'allumettes restantes : 13
Au tour de Ordinateur.
Ordinateur prend 3 allumettes.

Nombre d'allumettes restantes : 10
Au tour de Tricheur.
Tricheur prend 1 allumette.

Nombre d'allumettes restantes : 1
Au tour de Ordinateur.
Ordinateur prend 1 allumette.
Ordinateur a perdu !
Tricheur a gagné !
```

### B.2 Les fichiers du dossier TestsProject  <a id='TestsProject'></a>

Le but de ce dossier est de permettre l'utilisation de la commande **runtests**. Le fichier le plus important de ce dossier est  `tests_runner.py`. Celui-ci contient un dictionnaire python qui permet de préciser quel scenario de quel dossier doit bien s'exécuter ou doit mal s'exécuter. En effet, pour vérifier le bon fonctionnement de son projet, le professeur peut simuler le code des élèves de telle sorte que les résultats des scénarios de tests doivent être positifs ou négatifs. 

Ce fichier est en directe corrélation avec la liste __SCENARIOS_TESTS__ définie dans le fichier config.py. Le professeur a connaissance des scénarios qu'il a placés dans cette liste pour ses tests personnels.

Ce dictionnaire est écrit comme suit :

```
TESTS = {
    "ExampleTestOK" : True,
    "ExampleTestKO" : {
        "scenario2" : True,
        "scenario_test" : False,
        "bad_scenario_test" : False
    },
}
```

__ExampleTestOk__ est un dossier qui contient une simulation de fichier source d'un élève tel que tous les tests de __SCENARIOS_TESTS__ doivent bien s'exécuter.

__ExampleTestKO__ est un dossier qui contient une simulation de fichier source d'un élève tel que le scenario2 doit bien s'exécuter tandis qu'il doit y avoir au moins une erreur en exécutant les deux autres.




## C. Fichier de modalités : modalites.txt <a id='modalites'></a>

Le fichier `modalites.txt` est généré lors de la [configuration d'un projet](#config). Le fichier de modalités est le support que les étudiants utilisent pour demander une évaluation de leur code. Ce fichier contient plusieurs blocs de textes, chacun relatif à un scénario de tests écrit par un professeur. Chaque bloc de texte contient le nom du scénario, la dernière date d'utilisation de ce scénario, la prochaine date à laquelle il pourra être relancé et enfin le nombre de tentatives restantes et déjà effectuées. Pour identifier les scénarios qu'un étudiant veut jouer, il suffit que ce dernier remplace le terme "non" écrit à côté du nom du scénario par "oui". Il est aussi possible de jouer tous les scénarios en remplaçant "non" par "oui" sur la première ligne du fichier de modalités, ainsi que de ne jouer que les scénario sans restriction du nombre de tentatives en remplaçant "non" par "oui" sur la deuxième ligne du fichier. Voici un exemple de fichier de modalités :

```txt
Voulez-vous jouer tous les tests ? non
Voulez-vous jouer tous les tests qui n'ont pas de restriction de tentatives (infini) ? non

scenario1 : non
    nombre de tentatives infini, vous avez joue ce test 3 fois
    derniere tentative = 2021-03-03 15:52:16.828228
    prochaine tentative possible = 2021-03-03 15:52:21.828228

scenario2 : non
    nombre de tentatives restantes = 10
    derniere tentative = 2021-03-03 15:52:16.828228
    prochaine tentative possible = 2021-03-03 15:52:21.828228
```

Si jamais un étudiant modifie et compromet ce fichier en supprimant ou ajoutant une ligne ou s'il écrit autre chose que "oui" ou "non", alors ce dernier est prévenu de la compromission, aucun scénario n'est joué et le fichier de modalité est réinitialisé. 
