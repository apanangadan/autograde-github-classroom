#! /usr/bin/env python3.5

# Acknowledgment:
# https://github.com/kevinwortman/rubrictest
# https://github.com/kevinwortman/nerfherder

import os, os.path, shutil, subprocess, filecmp

BASE_DIR = '/home/me/Desktop/gitim/autograde/'
UNIQUE_PROJECT_FILE = 'Registrar.h' # any student file unique to this assignment to check if the repo is really for this project
RETAINED_SKELETON_FILES = ['critic.py', 'main.cpp', 'gradeslist.txt', 'gradeslistbig.txt'] # overwrite some repo files with test files
SKELETON_DIR = BASE_DIR + 'testfiles/' # directory containing RETAINED_SKELETON_FILES
OUTPUT_PATH = BASE_DIR + 'results.txt' # name of output file
CODE_DIR = BASE_DIR + 'code-to-grade' # directory containing student repos
EMPTY_DIR = BASE_DIR + 'empty-repos' # directory where empty repos should be moved
GRADED_DIR = BASE_DIR + 'graded' # directoty to where graded repos should be moved

INDENT = ' ' * 4
HORIZONTAL_RULE = ('#' * 79) + '\n'

def copy_from_skeleton(filename, destination_directory):
    print(INDENT + 'overwriting "' + filename + '"...')
    shutil.copyfile(os.path.join(SKELETON_DIR + filename),
                    os.path.join(destination_directory, filename))

def write_result_string(string_obj):
    with open(OUTPUT_PATH, 'a') as f:
        f.write(string_obj)

def write_result_bytes(bytes_obj):
    write_result_string(bytes_obj.decode('utf-8', 'ignore'))

def write_result_and_print(string_obj):
    write_result_string(string_obj)
    print(string_obj, end='')

def grade_one_submission(subdirectory):
    print('preparing:')
    for filename in RETAINED_SKELETON_FILES:
        copy_from_skeleton(filename, subdirectory)

    print('determining group members...')
    write_result_string('names:\n')
    try:
        with open(os.path.join(subdirectory, 'README.md')) as f:
            for line in f.readlines():
                if '@' in line:
                    write_result_string(INDENT + line.strip() + '\n')
    except FileNotFoundError:
        write_result_string('No README.md!')
    #return
    os.chdir(subdirectory)
    print('running...')
    # ensure that critic is executable
    subprocess.run(['chmod', '755', 'critic.py'])
    # run critic
    process = subprocess.Popen(['./critic.py', 'test'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    write_result_string('stdout:\n')
    stdout_iterator = iter(process.stdout.readline, b"")
    for line in stdout_iterator:
        print(line)
        #if '@gradingtest' in line.decode('utf-8', 'ignore'):
        #   write_result_bytes(line)
        write_result_bytes(line)
    write_result_string('\nstderr:\n')
    stderr_iterator = iter(process.stderr.readline, b"")
    for line in stderr_iterator:
        print(line)
        write_result_bytes(line)
    write_result_string('\n\n')
    os.chdir('..')
    print ('moving ', subdirectory, ' to ', GRADED_DIR)
    if not os.path.exists(GRADED_DIR):
        os.makedirs(GRADED_DIR)
    shutil.move(subdirectory, GRADED_DIR)

def grade_all():
    try:
        #os.remove(OUTPUT_PATH)
        print ('APPENDING to ', OUTPUT_PATH);
    except:
        pass

    os.chdir(CODE_DIR)
    for entry in sorted(os.scandir('.'),
                        key = lambda e: e.name):
        name = entry.name
        nocommits = True # if this folder has not been touched by a student, don't critic it and move it to Empty folder
        if entry.is_dir():
            if (os.path.isfile(os.path.join(name, 'README.md')) and
                os.path.isfile(os.path.join(name, UNIQUE_PROJECT_FILE))):
                if not filecmp.cmp(os.path.join(SKELETON_DIR, 'README.md'), os.path.join(name, 'README.md')):
                    nocommits = False
                    write_result_and_print(HORIZONTAL_RULE)
                    write_result_and_print(name + '\n')
                    grade_one_submission(name)
                else:
                    print (name, ' README.md unchanged\n')
            else:
                print (name, ' README.md not found\n')
        else:
            print(name, 'is not a folder\n\n')

        if nocommits:
            if not os.path.exists(EMPTY_DIR):
                os.makedirs(EMPTY_DIR)
            print ('moving ', name, ' to ', EMPTY_DIR)
            shutil.move(name, EMPTY_DIR)


if __name__ == '__main__':
    grade_all()
