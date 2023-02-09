import subprocess as sp
from typeAnnotations import *
import os

from variables import *

"""
    Ce module contient les fonctions relatives à la gestion d'un environement isolé pour exécuter
    les codes des étudiants en toute sécurité
"""

PATH_ISOLATE_CALL = os.path.join(featpp_path, "isolate", "isolate_call.sh") # chemin auquel sera le fichier isolate_call.sh après l'installation du framework


#TODO : gestion droit d'accès (simple ajout sudo avec gestion mdp depuis fichier ?)
#TODO : type de retour des fonction d'isolate 

@argumentType("id", int)
@argumentType("options", str)
@returnType(str)
def isolate_init(id, options=""):
    
    """
        Initialisation d'un environement isolé pour l'exécution du code d'un étudiant

        Paramètres :
            id : int - L'identifiant (unique) de l'environement à créer
                (peut par exemple être le login de l'étudiant)
            options : str - Une chaine de caractères contenant les options a utilisé par l'environement
                écrite de la même manière quelles seraient dans une ligne de commande classique
    """
    
    # exemple : isolate_init(0)

    command = ["sudo", PATH_ISOLATE_CALL, "init", "-b", str(id)]
    
    opts = options.split(" ") # Séparation des différents arguments des options
    for o in opts: # Ajout des options à la ligne de commande
        command.append(o)
        
    # command.append("--init") # Dépalcé dans le fichier isolate_call.sh
    
    isolated_env = sp.run(command, stdout=sp.PIPE, text=True)
    isolated_dir = str(isolated_env.stdout).strip()
    return isolated_dir

@argumentType("isolate_dir", str)
@argumentType("files", {list : str})
@returnType(sp.CompletedProcess)
def isolate_mv(isolate_dir, files):

    """
        Déplacement des fichiers sources de l'étudiant vers l'environement isolé

        Paramètres :
            isolate_dir : string - Le chemin absolu vers le répertoire isolé crée lors de l'initialisation de l'environement isolé
            files : liste de string - La liste des chemins des fichiers/dossiers à déplacer dans l'environement isolé
    """
    
    # exemple : isolate_mv("/var/local/lib/isolate/0", ["pveyet/src", "reponses/resultat_attendu.txt", ...])

    # TODO : tester le bon fonctionnement
    if isolate_dir[-1] == "/":
        isolate_dir = isolate_dir[:-1]
        
    if isolate_dir[-2:-1] == "\\":
        isolate_dir = isolate_dir[:-2]

    command = ["sudo", PATH_ISOLATE_CALL, "move", isolate_dir]
    
    command = command + files
    
    cp_state = sp.run(command, stdout=sp.PIPE, text=True)
    #cp_return = str(cp_state.stdout)
    
    return cp_state


@argumentType("id", int)
@argumentType("options", str)
@argumentType("prog", {list : str})
@returnType(sp.CompletedProcess)
def isolate_run(id, options="", prog=":"):
    
    """
        Lancement de l'exécution d'un programme dans l'environement isolé
        
        Paramètre :
            id : int - l'identifiant (unique) de l'environement isolé définit lors de son initialisation
            options : str - Une chaine de caractères contenant les options a utilisé par l'environement
                écrite de la même manière qu'elles le seraient dans une ligne de commande classique
            prog : liste de str - Une chaine de caractères contenant l'appel en ligne de commande du programme à exécuter
                écrite de la même manière qu'elles le seraient dans une ligne de commande classique 
    """
    
    # exemple : isolate_run(0, "-p", ["/usr/bin/sh", "hello_world.sh"])
    
    command = ["sudo", PATH_ISOLATE_CALL, "run", "-b", str(id)]
    
    opts = options.split(" ") # Séparation des différents arguments des options
    for o in opts: # Ajout des options à la ligne de commande
        command.append(o)
    
    command.append("--run")
    command.append("--")
    
    #args = prog.split(" ") # Séparation des différents arguments du programme à exécuter
    #for a in args: # Ajout du programme à exécuter à la ligne de commande
    #   command.append(a)
    command = command + prog # ajout du programme à exécuter à la commande
    
    isolated_run = sp.run(command,stdout=sp.PIPE, text= True)
    #run_output = str(isolated_run.stdout)
    return isolated_run


@argumentType("isolate_dir", str)
@argumentType("files", {list : str})
@argumentType("rep", str)
@returnType(sp.CompletedProcess)
def isolate_get_res(isolate_dir, files, rep):
    
    """
        Récupération des fichiers de sortie du programme exécuté dans l'environement

        Paramètres :
            isolate_dir : string - Le chemin absolu vers le répertoire isolé crée lors de l'initialisation de l'environement isolé
            files : liste de string - La liste des chemins (en partant de la racine de l'environement isolé) des fichiers/dossiers à récupérer depuis l'environement isolé
            rep : string - Le chemin vers le dossier dans lequel les sorties récupérées seront stockées
    """
    
    # exemple : isolate_get_res("/var/local/lib/isolate/0", ["tool_output_isole/*"], "tool_output_local")
    
    # TODO : tester le bon fonctionnement
    if isolate_dir[-1] == "/":
        isolate_dir = isolate_dir[:-1]
        
    if isolate_dir[-2:-1] == "\\":
        isolate_dir = isolate_dir [:-2]
    
    command = ["sudo", PATH_ISOLATE_CALL, "get_results"]
    
    for f in files:
        command.append(isolate_dir + "/box/" + f)
        
    command.append(rep)
    
    cp_state = sp.run(command, stdout=sp.PIPE, text=True)
    #cp_return = str(cp_state.stdout)
    
    return cp_state


@argumentType("id", int)
@argumentType("options", str)
@returnType(sp.CompletedProcess)
def isolate_clean(id, options=""):

    """
        Desctruction de l'environement isolé pour l'exécution du code d'un étudiant

        Paramètres :
            id : int - L'identifiant (unique) de l'environement isolé définit lors de son initialisation
            options : str - Une chaine de caractères contenant les options a utilisé par l'environement
                écrite de la même manière quelles seraient dans une ligne de commande classique
    """
    
    # exemple : isolate_clean(0)

    command = ["sudo", PATH_ISOLATE_CALL, "clean", "-b", str(id)]
    
    opts = options.split(" ")
    for o in opts:
        command.append(o)
    
    # command.append("--cleanup") # déplacé dans le fichier isolate_call.sh
    
    isolated_cleanup = sp.run(command, stdout=sp.PIPE, text=True)
    #cleanup_return = str(isolated_cleanup.stdout)
    
    return isolated_cleanup
