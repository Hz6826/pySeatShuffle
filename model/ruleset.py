"""
Ruleset Model
"""

from .rule import *

class Ruleset:
    def __init__(self, rules: list[Rule], relations=None):  # TODO: relations
        self.rules = rules
        self.relations = relations

    def check(self, group):
        for rule in self.rules:
            if not rule.check(group):
                return False
        return True

