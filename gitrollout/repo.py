# -*- coding: utf-8 -*-

import git
import os


class Config(object):
    def __init__(self, names, targetPath, eventCmd=None):
        self.names = names
        self.targetPath = targetPath
        self.eventCmd = eventCmd


class Repo(object):
    def __init__(self, remoteUrl, path):
        if os.path.isdir(path):
            # open repo
            self.repo = git.Repo(path)

            # update origin url
            self.repo.git.remote('set-url', 'origin', remoteUrl)
        else:
            # clone
            self.repo = git.Repo.clone_from(remoteUrl, path, mirror=True)

    def sync(self):
        # remember commit shas of branches and tags
        branchesBefore = {branch.name: branch.commit.hexsha
                          for branch in self.repo.branches}
        tagsBefore = {tag.name: tag.commit.hexsha for tag in self.repo.tags}

        # fetch all remotes
        self.repo.git.fetch('--all', '-f', '-p')

        branches = {branch.name: branch.commit.hexsha
                    for branch in self.repo.branches}
        tags = {tag.name: tag.commit.hexsha for tag in self.repo.tags}

        return branchesBefore, tagsBefore, branches, tags
