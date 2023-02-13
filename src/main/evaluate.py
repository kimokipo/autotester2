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

# Fichier stockant les paths utiles
from variables import *


def evaluate(commit : bool, matiere : str, tp : str, student : str, retour : str, *scenarios_name) -> None:

    '''
    Cycle d'execution manuelle des tests

    Paramètres :
        commit - bool : bool pour savoir si on dépose le fichier retour sur svn
        student - String : Login de l'etudiant
        tp - String : nom du projet
        matiere - String : nom de la matière
        retour - String : nom du fichier retour
        *scenarios_name - List(String) : Liste de nom de scénarios à effectuer
    '''

    student_path = os.path.join(paths[matiere]["repository_path"], student)
    project_folder = os.path.join(paths[matiere]["config_path"], tp)

    project_env = ProjectEnv(student_path + "/" + tp, project_folder)

    #Definition de tous les chemins nécessaires à partir de l'environnement donné en argument
    student_project_folder = os.path.join(student_path, tp)
    # Recuperation de la derniere revision
    
    
    gitconfig1 = "git config --global user.mail \"" + paths["mail"] + "\""
    gitconfig2 = "git config --global user.name \"" + paths["username"] + "\""
    sp.run(gitconfig1, shell = True)
    sp.run(gitconfig2, shell = True)
    
    depot = "https://" + paths["username"] + ":" + paths["password"] + "@gitlab.com/" + paths["gitlabArbre"] + matiere + "/" + student + "/" + tp + ".git"
    gitPull = "git pull " +  depot

    list_directory = student_project_folder.split('/')
    for i in range(0,len(list_directory)+1):
        try:
            os.mkdir('/'.join(list_directory[0:i]))
        except OSError as error:
            print(error)    
            
    
    print(os.listdir())
    print("student_project_folder " + student_project_folder)
    os.chdir(student_project_folder)
    sp.run(gitPull, shell=True)
    os.chdir("../../../../")
    gitClone = "git clone " + depot + " " + student_project_folder
    sp.run(gitClone, shell=True)
    print(os.listdir())

    #svnUpdate = "svn update " + student_project_folder
    #sp.run(svnUpdate, shell=True)
    
    student_name = os.path.split(student_path)[1]
    dest_address = os.path.join(student_path, tp, retour + '.txt')
    
    #Importation du fichier de configuration du projet
    sys.path.append(project_folder)
    fichier_config = importlib.import_module("config") # Import dynamique du fichier de configuration 
    sys.path.remove(project_folder)

    SCENARIOS = fichier_config.SCENARIOS # type: ignore
    
    #Selection des scenarios à jouer
    scenarios_to_run =[]
    for scenario in SCENARIOS :
        if scenario.run.__name__ in scenarios_name:
            scenarios_to_run.append(scenario)

    #Jouer les scénarios à jouer
    database_address = os.path.join(project_folder, "database_test.db")
    modalities_address = os.path.join(project_folder, "modalites.txt")
    results = utility.run_scenarios(scenarios_to_run, database_address, modalities_address, student, project_env, SCENARIOS)
    
    #Afficher les résultats où il faut
    
    utility.print_results(results, student_project_folder, dest_address , retour + '.txt', depot, 2, commit)
