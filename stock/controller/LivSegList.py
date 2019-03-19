# -*- coding: utf-8 -*
from LivSeg import LivSeg

class LivSegList(object):

    def __init__(self):
        self.livSegAll = LivSeg('all')
        self.list = []
        self.lastBlackClose = -1.00 #red black
        self.lastRedClose = -1.00 #red black
        self.lastDTClose = -1.00
        self.lastUTClose = -1.00