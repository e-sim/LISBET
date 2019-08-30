# -----------------------------------
# starting recreation of ELIZA for use with LISBET project
# based on Wade Brainerd's Python implementation of same
# with influence from Joe Strout & Jez Higgins's version
# and of course all thanks to Joseph Weizenbaum
# updated & added to by Erica Sim 
# requires dialog script file (therapist.txt)
#----------------------------------------


import re, random, logging

log = logging.getLogger(__name__)

class Key:
    def __init__(self, word, weight, decomps):
        self.word = word
        self.weight = weight
        self.decomps = decomps

class Decomp:
    def __init__(self, parts, save, reasmbs):
        self.parts = parts
        self.save = save
        self.reasmbs = reasmbs
        self.next_reasmb_index = 0

class Eliza:
    def __init__(self):
        self.initials = []
        self.finals = []
        self.quits = []
        self.pres = {}
        self.posts = {}
        self.synons = {}
        self.keys = {}
        self.memory = []

''' loads the dialog phrases from file and saves them in corresp tag's list
'''
    def load(self, path):
        key = None
        decomp = None
        with open(path) as file:

            for line in file:

                if not line.strip():
                    continue
                # vv confusing, come back    
                tag, content = [part.strip() for part in line.split(":")]
                if tag == "initial":
                    self.initials.append(content)
                elif tag == "final":
                    self.finals.append(content)
                elif tag == "quit":
                    self.quits.append(content)
                elif tag == "pre":
                    parts = content.split(" ")
                    self.pres[parts[0]] = parts[1:]
                elif tag == "post":
                    parts = content.split(" ")
                    self.posts[parts[0]] = parts[1:]
                elif tag == "synon":
                    parts = content.split(" ")
                    self.synons[parts[0]] = parts
                elif tag == "key":
                    parts = content.split(" ")
                    word = parts[0]
                    weight = int(parts[1]) if len(parts) > 1 else 1
                    key = Key(word, weight, [])
                    self.keys[word] = key
                elif tag == "decomp":
                    parts = content.split(" ")
                    save = False
                    if parts[0] == "$":
                        save = True
                        parts = parts[1:]
                    decomp = Decomp(parts, save, [])
                    key.decomps.append(decomp)
                elif tag == "reasmb":
                    parts = content.split(" ")
                    decomp.reasmbs.append(parts)

    def match_decomp_r(self, parts, words, results):
    # what does it do
        if not parts and not words:
            return True
        if not parts or (not words and parts != ["*"]):
            return False
        if parts[0] == "*":
            for index in range(len(words), -1, -1):
                results.append(words[:index])
                if self.match_decomp_r(parts[1:], words[index:], results):
                    return True
                results.pop()
            return False
        elif parts[0].startswith("@"):
            root = parts[0][1:]
            if not root in self.synons:
                raise ValueError("Unknown synonym root {}".format(root))
            if not words[0].lower() in self.synons[root]:
                return False
            results.append([words[0]])
            return self.match_decomp_r(parts[1:], words[1:], results)
        elif parts[0].lower() != words[0].lower():
            return False
        else:
            return self.match_decomp_r(parts[1:], words[1:], results)

    def match_decomp(self, parts, words):
        results = []
        if self.match_decomp_r(parts, words, results):
            return results
        return None

    def next_reasmb(self, decomp):
        index = decomp.next_reasmb_index
        result = decomp.reasmbs[index % len(decomp.reasmbs)]
        decomp.next_reasmb_index = index + 1
        return result

    def reassemble(self, reasmb, results):
        output = []
        for reword in reasmb:
            if not reword:
                continue
            if reword[0] == "(" and reword[-1] == ")":
            # that is if it's in parentheses, #s in parens represent phrases (like formatting)
                index = int(reword[1:-1])
                if index < 1 or index > len(results):
                    raise ValueError("Invalid result index {}".format(index))
                insert = results[index - 1]
                for punct in [",", ".", ";"]
                    if punct in insert:
                        insert = insert[:insert.index(punct)]
                output.extend(insert)
            else:
                output.append(reword)
        return output

    def sub(self, words, sub):
        output = []
        for word in words:
            word_lower = word.lower()
            if word_lower in sub:
                output.extend(sub[word_lower])
            else:
                output.append(word)
        return output




def main():
    eliza = Eliza()
    eliza.load("therapist.txt")
    eliza.run()

if __name__ == "__main__":
    logging.basicConfig()
    main()