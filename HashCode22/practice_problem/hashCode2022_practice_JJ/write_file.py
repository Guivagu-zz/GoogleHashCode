import os
import shutil


filepath = 'out.txt'

def write_file(tastes):
    with open(filepath, 'w') as f:
        f.write(str(len(tastes)) + " ")
        f.write(' '.join(tastes))
        f.write('\n')