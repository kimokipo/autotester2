import os
import time
import subprocess
import sys
from isolate import *
from ProjectEnv import ProjectEnv
import evaluate
import utility
import importlib

# Fichier stockant les paths utiles
from variables import *

WAIT_TIME = 5 # Temps en secondes entre 2 boucles de la moulinette

def mill(matiere : str, tp : str):
    
    # Recuperation de la liste des chemins vers les dossiers eleve
    students = [f.path for f in os.scandir(paths[matiere]["repository_path"]) if f.is_dir()][1:]
        
    # Setup de la "liste" des derniere revision de modalite controlee
    last_control = {}
    for stu_dir in students :

        tp_path = stu_dir + "/" + tp

        # Recuperation de la derniere revision de modalites
        svnUpdate = "svn update " + tp_path
        subprocess.run(svnUpdate, shell=True)
        
        svnInfoCommand = "svn info " + tp_path + "/modalites.txt"
        procInfo = subprocess.run(svnInfoCommand, stdout=subprocess.PIPE, shell=True)
        info = str(procInfo.stdout.decode(sys.stdout.encoding))
        splitInfo = info.split()
        try :
            index = splitInfo.index("Rev:")
        except ValueError:
            continue
        last_control[tp_path] = int(splitInfo[index + 1])
    
    # Boucle Principale
    update_student_counter = 0
    while True :
        
        time.sleep(WAIT_TIME)
        update_student_counter += 1
        
        # MàJ régulière des dossier élèves
        if update_student_counter == 10 :
            update_student_counter = 0
                
        #recherche d'une demande de tests
        for stu_dir in students :
            
            tp_path = stu_dir + "/" + tp
            
            # Recuperation de la derniere revision ou modalites a ete modifie
            svnUpdate = "svn update " + tp_path
            subprocess.run(svnUpdate, shell=True)
        
            svnInfoCommand = "svn info " + tp_path + "/modalites.txt"
            proc = subprocess.run(svnInfoCommand, stdout=subprocess.PIPE, shell=True)
            info = str(proc.stdout.decode(sys.stdout.encoding))
            splitInfo = info.split()
            try :
                index = splitInfo.index("Rev:")
            except ValueError:
                continue
            revision = int(splitInfo[index + 1])
            
            # Initialisation si nouveau TP
            if last_control[tp_path] == None :
                last_control[tp_path] = 0
    
            # Modalite a-t-il ete modifie depuis ?
            if revision != last_control[tp_path] :
                
                # Récupérer la liste des scenarios
                project_folder = os.path.join(paths[matiere]["config_path"], tp)
                sys.path.append(project_folder)
                fichier_config = importlib.import_module("config") # Import dynamique du fichier de configuration 
                sys.path.remove(project_folder)

                scenarios = utility.get_scenarios(tp_path + "/modalites.txt", fichier_config.SCENARIOS)

                scenarios_name = [scenario.run.__name__ for scenario in scenarios]
                                                        
                evaluate.evaluate(True, matiere, stu_dir.split('/')[-1], tp, *scenarios_name)

                # Renvoi des sources avec les divers retours
                svnCommit = "svn commit -m \" Retour du test automatique \" " + tp_path + "/retour.txt"
                subprocess.run(svnCommit, shell=True)
                
                # Maj de la revision
                last_control[tp_path] = revision