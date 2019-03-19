# -*- coding: utf-8 -*
class LivSeg(object):

    def __init__(self,type):
        self.close = []
        self.date = []
        self.type = type  #all  ambi   ut=upward trend    dt=downward trend    nra=natural rally   nre=natrual reaction   nf-nra   nf-nre   sra=secondary rally    sre=secondary reaction
        self.line = '' #red black