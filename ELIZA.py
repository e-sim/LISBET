# -----------------------------------
# starting recreation of ELIZA for use with LISBET project
# based on Wade Brainerd's Python implementation of same
# with influence from Joe Strout & Jez Higgins's version
# and of course thanks to Joseph Weizenbaum
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