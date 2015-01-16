# -*- coding: utf-8 -*-

# print(..., file=...) in python 2
from __future__ import print_function

import git


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
        added = afterSet.difference(beforeSet)
        modified = {name for name in beforeSet.intersection(afterSet)
                    if before[name] != after[name]}
        unmodified = beforeSet.intersection(afterSet).difference(modified)
        return {
            'removed': list(removed),
            'added': list(added),
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
