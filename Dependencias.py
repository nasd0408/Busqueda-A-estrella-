"""
Este scrip es para instalar las dependencias necesarias para A_asterisco.py 
Para utilizar el archivo A_asterisco.py se recomienda usar Windows PowerShell

Script por:Nicolás Sira 
"""
import subprocess

def install_dependencies():
    dependencies = ["windows-curses", "heapq", "math", "networkx", "matplotlib"]
    for dependency in dependencies:
        subprocess.call(["pip", "install", dependency])

if __name__ == '__main__':
    install_dependencies()
