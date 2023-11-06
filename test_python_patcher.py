# File: test_code_patcher.py - This file tests the functionality of code_patcher.py.

import unittest
from python_patcher import python_patcher
from redbaron import RedBaron

class test_python_patcher(unittest.TestCase):

    def setUp(self):
        self.file = "testcases.py"
        self.sample_code = """
import sys

def greet(name):
    print(f"Hello, {name}!")

class Person:
    def __init__(self, name):
        self.name = name
"""

    def test_text_command_function(self):
        patcher = python_patcher(self.file, self.sample_code)
        patcher.delete_function("greet")
        print("After delete_function:\n", patcher.get_patched_code())  # Debug print
        self.assertNotIn("print('Hello')", patcher.get_patched_code().strip())

    def test_find_imports(self):
        patcher = python_patcher(self.file, self.sample_code)
        imports = patcher.find_imports()
        self.assertIn("import sys", imports)

    def test_add_import(self):
        patcher = python_patcher(self.file, self.sample_code)
        patcher.add_import("import os")
        print("After add_import:\n", patcher.get_patched_code())  # Debug print
        self.assertIn("import os", patcher.get_patched_code())

    def test_delete_import(self):
        patcher = python_patcher(self.file, self.sample_code)
        patcher.delete_import("import sys")
        print("After delete_import:\n", patcher.get_patched_code())  # Debug print
        self.assertNotIn("import sys", patcher.get_patched_code())

    def test_find_functions(self):
        patcher = python_patcher(self.file, self.sample_code)
        functions = patcher.find_functions()
        self.assertIn("greet", functions)

    def test_add_function(self):
        new_function = """
def say_bye(name):
    print(f"Goodbye, {name}!")
"""
        patcher = python_patcher(self.file, self.sample_code)
        patcher.add_function(new_function)
        print("After add_function:\n", patcher.get_patched_code())  # Debug print
        self.assertIn("def say_bye(name):", patcher.get_patched_code())

    def test_delete_function(self):
        patcher = python_patcher(self.file, self.sample_code)
        patcher.delete_function("greet")
        print("After delete_function:\n", patcher.get_patched_code())  # Debug print
        self.assertNotIn("def greet(name):", patcher.get_patched_code())

    # You can continue to add more test cases for classes, main body, etc.
    def test_set_main_function(self):
        patcher = python_patcher(self.file, self.sample_code)
        patcher.set_main_body("print('Hello World')\n")
        print("After set_main_body:\n", patcher.get_patched_code())  # Debug print
        code = patcher.get_patched_code()
        self.assertIn("print('Hello World')", patcher.get_patched_code())

    def test_process_chatgpt_response(self):
        patcher = python_patcher(self.file, "") 
        response = """
Sure! Here's the code using PP commands:
Here are the step-by-step PP commands to draw a 3D surface plot of z = sin(x) + cos(y):

```
addimport from mpl_toolkits.mplot3d import Axes3D
addimport import numpy as np
addimport import matplotlib.pyplot as plt

addfunc def plot_surface():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) + np.cos(Y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z)

    plt.show()
###
setmain
if __name__ == "__main__":
    plot_surface()
###
```
"""
        code_lines = patcher.process_chatgpt_response(response)
        want_code = """addimport from mpl_toolkits.mplot3d import Axes3D
addimport import numpy as np
addimport import matplotlib.pyplot as plt

addfunc
def plot_surface():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) + np.cos(Y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z)

    plt.show()
###
setmain
if __name__ == "__main__":
    plot_surface()
###
"""
        want_code_lines= want_code.split('\n')
        self.assertEqual(code_lines, want_code_lines)       

if __name__ == '__main__':
    print("Start...")
    unittest.main()
