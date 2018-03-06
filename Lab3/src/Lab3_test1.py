# test1: test inference from facts and rule

import read, copy
from logical_classes import *
from student_code import KnowledgeBase


def main():
	KB = KnowledgeBase([], [])
	_, fact1 = read.parse_input("fact: (hero A)")
	_, fact2 = read.parse_input("fact: (person A)")
	_, rule1 = read.parse_input("rule: ((hero ?x) (person ?x)) -> (goodman ?x)")
	_, ask1 = read.parse_input("fact: (goodman A)")

	KB.kb_assert(fact1)
	KB.kb_assert(fact2)
	KB.kb_assert(rule1)
	answer = KB.kb_ask(ask1)

	if answer:
		print "pass test1"
		exit(0)
	else:
		print "fail test1"
		exit(1)








if __name__ == '__main__':
    main()