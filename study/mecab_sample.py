import MeCab

tagger = MeCab.Tagger()
tagger.parse('') # this is a fix for .parseToNode bug.

node = tagger.parseToNode('すもももももももものうち')
while node:
    print(node.surface, node.feature)
    node = node.next