import os

os.system("black core/ scripts/ subway.py")
os.system("pylint core/ scripts/ subway.py")
os.system("python3 -m pytest")