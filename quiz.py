# -*- coding: utf-8 -*-

import sys
import re
import codecs

def strip(x):
    return x.strip()

class ustdio(object):
    def __init__(self, stream):
        self.stream = stream
        self.encoding = stream.encoding
    def readline(self):
        return self.stream.readline().decode(self.encoding)
sys.stdin = ustdio(sys.stdin)


class Question:

    def __init__(self, question, answer, prompt = None):
        self.question = question
        if prompt:
            repl = "_" * len(answer)
            self.prompt = prompt.replace(" _ ", " %s " % repl)
        else:
            self.prompt = ""
        self.answer = answer

    def query(self):
        print self.question
        if self.prompt:
            print self.prompt
        resp = raw_input(":")
        if resp == self.answer:
            print "Genau!\n"
        else:
            print "Nein!"
            print self.answer
            print ""

class Translation(Question):
    
    def __init__(self, word, translation):
        Question.__init__(self, "Translate", translation, word)

class Quiz:
    
    def __init__(self):
        self.questions = []

    def append(self, q):
        self.questions.append(q)

    def add(self, question, answer, prompt = None):
        q = Question(question, answer, prompt)
        self.append(q)

    def translation(self, word, translation):
        t = Translation(word, translation)
        self.append(t)
        t = Translation(translation, word)
        self.append(t)

    def add_tense(self, verb, tense, text):
        for line in text.strip().splitlines():
            pronoun, conjug = map(strip, line.split(":"))
            qtext = unicode("Conjugate ") + verb + " in tense " + tense
            q = Question(qtext, conjug, pronoun)
            self.append(q)

    def add_verb(self, verb, text):
        verb = verb.strip()
        tenses = re.compile(r'([a-z]+)\s*[=]\s*[{](.*?)[}]', re.DOTALL).findall(text.strip())
        for tense, text in tenses:
            self.add_tense(verb, tense, text)

    def add_verbs(self, path):
        f = codecs.open(path, "r", "utf-8")
        text = f.read().strip()
        verbs = re.compile(r'^(.*?)[=]\s*[[](.*?)[]]', re.DOTALL).findall(text)
        for verb, text in verbs:
            self.add_verb(verb, text)


    def add_translations(self, path):
        f = codecs.open(path, "r", "utf-8")
        text = f.read().strip()
        for line in text.splitlines():
            w1, w2 = line.split(":")
            self.translation(w1.strip(), w2.strip())

    def start(self):
        import random
        random.shuffle(self.questions)

    def __iter__(self):
        return iter(self.questions)


if __name__ == "__main__":
    quiz = Quiz()
    #quiz.add_translations("translations")
    quiz.add_verbs("conjugations")
    quiz.start()
    for q in quiz:
        q.query()
        



