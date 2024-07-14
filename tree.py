class Tree:
    def __init__(self, label, children=None):
        """
        Construct a tree consisting of a single node with the given label,
        assumed to be a string. Children may optionally be provided as
        a list of subtrees.
        """
        if not isinstance(label,str):
            raise ValueError("Parameter 'label' must be str.")
        self.label = label
        if children is None:
            children = []
        elif not isinstance(children,list):
            raise ValueError("Parameter 'children' must be list.")
        self.children = children

    @staticmethod
    def from_list(nodes):
        """
        Construct tree from list of form [label, child1, child2, ...].
        Brackets around terminal nodes may be omitted.
        """
        if not isinstance(nodes, list):
            nodes = [nodes]
        if len(nodes) < 1:
            raise ValueError("Tree level cannot be empty.")
        elif len(nodes) == 1:
            return Tree(nodes[0])
        else:
            parent = nodes.pop(0)
            return Tree(parent, [Tree.from_list(n) for n in nodes])

    @staticmethod
    def from_string(text):
        text = text.strip()
        return Tree._parse(Tree._tokenize(text))

    def _tokenize(text):
        text = text.replace('(', ' ( ').replace(')', ' ) ')
        toks = text.split()
        toks = [t.strip() for t in toks]
        return toks

    def _parse(toks, d=0):
        # print(d, toks)
        # opening paren
        if toks[0] != '(':
            raise ValueError(f"Expected '(' but got '{toks[0]}'.")
        toks.pop(0)
        # label
        if toks[0] == '(':
            raise ValueError(f"Expected label but got '('.")
        if toks[0] == ')':
            raise ValueError(f"Expected label but got ')'.")
        label = toks.pop(0)
        # children
        children = []
        while toks and toks[0] != ')':
            if toks[0] != '(':
                children.append(Tree(toks.pop(0)))
            else:
                children.append(Tree._parse(toks, d+1))
        # closing paren
        if not toks:
            raise ValueError("Missing closing parenthesis.")
        toks.pop(0)
        if d == 0 and toks:
            if toks[0] == ')':
                raise ValueError("Extra closing parenthesis.")
            else:
                raise ValueError("Extra material after closing parenthesis.")
        return Tree(label, children)

    def __str__(self):
        if len(self.children) > 0:
            return "({} {})".format(
                self.label, ' '.join(str(c)for c in self.children))
        else:
            return '(' + str(self.label) + ')'

    __repr__ = __str__

    def __eq__(self, other):
        return (self.label == other.label
                and len(self.children) == len(other.children)
                and all(c == d for c, d in zip(self.children, other.children)))

    # def pformat(self):
    #     if len(self.children) > 0:
    #         return str([str(self.label)] + [c.pformat() for c in self.children])
    #     else:
    #         return str(self.label)

    def add_child(self, child):
        """
        Add given subtree as the last child of this tree.
        """
        self.children.append(child)

    def insert(self, pos, child):
        """
        Add given subtree in given position.
        """
        self.children.insert(pos, child)

    def size(self):
        """
        Return the number of nodes contained in the tree.
        """
        return 1 + sum(c.size() for c in self.children)

    def yld(self, sep=' '):
        """
        Return the string formed by concatenating all leaf nodes in the tree.
        """
        if len(self.children) > 0:
            return ' '.join(c.yld() for c in self.children)
        else:
            return self.label

    def depth(self):
        """
        Return the depth of the tree, where a single root node has depth 0
        and each additional level adds 1 to the depth.
        """
        if len(self.children) > 0:
            return 1 + max(c.depth() for c in self.children)
        else:
            return 0

    def width(self):
        """
        Return width of the tree, defined as the largest number of children
        of any node in the tree, or 0 in the case of a single root node.
        """
        if len(self.children) > 0:
            return max(len(self.children), max(c.width() for c in self.children))
        else:
            return 0

    def get_gorn(self, addr):
        """
        Return subtree at given gorn address, given as a list of non-negative
        integers. Return None if address not found.
        """
        if len(addr) > 0:
            i = addr.pop(0)
            if i in range(len(self.children)):
                return self.children[i].get_gorn(addr)
            else:
                return None
        else:
            return self

    def traverse(self, method="preorder", withgorn=False, gorn=None):
        """
        Generator for traversing tree.
        """
        if gorn is None:
            gorn = []
        if method not in ("preorder", "postorder"):
            raise ValueError("Parameter 'method' must be one of {preorder,postorder}.")
        if method == "preorder":
            yield self if not withgorn else (gorn, self)
        for n, c in enumerate(self.children):
            yield from c.traverse(method, withgorn, gorn + [n])
        if method == "postorder":
            yield self if not withgorn else (gorn, self)


if __name__ == "__main__":
    # t = Tree("boo", [Tree("baa"), Tree("bee")])
    # print(t)
    # t = Tree.from_list(['a', ['b', ['c', 'd'], 'e']])
    # print(t)
    s = "(a (b (c)) (d (e (f) (g)) (h)))"
    t = Tree.from_string(s)
    # print(t)
    # for e in t.traverse():
    #     print(e.label)
    print(str(t) == s)
    "(a (b (c)) (d (e (f) (g)) (h)))"
