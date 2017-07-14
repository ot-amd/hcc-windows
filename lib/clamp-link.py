#!/usr/bin/python

import os
from sys import argv, exit
from tempfile import mkdtemp
from shutil import rmtree, copyfile
from subprocess import Popen, check_call, check_output, PIPE, call

if __name__ == "__main__":

    bindir = os.path.dirname(argv[0])
    libpath = bindir + "/../lib"
    link = bindir + "/llvm-link"
    opt = bindir + "/opt"
    clang_offload_bundler = bindir + "/clang-offload-bundler"
    if os.name == "nt":
        clamp_device = bindir + "/clamp-device.py"
        clamp_embed = bindir + "/clamp-embed.py"
        obj_ext = ".obj"
        sl_ext = ".lib"
        libpath_flag = "-libpath:"
    else:
        clamp_device = bindir + "/clamp-device"
        clamp_embed = bindir + "/clamp-embed"
        obj_ext = ".o"
        sl_ext = ".a"
        libpath_flag = "-L"

    verbose = 0
    amdgpu_target_array = []
    link_host_args = []
    link_other_args = []

    args = argv[1:]
    static_lib_list = []
    temp_ar_dirs = []

    if not os.path.isfile(libpath + "/mcwamp.rar"):
        print("Can't find mcwamp.rar")
        exit(1)

    check_call(["unrar",
                "e",
                "-inul",
                libpath + "/mcwamp.rar"])

    link_host_args.append("mcwamp.host.obj")

    if "--verbose" in args:
        verbose = 2
        args.remove("--verbose")
    
    for arg in args:
        if arg.startswith("--amdgpu-target="):
            amdgpu_target_array.append(arg[16:])

        elif arg.endswith(obj_ext):
            if os.path.isfile(arg):
                link_host_args.append(arg)
        else:
            link_other_args.append(arg)

    if len(amdgpu_target_array) == 0:
        amdgpu_target_array.append("gfx803")

    if verbose != 0:
        print("AMDGPU target array: ", amdgpu_target_array)
        print("new host args: ", link_host_args)
        print("new other args: ", link_other_args)

    if os.name == "nt":
        command = ["link",
            "-verbose:lib",
            "-debug",
            "-force:multiple",
            "-ignore:4006",
            "-ignore:4078",
            "-ignore:4088",
            "-subsystem:console",
            "-nodefaultlib:libcmt",
            "-stack:10000000",
            "-heap:1000000000",
            "-debug",
            "ucrtd.lib",
            "vcruntimed.lib",
            "msvcrtd.lib",
            "msvcprtd.lib",
            "kernel_bundle_data.obj"]
    else:
        command = ["ld",
            "--allow-multiple-definition"]

    command += link_other_args
    command += link_host_args
    print(command)
    call(command)

    os.remove("kernel_bundle_data.obj")
    os.remove("mcwamp.host.obj")
    os.remove("mcwamp.kernel.bc")

    exit(0)

