from ToolResult import *

class TestsEtuResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par l'outil runTestEtu'

        Paramètres du constructeur :
            _filenames : String - Noms des fichiers testé
            _details : String - Détails d'execution de l'outil
            _test_compil : Bool - Booléen correspondant à si oui ou non l'intégralité des tests ont fonctionné
    """
    
    def __init__(self,_filenames, _details, _test):
        title = "Exécution de " + ", ".join(_filenames)
        if _test:      
            result = OK
            title += ' : OK'
        else:
            result  = FAILURE
            title += ' : ERROR'
        ToolResult.__init__(self, title, result, _details)
