# Author: NS
# Move missing files.
#

import shutil
import os

A = set(os.listdir("testImages"))
B = set(os.listdir("captchas"))

l0 = len(os.listdir("captchas"))

for a in A.difference(B):
    shutil.move(f"testImages/{a}", "captchas")

print("Missing files: ", A.difference(B))
print("Files moved: ", len(os.listdir("captchas")) - l0)