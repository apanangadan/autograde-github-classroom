# Python scripts and folders to download and grade submissions to Github Classroom assignments

## Example C++ programming assignment
An example assignment description for students (with link to create repos) is [here](https://docs.google.com/document/d/1mszTJFAmO-uTtE0nFBGjUvFE7y1e6-GjyAkK7cjN5n0/edit?usp=sharing).

Starter code for students, including a .travis.yml to provide automatic feedback is [here](https://github.com/CSUF-CPSC-131-Spring2018/project0skeleton).

## Steps to download and grade submissions
1. Create the list of repository URLs to clone (specify organization name here) into repos_list.txt

`get_urls_from github.py -u mygithubusername -p mygithubpassword --org githuborganization > repos_list.txt`

2. Edit repos_list.txt to remove any projects that should not be downloaded. (We have multiple assignments in one Organization, so we remove all but the ones to be graded)

3. Clone all repos in repos_list.txt into a folder

`clone_projects.py -u mygithubusername -p mygithubpassword -d code-to-grade -f repos_list.txt`

4. Enforce assignment deadline: rollback each repo/submission to the assignment deadline

`./rollback-to-deadline.py -d code-to-grade --deadline "2018-02-18 01:00 PST"`

5. Prepare test code (main.cpp with unit tests and related input data files). Commands to build and run code go in critic.py.
Specify location of these files in grade-assignments.py. Main task here is to separate repositories that have no changes made by the student. These are moved to empty_repos. Graded repos are moved to a folder called graded. Build and execute tests are written to a text file.

`./grade-assignments.py`

Example test code for the above assignment is included in the testfiles folder

## TO-DO:
Currently, grade-assignments.py will get stuck if one of the student repos goes into an infinite loop. This requires killing grade-assignments.py, moving the problem repo, and restarting grade-assignments.py. This should be automated in an improved version

## Acknowledgment
* Code to download from github is based on https://github.com/muhasturk/gitim
* Auto-grading code is based on:

https://github.com/kevinwortman/rubrictest

https://github.com/kevinwortman/nerfherder

https://github.com/kevinwortman/
* https://github.com/Sirusblk
