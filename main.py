from FileReader import Reader
from Interpreter import Processor, time
import os

def Main():
    os.system("cls")
    path = "console.txt"

    file = Reader(path)

    if file.has_content:
        program_start = time()

        program = Processor(file.lines)    

        program_end = time()
        elaps = f"{(program_end - program_start):.2f}"

        print(f"Program finished after {elaps} seconds.")  
    else:
        print("Program terminated early.")

    input("Press \"Enter\" to end: ")


Main()
