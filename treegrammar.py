import re
from tree import Tree


class TreeGrammar:
    def __init__(self, start=None, rules=None, terminals=None):
        """
        Contruct grammar from list of tuples of form (parent, children).
        """
        self.start = None
        self.rules = []
        if rules:
            for rule in rules:
                parent, children = rule
                rules.append((parent, tuple(children)))
        if terminals:
            self.add_terminals(terminals)
        self.any_terminal = False

    def set_start(self, start):
        self.start = start

    def add_rule(self, parent, children):
        children = tuple(children)
        self.rules.append((parent, children))

    def add_terminals(self, terminals):
        for symb in terminals:
            self.add_rule(symb, [])

    # def set_any_terminal(self, flag=True):
    #     self.any_terminal = flag

    def recognize(self, tree, debug=False):
        """
        Return True if tree obeys grammar, else False.
        """
        if self.start and tree.label != self.start:
            return False
        for node in tree.traverse():
            match = False
            parent_label = node.label
            child_labels = tuple(c.label for c in node.children)
            for rule in self.rules:
                # if self.any_terminal and not child_labels:
                #     match = True
                #     break
                if self._match_subtree(rule, parent_label, child_labels):
                    match = True
                    break
            if not match:
                if debug:
                    print(f"bad subtree: ({parent_label}, {child_labels})")
                return False
        return True

    @staticmethod
    def _match_subtree(rule, parent_label, child_labels):
        rule_label, rule_children = rule
        if not re.match(rule_label, parent_label):
            return False
        if len(child_labels) != len(rule_children):
            return False
        for c, rc in zip(child_labels, rule_children):
            if not re.match(rc, c):
                return False
        return True


if __name__ == "__main__":
    g1 = TreeGrammar(start='S')
    g1.add_rule('S', ['NP', 'VP'])
    g1.add_rule('NP', ['D', 'N'])
    g1.add_rule('NP', ['N'])
    g1.add_rule('NP', ['Pron'])
    g1.add_rule('VP', ['V-int'])
    g1.add_rule('VP', ['V-tr', 'NP'])
    g1.add_rule('D', ['the'])
    g1.add_rule('N', ['cat|rat'])
    g1.add_rule('V-int', ['sat|flew'])
    g1.add_rule('V-tr', ['chased'])
    g1.add_terminals(['the', 'cat', 'rat', 'sat', 'chased'])
    # g1.set_any_terminal(True)

    t1 = Tree.from_string("(S (NP (D the) (N cat)) (VP (V-tr chased) (NP (D the) (N rat))))")
    t2 = Tree.from_string("(S (NP (N cat) (D the)) (VP (NP (N rat) (D the)) (V-tr chased)))")
    t3 = Tree.from_string("(NP (D the) (N cat))")
    print(g1.recognize(t1, debug=True))
    print(g1.recognize(t2, debug=True))
    print(g1.recognize(t3, debug=True))
