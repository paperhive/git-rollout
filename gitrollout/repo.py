# -*- coding: utf-8 -*-

import git
import os
import re
import shutil


class Config(object):
    def __init__(self, targetPath, filters=None, eventCmd=None):
        self.targetPath = targetPath
        if filters is None:
            filters = [r'.*']
        self.filters = [re.compile(filter) for filter in filters]
        self.eventCmd = eventCmd

    def is_valid_name(self, name):
        # apply all filters and check for some nasty characters in a filename
        if not any([filter.match(name) for filter in self.filters]) or \
                re.match(r'^\.|.*[/$\0\n\t]', name):
            return False
        return True


class Repo(git.Repo):
    '''Extends git.Repo by a sync method that tracks changes when fetching.'''

    def __init__(self, *args, **kwargs):
        git.Repo.__init__(self, *args, **kwargs)

    @staticmethod
    def get_diff(before, after):
        '''Compute a diff of branches/tags.'''
        beforeSet = set(before.keys())
        afterSet = set(after.keys())

        removed = beforeSet.difference(afterSet)
        created = afterSet.difference(beforeSet)
        modified = {name for name in beforeSet.intersection(afterSet)
                    if before[name] != after[name]}
        unmodified = beforeSet.intersection(afterSet).difference(modified)
        return {
            'removed': list(removed),
            'created': list(created),
            'modified': list(modified),
            'unmodified': list(unmodified)
            }

    def sync(self):
        '''Calls fetch() and returns a diff of branches and tags'''
        # remember commit shas of branches and tags
        branchesBefore = {branch.name: branch.commit.hexsha
                          for branch in self.branches}
        tagsBefore = {tag.name: tag.commit.hexsha for tag in self.tags}

        # fetch all remotes
        self.git.fetch('--all', '-f', '-p')

        # get commit shas after update
        branchesAfter = {branch.name: branch.commit.hexsha
                         for branch in self.branches}
        tagsAfter = {tag.name: tag.commit.hexsha for tag in self.tags}

        # compute diffs
        branchesDiff = self.get_diff(branchesBefore, branchesAfter)
        tagsDiff = self.get_diff(tagsBefore, tagsAfter)

        return branchesDiff, tagsDiff


class RolloutHub(object):
    def __init__(self, path, remoteUrl=None,
                 branchConfig=None, tagsConfig=None):
        self.branchConfig = branchConfig
        self.tagsConfig = tagsConfig
        if os.path.isdir(path):
            # open repo
            self.repo = Repo(path)

            # update origin url
            if remoteUrl is not None:
                self.repo.git.remote('set-url', 'origin', remoteUrl)
        else:
            # clone
            self.repo = Repo.clone_from(remoteUrl, path, mirror=True)

            # TODO: apply 'virtual' diff where all branches + tags are created
