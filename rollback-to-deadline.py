#! /usr/bin/env python3

#Acknowledgment: https://github.com/Sirusblk

import os, shutil, subprocess
from argparse import ArgumentParser

DATE_STRING = '2018-02-18 01:00 PST'
#DATE_STRING = '2018-04-30 01:00 PST'

def rollback_one_submission(subdirectory):
    print(subdirectory)
    os.chdir(subdirectory)
    # rollback any changes to DATE_STRING
    command = 'git checkout `git rev-list -n 1 --before=\"' + DATE_STRING + '\" master`'
    os.system(command)
    os.chdir('..')


def rollback_all():
    """ Create parser for command line arguments """
    parser = ArgumentParser(
            usage=u'python -m rollback-to-deadline -h',
            description=' rollback all submissions to last commit before assignment deadline')
    parser.add_argument('-d', '--dest', help=u'Destination directory containing submissions [curr_dir]')
    parser.add_argument('--deadline', default=DATE_STRING, help=u'Assignment deadline in git date format [' + DATE_STRING +']')
    args = parser.parse_args()

    if args.dest:
        os.chdir(args.dest)
    for entry in sorted(os.scandir('.'),
                        key = lambda e: e.name):
        name = entry.name
        if entry.is_dir():
            rollback_one_submission(name)

if __name__ == '__main__':
    rollback_all()
