#!/usr/bin/python
#clamp-assemble kernel-bitcode kernel-object

from sys import argv, exit
import os
from shutil import copyfile
from subprocess import check_call

if __name__ == "__main__":

    bindir = os.path.dirname(argv[0])
    if os.name == "nt":
        embed = bindir + "/clamp-embed.py"
        obj_ext = ".obj"
    else:
        embed = bindir + "/clamp-embed"
        obj_ext = ".o"

    if len(argv) != 3:
        print("Usage: %s kernel-bitcode object" % argv[0])
        exit(1)

    if not os.path.isfile(argv[1]):
        print("kernel-bitcode %s is not valid" % argv[1])
        exit(1)

    if os.path.isfile(argv[2]):
        copyfile(argv[2], argv[2] + ".host" + obj_ext)
        os.remove(argv[2])

        check_call(["python",
            embed,
            argv[1],
            argv[2] + ".kernel" + obj_ext])

        check_call(["ld",
            "-r",
            argv[2] + ".kernel" + obj_ext,
            argv[2] + ".host" + obj_ext,
            "-o",
            argv[2]])

        os.remove(argv[2] + ".kernel" + obj_ext)
        os.remove(argv[2] + ".host" + obj_ext)
    else:
        check_call(["python",
            embed,
            argv[1],
            argv[2]])

    exit(0)
