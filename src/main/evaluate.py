# Modules Python
import importlib
import sqlite3
import datetime
import sys
import subprocess as sp
from Section import Section
from scenarios.tools.TestsEtu import TestsEtu

# Modules featpp
from Scenario import Scenario
from ProjectEnv import ProjectEnv
from typeAnnotations import *
import utility

# Fichier stockant les paths utiles
from variables import *

TestsEtu = TestsEtu()

def evaluate(commit : bool, caller : str, matiere : str, tp : str, student : str, retour : str, *scenarios_name) -> None:

    '''
    Cycle d'execution manuelle des tests

    Paramètres :
        commit - bool : bool pour savoir si on dépose le fichier retour sur svn
        caller - str : nom de l'appelleur de la fonction evaluate pour distinguer entre main et mill.
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
    
    
    gitconfig1 = "git config --global user.email \"" + paths["mail"] + "\""
    gitconfig2 = "git config --global user.name \"" + paths["username"] + "\""
    sp.run(gitconfig1, shell = True)
    sp.run(gitconfig2, shell = True)
    
    depot = "https://" + paths["username"] + ":" + paths["password"] + "@gitlab.com/" + paths["gitlabArbre"] + matiere + "/" + student + "/" + tp + ".git"
    

    list_directory = student_project_folder.split('/')
    for i in range(0,len(list_directory)+1):
        try:
            os.mkdir('/'.join(list_directory[0:i]))
        except OSError as error:
            print(error)    
            
    
    gitClone = "git clone " + depot + " " + student_project_folder
    sp.run(gitClone, shell=True)

    os.chdir(student_project_folder)
    gitpull = "git pull --no-edit " + depot + " evaluations"
    sp.run(gitpull, shell = True)
    os.chdir("../../../../")


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
    #ajout du scenario evaluation des tests visibles chez etudiants.
    scenario_TestEtu = Scenario(testsEtu)
    scenarios_to_run.append(scenario_TestEtu)
    
    for scenario in SCENARIOS :
        if scenario.run.__name__ in scenarios_name:
            scenarios_to_run.append(scenario)

    #Jouer les scénarios à jouer
    database_address = os.path.join(project_folder, "database_test.db")
    modalities_address = os.path.join(project_folder, "modalites.txt")
    if (caller == "mill"):
        modalities_address = os.path.join(student_project_folder, "modalites.txt")
        os.chdir(student_project_folder)
        gitchekout = "git checkout main"
        sp.run(gitchekout, shell = True) 
        os.chdir("../../../../")
    
    results = utility.run_scenarios(scenarios_to_run, database_address, modalities_address, student, project_env, SCENARIOS)
    
    os.chdir(project_folder)
                        
    gitAddCommit = "git add database_test.db && git commit -m \" update automatique de la base de données\""
    sp.run(gitAddCommit, shell = True)

    depot_repo = "https://" + paths["username"] + ":" + paths["password"] + "@gitlab.com/" + paths["gitlabArbre"] + "repository.git"
    gitpush = "git push " + depot_repo 
    sp.run(gitpush, shell = True)
    os.chdir("../../../../")

    if (caller == "mill"):
        os.chdir(student_project_folder)
                        
        gitAddCommit = "git add modalites.txt && git commit -m \" Retour automatique des modalites\""
        sp.run(gitAddCommit, shell = True)

        gitpush = "git push " + depot + " main" 
        sp.run(gitpush, shell = True)
        os.chdir("../../../../")
    #Afficher les résultats où il faut
    results.append(utility.report(scenarios_to_run, results, database_address, student_name))

    utility.print_results(results, student_project_folder, dest_address , retour + '.txt', depot, 2, commit)

def testsEtu(project_env):
    results = [Section("Evaluation TestsEtu ", _title_Lvl = 1)]
    run = TestsEtu.run(project_env.student_project_folder, [])
    results.append(run)
    return results