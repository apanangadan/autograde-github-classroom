#!/usr/bin/env python
# -*- coding: utf8 -*-

# Acknowledgment: https://github.com/muhasturk/gitim

from getpass import getpass
from argparse import ArgumentParser
from os import path, makedirs, pardir, environ
from subprocess import call
from functools import partial
from platform import python_version_tuple

from github import Github
import time
import sys

if python_version_tuple()[0] == u'2':
    input = lambda prompt: raw_input(prompt.encode('utf8')).decode('utf8')

class MyRepo():
    def __init__(self, full_name, name, url):
        self.full_name = full_name
        self.name = name
        self.clone_url = url

class Gitim():

    def set_args(self):
        """ Create parser for command line arguments """
        parser = ArgumentParser(
                usage=u'python -m clone-projects.py -h\'\n\t\t\tUsername and password will be prompted.',
                description='Clone all repositories in input file')
        parser.add_argument('-u', '--user', help='Your github username')
        parser.add_argument('-p', '--password', help=u'Github password')
#        parser.add_argument('-t', '--token', help=u'Github OAuth token')
        parser.add_argument('-d', '--dest', help=u'Destination directory. Created if doesn\'t exist. [curr_dir]')
        parser.add_argument('-f', '--filename', default=u'repos_list.txt', help=u'List of repos to full. [repos_list.txt]')
        parser.add_argument('--nopull', action='store_true', help=u'Don\'t pull if repository exists. [false]')
        return parser

    def clone_main(self):
        """ Clone all repos """
        parser = self.set_args()
        args = parser.parse_args()

        join = path.join
        if args.dest:
            if not path.exists(args.dest):
                makedirs(args.dest)
                print(u'Creating folder "{}"'.format(args.dest))
            join = partial(path.join, args.dest)

        get_repos = []
        try:
            with open(args.filename, 'r') as fp:
                data = fp.readlines()
                for line in data:
                    words = line.split()
                    get_repos.append(MyRepo(words[0],words[1],words[2]))
        except IOError as e:
            print (u'Unable to open file "{}"'.format(args.filename))
            sys.exit(1)

        # password hack
        username = args.user
        password = args.password
        if not username:
            username = input(u'Username: ')
        if not password:
            password = getpass('Password: ')

        for repo in get_repos:
            time.sleep(0.5)
            if not path.exists(join(repo.name)):
                print(u'Cloning "{repo.full_name}"'.format(repo=repo))

                url = unicode(repo.clone_url)
                print (url)
                assert(url.startswith('https://'))
                url = url[len('https://'):]
                url = 'https://' + username + ':' + password + '@' + url

                call([u'git', u'clone', url, join(repo.name)]) # anand
            elif not args.nopull:
                print(u'Updating "{repo.name}"'.format(repo=repo))
                call([u'git', u'pull'], env=dict(environ, GIT_DIR=join(repo.name, '.git').encode('utf8'))) # anand
            else:
                print(u'Already cloned, skipping...\t"{repo.name}"'.format(repo=repo))
        print(u'FIN')


if __name__ == '__main__':
    gitim = Gitim()
    gitim.clone_main()
