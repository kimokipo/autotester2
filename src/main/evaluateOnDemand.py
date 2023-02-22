import os
import time
import subprocess
import sys
from isolate import *
from ProjectEnv import ProjectEnv
import evaluate
import setup
import utility
import importlib
import csv

# Fichier stockant les paths utiles
from variables import *

def evaluateOnDemand(project_link : str):
    
    list_lien = project_link.split(paths["gitlabArbre"])[1].split("/")

    matiere = list_lien[0]
    student_name = list_lien[1]
    tp = list_lien[2].split('.git')[0]

    print("matiere : " + matiere + " student_name : " + student_name + " tp : "+ tp)
    
    project_path = paths[matiere]["repository_path"] 

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


    # Récupérer la liste des scenarios
    setup.setup(matiere,tp)
    project_folder = os.path.join(paths[matiere]["config_path"], tp)
    sys.path.append(project_folder)
    fichier_config = importlib.import_module("config") # Import dynamique du fichier de configuration 
    sys.path.remove(project_folder)
    scenarios = []
    modalites = False
    if (os.path.exists(tp_path + "/modalites.txt")):
        modalites = True
        scenarios = utility.get_scenarios(tp_path + "/modalites.txt", fichier_config.SCENARIOS)

    if (scenarios == [] and fichier_config.SCENARIOS_To_Test != None):
        scenarios = fichier_config.SCENARIOS_To_Test

    scenarios_name = [scenario.run.__name__ for scenario in scenarios]
                                                         
    evaluate.evaluate(True, modalites, matiere, tp, student_name, "evaluations/retour",  *scenarios_name) 

    