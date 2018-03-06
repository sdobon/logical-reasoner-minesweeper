# test3: more complicated inference test

import read, copy
from logical_classes import *
from student_code import KnowledgeBase


def main():
	KB = KnowledgeBase([], [])
	_, fact1 = read.parse_input("fact: (hero A)")
	_, fact2 = read.parse_input("fact: (person A)")
	_, rule1 = read.parse_input("rule: ((hero ?x) (person ?x)) -> (goodman ?x)")
	_, rule2 = read.parse_input("rule: ((goodman ?x) (wenttoschool ?x)) -> (doctor ?x)")
	_, fact3 = read.parse_input("fact: (wenttoschool A)")
	_, ask1 = read.parse_input("fact: (goodman A)")
	_, ask2 = read.parse_input("fact: (doctor A)")

	
	KB.kb_assert(fact1)
	KB.kb_assert(fact2)
	KB.kb_assert(rule1)
	answer1 = KB.kb_ask(ask1)
	KB.kb_assert(rule2)
	KB.kb_assert(fact3)
	answer2 = KB.kb_ask(ask2)


	if answer1 and answer2:
		print "pass test3"
		exit(0)
	else:
		print "fail test3"
		exit(1)








if __name__ == '__main__':
    main()