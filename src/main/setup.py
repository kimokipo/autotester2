# Modules Python
import importlib
import sqlite3
import datetime
import sys
import subprocess as sp

# Modules featpp
from Scenario import Scenario
from ProjectEnv import ProjectEnv
from typeAnnotations import *
import utility
import evaluate

# Fichier stockant les paths utiles
from variables import *
import json
import csv


def setup(matiere : str, tp : str):

    depot = "https://" + paths["username"] + ":" + paths["password"] + "@gitlab.com/" + paths["gitlabArbre"] + "repository.git"
    gitClone = "git clone " + depot
    sp.run(gitClone, shell=True)

    project_folder = os.path.join(paths[matiere]["config_path"], tp)
    database_address = os.path.join(project_folder, "database_test.db")
    students_info = "repository/1sn-autotester.csv"

    groupe_tp = []
    students_name = []
    with open(students_info) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            students_name.append(row[3])
            groupe_tp.append(row[4])
    students_name = students_name[1:]
    groupe_tp = groupe_tp[1:]

    # Creating a database of all students and scenarios if it doesn't exist
    # Adding scenarios into scenarios.json    ###### USED IN THE WEBSITE
    if not os.path.exists(database_address):
        sys.path.append(project_folder)
        try :
            fichier_config = importlib.import_module("config")
        except ModuleNotFoundError:
            sys.path.remove(project_folder)
            print("Fichier config.py non trouvé ou mal écrit. Opération avortée.\n")
            sys.exit(1)
        sys.path.remove(project_folder)
        f = open('scenarios.json',)
        scenarios = json.load(f)
        scenarios[matiere][tp] = [scenario.run.__name__ for scenario in fichier_config.SCENARIOS]
        utility.create_database(database_address, fichier_config.SCENARIOS, students_name, groupe_tp)
    
    return students_name
    