from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode) 
        self.smallest_str = None
        self.end = None
    def __getitem__(self, c):
        return self.children[c]
class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, s: str):
        node = self.root
        for c in s:
            node = node[c]
            if node.smallest_str is None:
                node.smallest_str = s
        node.end = s
    def get_similar(self, s):
        node = self.root
        for i, c in enumerate(s):
            if c not in node.children:
                i -= 1
                break
            node = node[c]
        return (node.smallest_str or node.end, i + 1)


class Matcher:
    def __init__(self, dic: dict):
        self.trie = Trie()
        for s in dic:
            self.trie.insert(s)

    def get_match(self, s: str) -> tuple:
        return self.trie.get_similar(s)


if __name__ == '__main__':
    s = {
        'a': 1,
        'b': 2,
        'aa': 3,
        'abcc': 4
    }
    matcher = Matcher(s)
    print(matcher.get_match('abcc'))