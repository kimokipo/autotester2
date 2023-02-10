from Scenario import Scenario
from scenarios.tools.CheckStyle import CheckStyle
from scenarios.tools.SimJava import SimJava
from scenarios.tools.JavaCompiler import JavaCompiler
from scenarios.tools.Blackbox import Blackbox
from scenarios.tools.Utilisation import Utilisation
from scenarios.results.Penalty import Penalty
from scenarios.tools.Junit import Junit
from tools import *
from Section import Section
import datetime


# ---------------------------------------------
# Outils disponibles
# ---------------------------------------------

javaCompiler = JavaCompiler() 
blackBox = Blackbox()
simjava = SimJava()
checkstylejava = CheckStyle()
utilisation = Utilisation()
junit = Junit()


# ------------------------------------------------------
# Fichiers à passer dans sim
# ------------------------------------------------------

sim_files = [("allumettes/StrategieNaive.java", "allumettes/StrategieExperte.java"),
            ("allumettes/StrategieExperte.java", "allumettes/StrategieHumaine.java"),
            ("allumettes/StrategieHumaine.java", "allumettes/StrategieRapide.java"),
            ("allumettes/Arbitre.java", "allumettes/Arbitre.java")]


# ------------------------------------------------------
# Fichiers a passé dans le checkstyle
# ------------------------------------------------------

checkstyle_files = ["allumettes/StrategieNaive.java", "allumettes/StrategieExperte.java", 
                "allumettes/StrategieHumaine.java", "allumettes/StrategieRapide.java",
                "allumettes/Arbitre.java", "allumettes/JeuProxy.java", "allumettes/OperationInterditeException.java",
                "allumettes/Joueur.java", "allumettes/Partie.java", "allumettes/Jeu.java"]


# ------------------------------------------------------
# Fichiers a passé dans le checkstyle
# ------------------------------------------------------

utilisation_files = [('Scanner', "allumettes/StrategieHumaine.java", 1), ('split', "allumettes/Partie.java", 1),
                    ('Random', "allumettes/StrategieNaive.java", 1), ('Random', "allumettes/StrategieExperte.java", 1),
                    (' 3', "allumettes/Partie.java", 0)]


# ------------------------------------------------------
# Fichiers à compiler en Java
# ------------------------------------------------------

compile_files_java = ["allumettes/Jouer.java", "allumettes/Arbitre.java"]


# ------------------------------------------------------
# Test en boite noire à exécuter
# ------------------------------------------------------

testsBN = ["exempleConfiantTricheurSujet", "exemplePresqueSujet",
            "exempleRobustesse", "exempleTricheurSujet"]


# ---------------------------------------------
# Definition des scénarios 
# ---------------------------------------------

def setup(project_env):
    results = []
    results.append(Section("% Validation de : " + project_env.student_project_folder))
    results.append(Section("% Date de l'évaluation : " + str(datetime.datetime.today())))
    return results

def similitude(project_env):
    results = [Section("Test de similitude ", _title_Lvl = 1)]
    for sim_file in sim_files:
        run = simjava.run(project_env, sim_file[0], sim_file[1])
        run.penalty = 1 if (run.result == "ERROR") else 0
        results.append(run)
    return results

def assertions(project_env):
    results = [Section("Test avec assertion ", _title_Lvl = 2)]
    run = junit.run('test', classpath = '/mnt/c/Users/amineak/Documents/autotester', options = ['-ea'])
    run.title = "Test avec assert de test : " + run.result
    project_env.tests['assertion'] = run.result != "ERROR"
    results.append(run)
    return results

def sans_assertions(project_env):
    results = []
    if project_env.tests['assertion'] == False:
        results = [Section("Test sans assertion ", _title_Lvl = 2)]
        results.append(junit.run('test', classpath = '/mnt/c/Users/amineak/Documents/autotester'))
    return results

def checkstyle(project_env):
    results = [Section("Test checkstyle ", _title_Lvl = 1)]
    f = open(project_env.student_project_folder + '/checkstyle.log',"r+")
    f.truncate(0)
    for file in checkstyle_files:
        results.append(checkstylejava.run(project_env.student_project_folder + '/' + file,
                    project_env.student_project_folder + '/checkstyle.log', "config_java.xml"))
    return results

def utilisationword(project_env):
    results = [Section("Test de similitude ", _title_Lvl = 1)]
    for utilisation_file in utilisation_files:
        results.append(utilisation.run(utilisation_file[0], project_env.student_project_folder + '/' + utilisation_file[1], utilisation_file[2]))
    return results

def compilationjava(project_env):
    results = [Section("Compilation des fichiers en JAVA", _title_Lvl = 1),
                javaCompiler.run(project_env, compile_files_java)]
    return results

def blackbox(project_env):
    results = [Section("Test en boite noire ", _title_Lvl = 1)]
    for test in testsBN:
        results.append(blackBox.run(project_env, test))
    return results


# ---------------------------------------------
# Liste des scénarios
# ---------------------------------------------

SCENARIOS = [
    Scenario(setup),
    Scenario(similitude, _mark = 2),
    Scenario(checkstyle),
    Scenario(utilisationword),
    Scenario(compilationjava),
    Scenario(blackbox),
    Scenario(assertions),
    Scenario(sans_assertions)
]

SCENARIOS_TESTS = SCENARIOS + [
    Scenario(setup),
    Scenario(similitude),
    Scenario(checkstyle),
    Scenario(compilationjava),
    Scenario(blackbox)
]