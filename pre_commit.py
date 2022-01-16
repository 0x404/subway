import os

os.system("black core/ subway.py")
os.system("pylint core/ subway.py")
os.system("python3 -m pytest")