HCC on Windows
======================
- Clone `hcc-windows`
`git clone --recursive -b windows https://github.com/otauqir/hcc-windows.git `
- Copy the `clang` and `lld` folders to the `compiler/tools` folder
- Open the Developer Command Prompt for VS2015 (installed with Visual Studio 2015)
- Create a `build_compiler` folder in the `hcc` folder
- Run the CMake command to generate the Visual Studio project for LLVM+Clang
`cmake -DLLVM_TARGETS_TO_BUILD="X86;AMDGPU" -G "Visual Studio 14" ../compiler`
- In the `build_compiler` folder, open `LLVM.sln`
- Change the build type from `Debug` to `Release` in the Visual Studio toolbar
- In the `Solution Explorer`, build the `ALL_BUILD` solution
- Download and install `GnuWin32` from `http://getgnuwin32.sourceforge.net/`
- Download `binutils` from `https://sourceforge.net/projects/mingw/files/MinGW/Base/binutils/binutils-2.28/` into the `GnuWin32` folder. Download the `-bin.tar.xz` archive and extract it.
- Add the `GnuWin32` folder to the Windows environment variables path
- Copy the Python scripts to the `Release/bin` folder
- Copy the `rocdl` folder to the `Release/bin` folder


Use the following command to build mcwamp.cpp
```
clang++ ^
-D _USE_MATH_DEFINES ^
-D _CRT_SECURE_NO_WARNINGS ^
-I "C:/hcc/include" ^
-I "C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/include" ^
-I "C:/Program Files (x86)/Windows Kits/10/include/10.0.10240.0/ucrt" ^
-I "C:/Program Files (x86)/Windows Kits/NETFXSDK/4.6.1/include/um" ^
-I "C:/Program Files (x86)/Windows Kits/8.1/Include/um" ^
-I "C:/Program Files (x86)/Windows Kits/8.1/Include/shared" ^
-fms-compatibility-version=19.0.24215 ^
-fms-compatibility ^
-fms-extensions ^
-fdelayed-template-parsing ^
-fdeclspec ^
-std=c++amp ^
-ferror-limit=1000 ^
-O3 ^
-c ^
-w ^
-v ^
-o mcwamp.obj ^
mcwamp.cpp < nul ^
&& ^
ar qc mcwamp.lib  mcwamp.obj < nul ^
&& ^
ranlib mcwamp.lib
```


Use the following command to build saxpy.cpp
```
hcc ^
-D _USE_MATH_DEFINES ^
-D _CRT_SECURE_NO_WARNINGS ^
-I "C:/hcc/include" ^
-I "C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/include" ^
-I "C:/Program Files (x86)/Windows Kits/10/include/10.0.10240.0/ucrt" ^
-I "C:/Program Files (x86)/Windows Kits/NETFXSDK/4.6.1/include/um" ^
-I "C:/Program Files (x86)/Windows Kits/8.1/Include/um" ^
-I "C:/Program Files (x86)/Windows Kits/8.1/Include/shared" ^
-LC:/hcc/build/Release/lib ^
-lmcwamp ^
-fms-compatibility-version=19.0.24215 ^
-fms-compatibility ^
-fms-extensions ^
-fdelayed-template-parsing ^
-fdeclspec ^
-hc ^
-std=c++amp ^
-w ^
-v ^
-o saxpy.exe ^
saxpy.cpp 
```

