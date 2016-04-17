#! /usr/bin/env python

# -*- coding: utf-8 -*-

import os
import os.path
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

    def __init__(self, question, answers, prompt, hint = None):
        self.question = question
        self.hint = hint
        self.answers = answers
        self.prompt = prompt

    def query(self):
        print self.question, self.prompt,
        if self.hint:
            print ":", self.hint
        else:
            print ""
        resp = raw_input(":")
        if resp in self.answers:
            print "Genau! %s\n" % " or ".join(self.answers)
            return True
        elif resp == "n/a": 
            return True
        else:
            print "Nein!"
            print " or ".join(self.answers)
            print ""
            return False

class Translation(Question):
    
    def __init__(self, word, translations, hint):
        Question.__init__(self, "Translate", translations, word, hint)

class ForeignTranslation(Translation):

    def __init__(self, word, translations, hint):
        hint = hint.replace("#", "")
        #print word, translations, hint
        Question.__init__(self, "Translate", translations, word, hint)

class NativeTranslation(Translation):

    def __init__(self, word, translations, hint):
        if hint:
            str_arr = hint.split("#")
            try:
                repl = "_" * (len(str_arr[1]))
            except IndexError:
                print word, translations, hint
                sys.exit("Improper format")
            str_arr[1] = repl
            hint = "".join(str_arr)
            Question.__init__(self, "Translate", translations, word, hint)
        else:
            #print word, translations, hint
            Question.__init__(self, "Translate", translations, word, hint)


class Quiz:
    
    def __init__(self):
        self.questions = []

    def append(self, q):
        self.questions.append(q)

    def add(self, question, answer, prompt = None):
        q = Question(question, answer, prompt)
        self.append(q)

    def translation(self, word, translation, example):
        translations = map(strip, translation.split(","))
        words = map(strip, word.split(","))
        for w in words:
          t = ForeignTranslation(w, translations, example)
          self.append(t)

        translation = " or ".join(translations)
        t = NativeTranslation(translation, words, example)
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
            splitter = line.split(":")
            if len(splitter) == 2:
                word, answers = map(strip, splitter)
                self.translation(word=word, translation=answers, example="")
            else:
                word, answers, example = map(strip, splitter)
                self.translation(word=word, translation=answers, example=example)

    def start(self):
        import random
        random.shuffle(self.questions)

    def __iter__(self):
        return iter(self.questions)


if __name__ == "__main__":
    path = sys.argv[1]
    quiz = Quiz()
    quiz.add_translations(path)
    quiz.start()
    questions = quiz.questions
    while questions:
      wrongAnswers = []
      for q in questions:
          correct = q.query()
          if not correct:
            wrongAnswers.append(q)
      questions = wrongAnswers

        



