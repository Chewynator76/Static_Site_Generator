import os
import shutil

def copydir_to_targetdir(source, target):
    target_path = os.path.abspath(target)
    source_path = os.path.abspath(source)
    target_contents = os.listdir(target_path)
    source_contents = os.listdir(source_path)

    if os.path.exists(source_path) == False:
        return
    if os.path.exists(target_path) == False:
        os.mkdir(target_path)

    for path in target_contents:
        temp = os.path.join(target_path, path)
        if os.path.isfile(temp):
            os.remove(temp)
        else:
            shutil.rmtree(temp)
    
    for path in source_contents:
        temp = os.path.join(source_path, path)
        if os.path.isfile(temp):
            shutil.copy(temp, target)
            continue
        temp2 = os.path.join(target_path, path)
        os.mkdir(temp2)
        copydir_to_targetdir(temp, temp2)