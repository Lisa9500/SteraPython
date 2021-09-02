import glob
import re
import os

file = glob.glob('test/*.txt')
print(file)

# f = glob.glob('test/*.text')
# print(os.path.split(f)[1])

file = print(glob.glob('test/**/*.txt', recursive=True))
print(file)
