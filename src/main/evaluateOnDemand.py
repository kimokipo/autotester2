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

def evaluateOnDemand(project_student_link : str, *tp_folders):

    student_name = project_student_link.split("/")[-1]

    matiere = paths["matiere"]

    print("matiere : " + matiere + " student_name : " + student_name)
    student_path = matiere + "/" + student_name

    list_directory = student_path.split('/')
    for i in range(0,len(list_directory)+1):
        try:
            os.mkdir('/'.join(list_directory[0:i]))
        except OSError as error:
            print(error)  

    depot = "https://" + paths["username"] + ":" + paths["password"] + "@" + paths["gitlabArbre"].split("https://")[1] + "/" + student_name + ".git"
    gitClone = "git clone " + depot + " " + student_path
    sp.run(gitClone, shell=True)

    for tp in tp_folders:

        print("tp : "+ tp)
        tp_path = student_path + "/" + tp
        # Récupérer la liste des scenarios
        setup.setup(matiere,tp)
        project_folder = "repository/projects/" + tp
        sys.path.append(project_folder)
        fichier_config = importlib.import_module("config")
        try:
            importlib.reload(fichier_config)
        except UnboundLocalError as error:
            print(error) # Import dynamique du fichier de configuration 
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
        del fichier_config
