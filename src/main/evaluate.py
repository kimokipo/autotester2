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
import setup

# Fichier stockant les paths utiles
from variables import *

TestsEtu = TestsEtu()

def evaluate(commit : bool, modalites : bool, matiere : str, tp : str, student_name : str, retour : str, *scenarios_name) -> None:

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

    student_path = matiere + "/" + student_name
    project_folder = "repository/projects/" + tp

    project_env = ProjectEnv(student_path + "/" + tp, project_folder)

    #Definition de tous les chemins nécessaires à partir de l'environnement donné en argument
    student_project_folder = os.path.join(student_path, tp)
    # Recuperation de la derniere revision
    
    gitconfig1 = "git config --global user.email \"" + paths["mail"] + "\""
    gitconfig2 = "git config --global user.name \"" + paths["username"] + "\""
    sp.run(gitconfig1, shell = True)
    sp.run(gitconfig2, shell = True)
    
    depot = "https://" + paths["username"] + ":" + paths["password"] + "@" + paths["gitlabArbre"].split("https://")[1] + "/" + student_name + ".git"

    list_directory = student_path.split('/')
    for i in range(0,len(list_directory)+1):
        try:
            os.mkdir('/'.join(list_directory[0:i]))
        except OSError as error:
            print(error)    
            
    
    gitClone = "git clone " + depot + " " + student_path
    sp.run(gitClone, shell=True)

    os.chdir(student_project_folder)
    gitpull = "git pull --no-edit " + depot + " evaluations"
    sp.run(gitpull, shell = True)
    os.chdir("../../../")

    
    dest_address = os.path.join(student_project_folder, retour + '.txt')
    
    setup.setup(matiere,tp)

    #Importation du fichier de configuration du projet
    sys.path.append(project_folder)
    fichier_config = importlib.import_module("config") # Import dynamique du fichier de configuration 
    sys.path.remove(project_folder)
    SCENARIOS = fichier_config.SCENARIOS # type: ignore
    
    #Selection des scenarios à jouer
    scenarios_to_run =[]
    #ajout du scenario evaluation des tests visibles chez etudiants.
    if (fichier_config.Evaluate_TestsEtu == None or fichier_config.Evaluate_TestsEtu):
        scenario_TestEtu = Scenario(testsEtu)
        scenarios_to_run.append(scenario_TestEtu)
    
    for scenario in SCENARIOS :
        if scenario.run.__name__ in scenarios_name:
            scenarios_to_run.append(scenario)

    #Jouer les scénarios à jouer
    database_address = os.path.join(project_folder, "database_test.db")
    modalities_address = os.path.join(project_folder, "modalites.txt")
    if (modalites):
        modalities_address = os.path.join(student_project_folder, "modalites.txt")
        os.chdir(student_project_folder)
        gitchekout = "git checkout main"
        sp.run(gitchekout, shell = True) 
        os.chdir("../../../")
    results = utility.run_scenarios(modalites, scenarios_to_run, database_address, modalities_address, student_name, project_env, SCENARIOS)
    os.chdir(project_folder)

    gitAddCommit = "git add database_test.db && git commit -m \" update automatique de la base de données\""
    sp.run(gitAddCommit, shell = True)

    depot_repo = "https://" + paths["username"] + ":" + paths["password"] + "@" + paths["repository_path"].split("https://")[1] + ".git"
    gitpush = "git push " + depot_repo 
    sp.run(gitpush, shell = True)
    os.chdir("../../../")

    if (modalites):
        os.chdir(student_project_folder)
                        
        gitAddCommit = "git add modalites.txt && git commit -m \" Retour automatique des modalites\""
        sp.run(gitAddCommit, shell = True)

        gitpush = "git push " + depot + " main" 
        sp.run(gitpush, shell = True)
        os.chdir("../../../")

    #Afficher les résultats où il faut
    results.append(utility.report(scenarios_to_run, results, database_address, student_name))

    utility.print_results(results, student_project_folder, dest_address , retour + '.txt', depot, 2, commit)

def testsEtu(project_env):
    results = [Section("Evaluation TestsEtu ", _title_Lvl = 1)]
    run = TestsEtu.run(project_env.student_project_folder, [])
    results.append(run)
    return results