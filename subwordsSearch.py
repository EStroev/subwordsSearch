import re
from collections import defaultdict
import sys
import gc

word_dict = defaultdict(set)


def load_words(inFile):
    global word_dict
    wordPattern = re.compile(r'(\w+)')
    with open(inFile) as inF:
        for line in inF:
            line = line.strip()
            match = wordPattern.match(line)
            if match:
                wv = match.group(1).upper()
                wk = ''.join(sorted(list(wv)))
                word_dict[wk].add(wv)
    print(f'[+] Done. Its was loaded {len(word_dict)} words.txt')


def find_word(word):
    global word_dict
    word = ''.join(sorted(list(word)))
    return word_dict[word]


def select(lst, n):
    if n == 0 or lst == [] or len(lst) < n:
        return [[]]
    elif n == 1:
        return [[e] for e in lst]
    elif len(lst) == n:
        return [lst]
    elif len(lst) > n:
        return [[lst[0]] + s for s in select(lst[1:], n - 1)] + select(lst[1:], n)


def wselect(word, n):
    return {''.join(w) for w in select(list(word), n)}


def words(word_set):
    wset = set()
    for w in word_set:
        wl = find_word(w)
        if wl != set():
            wset = wset.union(wl)
    return wset


def get_words(wseq, n):
    return words(wselect(wseq, n))


class SessionRepl:
    def __init__(self):
        self.word = ''
        self.word_len = {}
        self.wset = False

    def set_word(self, w):
        self.clear()
        self.word = w
        self.wset = True
        self.word_len = {}

    def print_words(self, n):
        if not self.wset:
            return
        if n not in self.word_len:
            s = get_words(self.word, int(n))
            self.word_len[n] = s
        else:
            s = self.word_len[n]
        print(s)

    def auto(self):
        if not self.wset:
            return
        for n in range(1, len(self.word)):
            if n not in self.word_len:
                s = get_words(self.word, int(n))
                self.word_len[n] = s
            else:
                s = self.word_len[n]
            if s:
                print(f'{n}: {s}')

    def clear(self):
        self.word = ''
        self.word_len = None
        self.wset = False
        gc.collect()


def help():
    m = '''
Available commands:
    :help: prints this message.
    :clear: removes current word. To set a new one, use set command.
    :quit: quits the REPL.
    :auto: prints the set of all the sub-words for current word set. 
    <word>: sets the current word as <word>. All sub-words.txt are taken from this one.
    <length:int>: prints the set of sub-words of length <length> (an int) for the current word set. Shows nothing when no word is set.
    '''
    print(m)


def repl():
    session = SessionRepl()
    session.clear()

    while True:
        line = input('> ').strip()
        parts = re.split(r'\s+', line)
        l = len(parts)
        if l < 0 or l > 2:
            print('*** Bad command')
            continue
        command = parts[0].upper()
        if command == ':HELP':
            help()
        elif command == ':AUTO':
            session.auto()
        elif command == ':CLEAR':
            session.clear()
        elif command == ':QUIT':
            sys.exit(0)
        elif re.match(r'[a-zA-Z]{1,}', command):
            word = parts[0].upper()
            session.set_word(word)
            print('[+] Word was set up. Enter the length of subwords')
        elif re.match(r'\d+', command):
            length = int(command)
            session.print_words(length)
        else:
            print('*** Not sure what that means, try help')


if __name__ == '__main__':
    print('words-search utility\ntype :help to see available commands\ntype :quit to exit the prompt\n')
    print('[*] Loading dictionary... ')
    load_words('words.txt')
    repl()