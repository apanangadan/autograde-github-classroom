#! /usr/bin/env python3
# -*-Python-*-

import os, subprocess, sys
from pexpect import run # $ pip install pexpect

COMPILER = 'clang++'

# return True on success or False on failure
def command(arg_list):
    print()
    print('-'*len(' '.join(arg_list)))
    print(' '.join(arg_list))
    print('-'*len(' '.join(arg_list)))
    #return ' '.join(arg_list) + '\n' + subprocess.check_output(arg_list, stderr=subprocess.STDOUT)
    proc = subprocess.run(arg_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if (len(proc.stdout) > 0):
        print(proc.stdout.decode('ascii'))
    if (len(proc.stderr) > 0):
        print(proc.stderr.decode('ascii'))
    #print(subprocess.check_outpu(arg_list, stderr=subprocess.STDOUT))
    #return_code = subprocess.call(arg_list)
    #return (return_code == 0)


# return True on success or False on failure
def compile(source_path_list, library_name_list, output_path):
    return command([COMPILER] +
                   ['-g', '-std=c++11'] +
                   source_path_list +
                   ['-l' + lib for lib in library_name_list] +
                   ['-o'] + output_path)

def build():
    command(['cat', 'Student.h']) # to include student's source code in the results file
    command(['cat', 'Registrar.h']) # to include student's source code in the results file
    compile(['main.cpp', 'Registrar.cpp', 'Student.cpp'],
                    [],
                    ['testexe'])

def test():
    build()
    if os.path.exists('./testexe'):
        command(['./testexe'])
    else:
        print('Executable file not found')

def printUsageAndExit():
    print ('critic.py [test|build]')
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        printUsageAndExit()
    command = sys.argv[1]
    if command == 'build':
        build()
    elif command == 'test':
        test()
    else:
        printUsageAndExit()

if __name__ == '__main__':
    main()
