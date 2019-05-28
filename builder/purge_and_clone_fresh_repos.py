'''Utility module for purging local ESGF repos and cloning fresh copies from Github'''
#!usr/bin/env python
import os
import re
import shutil
from git import Repo
from git import RemoteProgress
import repo_info


class MyProgressPrinter(RemoteProgress):
    '''Helper class for printing streaming output when cloning from Github'''
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print self._cur_line
            print message


def purge_repos(repo_directory):
    '''Delete all local ESGF repos from the repo_directory that are listed in the repo_info file'''
    for repo in repo_info.REPO_LIST:
        try:
            shutil.rmtree(os.path.join(repo_directory, repo))
            print repo + " removed successfully."
        except OSError:
            print repo + " does not exist on this system."
            print(repo + " skipped.")


def clone_repos(repo_directory):
    '''Clone fresh ESGF repos that are listed in the repo_info file to the repo_directory'''
    for repo_name, repo_url in repo_info.ALL_REPO_URLS.items():
        repo_path = os.path.join(repo_directory, repo_name)
        print("Currently cloning repo: " + repo_name)
        Repo.clone_from(repo_url, repo_path,
                        progress=MyProgressPrinter())
        print(repo_name + " successfully cloned -> {repo_path}".format(repo_path=repo_path))


def main(repo_directory=None):
    # Search for and remove appropriate repos
    if not repo_directory:
        default_repo_directory = os.path.join(os.environ["HOME"], "Development")
        repo_directory = raw_input("Enter the directory where the repos will be placed [{default_repo_directory}]: ".format(
            default_repo_directory=default_repo_directory)) or default_repo_directory

    purge_repos(repo_directory)
    clone_repos(repo_directory)


if __name__ == '__main__':
    main()
