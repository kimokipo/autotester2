from Tool import Tool
from pylintResult import pylintResult
from typeAnnotations import *
from ProjectEnv import ProjectEnv
from isolate import *
import subprocess as sp
import os
import pathlib


class pylint():
    
    """
    Classe des tests de pylint.
    """

    def __init__(self):
        
        Tool.__init__(self,'')
        
    def run(self, file, result, config):

        cmd = 'pylint '+config +' '+file
        cp=sp.run(cmd.split(), stdout=sp.PIPE)

        buffer = open(result,'a')

        details = cp.stdout

        check_success = cp.stdout == 0
        
        list_erreurs = [ch for ch in str(details.decode("utf-8")).split('\n') if ch.startswith('[ERROR]')]

        test = len(list_erreurs) == 0

        if test == False:
            buffer.write(details.decode("utf-8"))
            buffer.close()

        return pylintResult(file, test, len(list_erreurs), details)
        

    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en python
        """

        return self.run([os.path.abspath("Helloworld.py")], [])
        pass
