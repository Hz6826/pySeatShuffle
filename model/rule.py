"""
Rule Model
"""

class Rule:
    """
    available t(type):
    identical_in_group: provide 1 prop, if it is identical for ALL people in group, return True, elsewise return False
    unique_in_group: provide 1 prop, if everyone has different prop value, return True, elsewise return False
    """
    def __init__(self, t, prop: list, reversed=False):
        self.t = t
        self.prop = prop
        self.reversed = reversed

    def check(self, group):
        if self.t == 'identical_in_group':
            for i in range(len(group)):
                for j in range(i+1, len(group)):
                    if group[i][self.prop[0]] != group[j][self.prop[0]]:
                        return False
            return True
        elif self.t == 'unique_in_group':
            for i in range(len(group)):
                for j in range(i+1, len(group)):
                    if group[i][self.prop[0]] == group[j][self.prop[0]]:
                        return False
                    return True
                return False
            return True
        else:
            raise Exception('Invalid rule type')