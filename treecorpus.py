from tree import Tree
from treegrammar import TreeGrammar


class TreeCorpus:
    def __init__(self):
        self.grammatical = []
        self.ungrammatical = []

    def add_grammatical(self, sent):
        if type(sent) is str:
            sent = Tree.from_string(sent)
        self.grammatical.append(sent)

    def add_ungrammatical(self, sent):
        if type(sent) is str:
            sent = Tree.from_string(sent)
        self.ungrammatical.append(sent)

    def test_grammar(self, gram, debug=False):
        truepos = []
        falsepos = []
        trueneg = []
        falseneg = []

        for sent in self.grammatical:
            if gram.recognize(sent):
                truepos.append(sent)
            else:
                falseneg.append(sent)
        for sent in self.ungrammatical:
            if gram.recognize(sent):
                falsepos.append(sent)
            else:
                trueneg.append(sent)

        print(f"True positives: {len(truepos)}")
        print(f"False positives: {len(falsepos)}")
        print(f"True negatives: {len(trueneg)}")
        print(f"False negatives: {len(falseneg)}")

        if debug:
            print("\n***False positives***")
            for sent in falsepos:
                print(sent)

            print("\n***False negatives***")
            for sent in falseneg:
                print(sent)
        else:
            print("Add option debug=True for more information.")


if __name__ == "__main__":
    g1 = TreeGrammar(start='S')
    g1.add_rule('S', ['NP', 'VP'])
    g1.add_rule('NP', ['D', 'N'])
    g1.add_rule('NP', ['N'])
    g1.add_rule('NP', ['Pron'])
    g1.add_rule('VP', ['V-int'])
    g1.add_rule('VP', ['V-tr', 'NP'])
    g1.add_rule('D', ['the'])
    g1.add_rule('N', ['cat'])
    g1.add_rule('N', ['rat'])
    g1.add_rule('V-int', ['sat'])
    g1.add_rule('V-tr', ['chased'])
    g1.add_terminals(['the', 'cat', 'rat', 'sat', 'chased'])

    corpus = TreeCorpus()
    corpus.add_grammatical("(S (NP (D the) (N cat)) (VP (V-tr chased) (NP (D the) (N rat))))")
    corpus.add_ungrammatical("(S (NP (N cat) (D the)) (VP (NP (N rat) (D the)) (V-tr chased)))")
    corpus.test_grammar(g1)
