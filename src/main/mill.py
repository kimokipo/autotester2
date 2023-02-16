import os
import time
import subprocess
import sys
from isolate import *
from ProjectEnv import ProjectEnv
import evaluate
import utility
import importlib
import csv

# Fichier stockant les paths utiles
from variables import *

WAIT_TIME = 5 # Temps en secondes entre 2 boucles de la moulinette

def mill(matiere : str, tp : str):
    
    # Recuperation de la liste des chemins vers les dossiers eleve
    
    students = []
    students_info = '1sn-autotester.csv'
    with open(students_info) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            students.append(row[3])
    students = students[1:]

    project_path = paths[matiere]["repository_path"]

    # Setup de la "liste" des derniere revision de modalite controlee
    last_control = {}
    for student_name in students :
        if student_name != 'khammi':
            continue

        tp_path = project_path + "/" + student_name + "/" + tp

        list_directory = tp_path.split('/')
        for i in range(0,len(list_directory)+1):
            try:
                os.mkdir('/'.join(list_directory[0:i]))
            except OSError as error:
                print(error)  

        depot = "https://" + paths["username"] + ":" + paths["password"] + "@gitlab.com/" + paths["gitlabArbre"] + matiere + "/" + student_name + "/" + tp + ".git"
        gitClone = "git clone " + depot + " " + tp_path
        sp.run(gitClone, shell=True)

        # Recuperation de la derniere revision de modalites
        #svnUpdate = "svn update " + tp_path
        #subprocess.run(svnUpdate, shell=True)
        
        #svnInfoCommand = "svn info " + tp_path + "/modalites.txt"
        #procInfo = subprocess.run(svnInfoCommand, stdout=subprocess.PIPE, shell=True)
        #info = str(procInfo.stdout.decode(sys.stdout.encoding))

        os.chdir(tp_path)
        gitLog = "git log modalites.txt"
        procInfo = subprocess.run(gitLog, stdout=subprocess.PIPE, shell=True)
        info = str(procInfo.stdout.decode(sys.stdout.encoding))
        splitInfo = info.split("commit")
        for c in splitInfo:
            if (c != "" and "Retour automatique des modalites" not in c):
                last_control[tp_path] = c.split()[0]
                break
            
        os.chdir("../../../../")
    
    # Boucle Principale
    update_student_counter = 0
    while True :
        
        time.sleep(WAIT_TIME)
        update_student_counter += 1
        
        # MàJ régulière des dossier élèves
        if update_student_counter == 10 :
            update_student_counter = 0
                
        #recherche d'une demande de tests
        for student_name in students :
            if student_name != 'khammi':
                continue

            tp_path = project_path + "/" + student_name + "/" + tp

            depot = "https://" + paths["username"] + ":" + paths["password"] + "@gitlab.com/" + paths["gitlabArbre"] + matiere + "/" + student_name + "/" + tp + ".git"
        
            # Recuperation de la derniere revision ou modalites a ete modifie
            #svnUpdate = "svn update " + tp_path
            #subprocess.run(svnUpdate, shell=True)

            os.chdir(tp_path)
            gitchekout = "git checkout main"
            sp.run(gitchekout, shell = True) 
            gitpull = "git pull --no-edit " + depot + " main"
            sp.run(gitpull, shell = True)

            gitLog = "git log modalites.txt"
            procInfo = subprocess.run(gitLog, stdout=subprocess.PIPE, shell=True)
            info = str(procInfo.stdout.decode(sys.stdout.encoding))

            revision = last_control[tp_path] 
            splitInfo = info.split("commit")
            for c in splitInfo:
                if (c != "" and "Retour automatique des modalites" not in c):
                    revision = c.split()[0]
                    break
            os.chdir("../../../../")
            
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
                                                     
                evaluate.evaluate(True, "mill", matiere, tp, student_name, "evaluations/retour",  *scenarios_name) 

                
                # Renvoi des sources avec les divers retours
                #svnCommit = "svn commit -m \" Retour du test automatique \" " + tp_path + "/retour.txt"
                #subprocess.run(svnCommit, shell=True)
                
                # Maj de la revision
                last_control[tp_path] = revision