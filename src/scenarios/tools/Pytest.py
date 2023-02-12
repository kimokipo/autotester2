import subprocess
import os

# PytestResult class 
class PytestResult:
    # Initialisation
    def __init__(self, test_file, return_code, stdout, stderr):
        self.test_file = test_file
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
    
    # On verifie que le Pytest run ait marché
    def success(self):
        return self.return_code == 0
    
    # Return a string representation of the PytestResult object
    def __str__(self):
        return f"Test file: {self.test_file}\nReturn code: {self.return_code}\nStandard Output:\n{self.stdout}\nStandard Error:\n{self.stderr}"

# Pytest class utilisé pour run les Pytest
class Pytest:
    # Initialisation
    def __init__(self):
        self.results = [] # liste qui va stocker les Pytest runs
        
    # Run les Pytests tests
    def run(self, test_file, options=[]):
        # The command to run the Pytest tests
        command = ['pytest', test_file] + options
        
        # Run the Pytest tests and capture its output
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Store the result of the Pytest run in the results list
        self.results.append(PytestResult(test_file, result.returncode, result.stdout, result.stderr))
        return self.results[-1]
        
    # Run a quick self check test of Pytest
    def selfcheck(self):
        test_file = 'test_hello_world.py' # The test file name
        
        # Write a simple test to the test file
        with open(test_file, 'w') as f:
            f.write("def test_hello_world():\n    assert True")
        
        # Run the test file with Pytest
        result = self.run(test_file)
        
        # Remove the test file
        os.remove(test_file)
        return result
    
    
