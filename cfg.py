import numpy as np


class CFG:

    def __init__(self, alpha, nonterm, start, rules):
        self.alpha = alpha
        self.nonterm = nonterm
        self.start = start
        self.rules = rules

    @property
    def terminal_rules(self):
        return list(r for r in self.rules if len(r) == 2
                    and r[0] in self.nonterm and r[1] not in self.nonterm)

    @property
    def unary_rules(self):
        return list(r for r in self.rules if len(r) == 2
                    and r[0] in self.nonterm and r[1] in self.nonterm)

    @property
    def binary_rules(self):
        return list(r for r in self.rules if len(r) == 3)

    def __str__(self):
        print(f"CFG({repr(self.rules)})")

    def parse(self, sent):
        """Parse a sentence given as a list of words."""
        return self._cyk(sent)

    def _cyk(self, sent):
        """Parse a sentence given as a list of words. Uses the CYK algorithm."""
        # array of form [span_length, word_idx, nonterm_idx]
        chart = np.full((len(sent), len(sent), len(self.nonterm)), False)
        # back = np.full((len(sent), len(sent), len(self.nonterm)), list())
        n_words = len(sent)
        # n_term = len(self.terminal_rules)

        for i, word in enumerate(sent):
            for j, sym in enumerate(self.nonterm):
                for r in self.rules:
                    if r == (sym, word):
                        chart[0,i,j] = True

        # for spanlen in range(2, n_words + 1):  # Length of span
        #     for start in range(0, n_words - spanlen):  # Start of span
        #         for part in range(0, spanlen - 1):  # Partition of span
        #             for i, r in enumerate(self.rules):
        #                 if r == ()
        #                 if P[part,start,b] and P[spanlen-part,start+part,c] then
        #                     set P[spanlen,start,a] = true,
        #                     append <p,b,c> to back[l,s,a]

        for i in range(n_words):
            for j in range(n_words):
                labels = ','.join(self.nonterm[k][0] for k in range(len(self.nonterm))
                                  if chart[i,j,k])
                print(f"{labels:3}" if labels else "---", end=' ')
            print()
        return None


def test():
    g = CFG(alpha=['S', 'A', 'a'], nonterm=['S', 'A'], start='S',
            rules=[('S', 'A'), ('A', 'A', 'A'), ('A', 'a')])
    g.parse("aaa")


if __name__ == "__main__":
    test()
