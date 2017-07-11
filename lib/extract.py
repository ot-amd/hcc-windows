import os
from subprocess import check_call
from sys import argv, exit
from shutil import copyfile

if __name__ == "__main__":
    cur_dir = os.getcwd()
    bin_dir = "C:/ROC/hcc/hcc/lib/pal"
    os.chdir(bin_dir)

    for f in os.listdir("."):
        if f.endswith(".rar"):
            if os.path.isfile(os.path.splitext(f)[0] + ".kernel.bc"):
                os.remove(os.path.splitext(f)[0] + ".kernel.bc")
            if os.path.isfile(os.path.splitext(f)[0] + ".host.obj"):
                os.remove(os.path.splitext(f)[0] + ".host.obj")
            check_call(["unrar",
                "e",
                "-inul",
                f])
    
    for f in os.listdir("."):
        if f.endswith(".kernel.bc"):
            os.remove(f)
        elif f.endswith(".host.obj"):
            copyfile(f, cur_dir + "/" + f[:-9] + ".obj")
            os.remove(f)
        elif f.endswith(".rar"):
            os.remove(f)
    
    exit(0)

