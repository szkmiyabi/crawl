import sys
import os
from glob import glob
from collections import Counter
import MeCab
import re

def main():

    input_dir = sys.argv[1]
    tagger = MeCab.Tagger()
    tagger.parse('') # bug fix.
    frequency = Counter()
    count_processed = 0

    for path in glob(os.path.join(input_dir, '*.txt')):
        print('Processing {0}...'.format(path), file=sys.stderr)

        with open(path) as file:
            #for content in iter_docs(file):
            content = file.read()
            content = text_clean(content)
            tokens = get_tokens(tagger, content)
            frequency.update(tokens)
            count_processed += 1
            if count_processed % 1000 == 0:
                print('{0} documents were processed.'.format(count_processed), file=sys.stderr)
    
    for token, count in frequency.most_common():
        print(token, count)

def text_clean(content):
    txt = None
    txt = re.sub(r'(\t|\s{3,}|\r\n{2,}|\n{2,})+', "", content, re.DOTALL)
    return txt

def get_tokens(tagger, content):
    tokens = []
    node = tagger.parseToNode(content)
    while node:
        category, sub_category = node.feature.split(',')[:2]
        if category == '名詞' and sub_category in ('固有名詞', '一般'):
            tokens.append(node.surface)
        node = node.next
    return tokens

if __name__ == '__main__':
    main()