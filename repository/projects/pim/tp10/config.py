from Scenario import Scenario
from scenarios.tools.CheckStyle import CheckStyle
from scenarios.tools.SimJava import SimJava
from scenarios.tools.JavaCompiler import JavaCompiler
from scenarios.tools.AdaCompiler import AdaCompiler
from scenarios.tools.Blackbox import Blackbox
from scenarios.tools.UnchangedFile import UnchangedFile
from scenarios.tools.ChangedFile import ChangedFile
from scenarios.tools.RunAda import RunAda
from scenarios.tools.Valkyrie import Valkyrie
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
unchangedfile = UnchangedFile()
changedfile = ChangedFile()
adacompiler = AdaCompiler()
runada = RunAda()
valkyrie = Valkyrie()


# ------------------------------------------------------
# Fichiers qui doivent ou ne doivent pas être modifiers
# ------------------------------------------------------

changed_files = ["lca.ads", "th.ads", "lca.adb", "th.adb"]
unchanged_files = ["sda_exceptions.ads", "test_lca.adb"]

# ------------------------------------------------------
# Fichiers a passé dans le checkstyle
# ------------------------------------------------------

checkstyle_files = ["HelloWorld.java"]

# ------------------------------------------------------
# Fichiers à compiler en Java
# ------------------------------------------------------

compile_files_java = ["HelloWorld.java"]

# ------------------------------------------------------
# Fichiers à compiler en Ada
# ------------------------------------------------------

compile_files_ada = ["alea.adb", "evaluer_alea_lca.adb", "lca.ads", "lca.adb", "th.adb"]

# ------------------------------------------------------
# Fichiers + scenario à exécuter en Ada
# ------------------------------------------------------

run_files_ada = [("evaluer_alea_lca.adb", '6 100'),
                ("evaluer_alea_lca.adb", '5 100'),
                ("evaluer_alea_lca.adb", '100000 10'),
                ("evaluer_alea_lca.adb", '2 2')]


# ------------------------------------------------------
# Fichiers à passer dans sim
# ------------------------------------------------------

sim_files = [("HelloWorld.java", "HelloWorld.java")]


# ------------------------------------------------------
# Test en boite noire à exécuter
# ------------------------------------------------------

testsBN = ["BadHelloWorld", "helloWorld"]


# ---------------------------------------------
# Definition des scénarios 
# ---------------------------------------------

def setup(project_env):
    results = []
    results.append(Section("% Validation de : " + project_env.student_project_folder))
    results.append(Section("% Run on : " + str(datetime.datetime.today())))
    return results

def modification(project_env):
    results = [Section("Modification des fichiers fournis", _title_Lvl = 1),
            Section("Fichiers qui NE devaient PAS être modifiés", _title_Lvl = 2)]
    for file in unchanged_files:
        results.append(unchangedfile.run("../pim/tps/__fournis/tp10/" + file, project_env.student_project_folder + "/" + file))
    results.append(Section("Fichiers qui DEVAIENT être modifiés", _title_Lvl = 2))
    for file in changed_files:
        results.append(changedfile.run("../pim/tps/__fournis/tp10/" + file, project_env.student_project_folder + "/" + file))
    return results

def compilationada(project_env):
    results = [Section("Compilation des fichiers en ADA", _title_Lvl = 1)]
    for file in compile_files_ada:
        run = adacompiler.run(project_env, file)
        run.penalty = 1 if (run.result == "ERROR") else 0
        results.append(run)
    return results

def adarun(project_env):
    results = [Section("Exécution des programmes ADA ", _title_Lvl = 1)]
    for file, arg in run_files_ada:
        run = runada.run(project_env, file, arguments = arg)
        run.penalty = 1 if (run.result == "ERROR") else 0
        results.append(run)
    return results

def adavalkyrie(project_env):
    results = [Section("Exécution des programmes ADA avec Valkyrie", _title_Lvl = 1)]
    for file, arg in run_files_ada:
        run = valkyrie.run(project_env, file, arguments = arg)
        run.penalty = 1 if (run.result == "ERROR") else 0
        results.append(run)
    return results


# ---------------------------------------------
# Liste des scénarios
# ---------------------------------------------

SCENARIOS = [
    Scenario(setup),
    Scenario(modification, _mark = 5),
    Scenario(compilationada, _mark = 5),
    Scenario(adarun, _mark = 5),
    Scenario(adavalkyrie, _mark = 5)
]