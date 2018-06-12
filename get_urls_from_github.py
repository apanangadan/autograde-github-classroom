#!/usr/bin/env python
# -*- coding: utf8 -*-

# output a list of repository names separated by space:
# full_name name clone_url
# this list can be used later to clone code

# code based on https://github.com/muhasturk/gitim

from getpass import getpass
from argparse import ArgumentParser
from platform import python_version_tuple

from github import Github
import time

if python_version_tuple()[0] == u'2':
    input = lambda prompt: raw_input(prompt.encode('utf8')).decode('utf8')

class Gitim():
    def set_args(self):
        """ Create parser for command line arguments """
        parser = ArgumentParser(
                usage=u'python -m gitim -u\'\n\t\t\tUsername and password will be prompted.',
                description=' output a list of repository names and URLs to be later used for cloning')
        parser.add_argument('-u', '--user', help='Your github username')
        parser.add_argument('-p', '--password', help=u'Github password')
        parser.add_argument('-t', '--token', help=u'Github OAuth token')
        parser.add_argument('--org', default=u'CSUF-CPSC-131-Spring2018', help=u'Organisation name [CSUF-CPSC-131-Spring2018]')
        return parser

    def make_github_agent(self, args):
        """ Create github agent to auth """
        if args.token:
            g = Github(args.token)
        else:
            user = args.user
            password = args.password
            if not user:
                user = input(u'Username: ')
            if not password:
                password = getpass('Password: ')
            g = Github(user, password)
        return g

    def clone_main(self):
        """ Clone all repos """
        parser = self.set_args()
        args = parser.parse_args()
        g = self.make_github_agent(args)
        user = g.get_user().login

        get_repos = g.get_organization(args.org).get_repos if args.org else g.get_user().get_repos
        for repo in get_repos():
            time.sleep(0.1)
            print(u'{repo.full_name} {repo.name} {repo.clone_url}'.format(repo=repo))
        print(u'FIN')


if __name__ == '__main__':
    gitim = Gitim()
    gitim.clone_main()
