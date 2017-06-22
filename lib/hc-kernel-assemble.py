#!/usr/bin/python

#hc-kernel-assemble kernel-bitcode kernel-object

import os
from sys import argv, exit
from tempfile import mkdtemp
from subprocess import Popen, check_call
from shutil import rmtree, copyfile

if __name__ == "__main__":
    bindir = os.path.dirname(argv[0])
    clang = bindir + "/clang"
    llvm_link = bindir + "/llvm-link"
    opt = bindir + "/opt"
    llvm_as = bindir + "/llvm-as"
    llvm_dis = bindir + "/llvm-dis"
    libpath = bindir + "/../lib"
    if os.name == "nt":
        clamp_asm = bindir + "/clamp-assemble.py"
        obj_ext = ".obj"
    else:
        clamp_asm = bindir + "/clamp-assemble"
        obj_ext = ".o"

    if len(argv) != 3:
        print("Usage: %s kernel-bitcode kernel-object" % argv[0])
        exit(1)

    kernel_input = argv[1]
    command = [clang, "-std=c++amp", "-I" + bindir + "/../../include", "-fPIC", "-O3", "-c", "-o"]

    if not os.path.isfile(kernel_input):
        print("kernel-bitcode %s is not valid" % kernel_input)
        exit(1)

    temp_dir = mkdtemp()
    basename = os.path.basename(argv[2])
    temp_name = temp_dir + '/' + basename

    if os.path.isfile(argv[2]):
        copyfile(argv[2], temp_name + ".tmp" + obj_ext)
        os.remove(argv[2])

    check_call([llvm_dis,
        kernel_input,
        "-o",
        temp_name + ".ll"])

    f0 = open(temp_name + ".ll", "rb")
    if os.name == "nt":
        f1 = open("nul", "wb")
        ext = ".dll"
    else:
        f1 = open("/dev/null", "wb")
        ext = ".so"
    f2 = open(temp_name + ".kernel_redirect.ll", "wb")
    if os.name == "nt":
            p = Popen([opt,
            "-redirect"],
            stdin = f0,
            stdout = f1,
            stderr = f2)
    else:
        p = Popen([opt,
            "-load",
            libpath + "/LLVMDirectFuncCall" + ext,
            "-redirect"],
            stdin = f0,
            stdout = f1,
            stderr = f2)
    p.wait()
    f0.close()
    f1.close()
    f2.close()

    if os.path.isfile(temp_name + ".kernel_redirect.ll") and (os.stat(temp_name + ".kernel_redirect.ll").st_size != 0):
        f0 = open(temp_name + ".ll", "rb")
        f2 = open(temp_name + ".camp.cpp", "wb")
        if os.name == "nt":
            f1 = open("nul", "ab")
            p = Popen([opt,
                "-gensrc"],
                stdin = f0,
                stdout = f1,
                stderr = f2)
        else:
            f1 = open("/dev/null", "ab")
            p = Popen([opt,
                "-load",
                libpath + "/LLVMWrapperGen.so",
                "-gensrc"],
                stdin = f0,
                stdout = f1,
                stderr = f2)
        p.wait()
        f0.close()
        f1.close()
        f2.close()

        check_call([llvm_as,
            temp_name + ".kernel_redirect.ll",
            "-o",
            temp_name + ".kernel_redirect.bc"])
        check_call(command + [temp_name + ".camp.s", "-emit-llvm"])
        check_call(command + [temp_name + ".camp" + obj_ext])
        check_call(["objcopy",
            "-R",
            ".kernel",
            temp_name + ".camp" + obj_ext])
        check_call([llvm_link,
            temp_name + ".kernel_redirect.bc",
            temp_name + ".camp.s",
            "-o",
            temp_name + ".link.bc"])
        check_call(["python",
            clamp_asm,
            kernel_input + ".bc",
            temp_name + ".camp" + obj_ext])
    else:
        os.link(kernel_input, kernel_input + ".bc")
        check_call(["python",
            clamp_asm,
            kernel_input + ".bc",
            temp_name + ".camp" + obj_ext])
    if os.path.isfile(temp_dir + '/' + basename + ".tmp" + obj_ext):
        if os.name == "nt":
            if os.path.isfile(os.path.splitext(argv[2])[0] + ".rar"):
                os.remove(os.path.splitext(argv[2])[0] + ".rar")
            copyfile(temp_name + ".camp" + obj_ext, os.path.splitext(argv[2])[0] + ".kernel.bc")
            copyfile(temp_dir + '/' + basename + ".tmp" + obj_ext, os.path.splitext(argv[2])[0] + ".host.obj")
            check_call(["rar",
                "a",
                "-df",
                "-ep",
                os.path.splitext(argv[2])[0] + ".rar",
                os.path.splitext(argv[2])[0] + ".host.obj",
                os.path.splitext(argv[2])[0] + ".kernel.bc"])
        else:
            check_call(["ld",
                "-r",
                "--allow-multiple-definition",
                temp_dir + '/' + basename + ".tmp" + obj_ext,
                temp_name + ".camp" + obj_ext,
                "-o",
                argv[2]])
    else:
        copyfile(temp_name + ".camp" + obj_ext, argv[2])
        os.remove(temp_name + ".camp" + obj_ext)

    rmtree(temp_dir)
    exit(0)

