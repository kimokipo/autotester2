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
import setup

# Fichier stockant les paths utiles
from variables import *
import json
import csv


def evaluateAll(commit : bool, matiere : str, tp : str, students_info, retour : bool, *scenarios_name) -> None:

    students = [f.path for f in os.scandir(paths[matiere]["repository_path"]) if f.is_dir()]

    project_folder = os.path.join(paths[matiere]["config_path"], tp)
    database_address = os.path.join(project_folder, "database_test.db")

    students_name = []
    with open(students_info) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            students_name.append(row[3])
    students_name = students_name[1:]

    for student_name in students_name:
        evaluate.evaluate(commit, matiere, tp, student_name, retour, *scenarios_name)