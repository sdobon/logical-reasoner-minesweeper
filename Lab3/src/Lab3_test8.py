# test8: test long inference

import read, copy
from logical_classes import *
from student_code import KnowledgeBase


def main():
	KB = KnowledgeBase([], [])
	_, fact1 = read.parse_input("fact: (rela A X)")
	_, fact2 = read.parse_input("fact: (relb B X)")
	_, fact3 = read.parse_input("fact: (relc C X)")
	_, fact4 = read.parse_input("fact: (reld D X)")
	_, fact5 = read.parse_input("fact: (rele E X)")

	_, rule1 = read.parse_input("rule: ((rela ?a ?x) (relb ?b ?x) (relc ?c ?x) (reld ?d ?x) (rele ?e ?x)) -> (relf ?x)")

	_, ask1 = read.parse_input("fact: (relf X)")

	KB.kb_assert(fact1)
	KB.kb_assert(fact2)
	KB.kb_assert(fact3)
	KB.kb_assert(fact4)
	KB.kb_assert(fact5)
	KB.kb_assert(rule1)

	
	answer1 = KB.kb_ask(ask1)

	if answer1:
		print "pass test8"
		exit(0)
	else:
		print "fail test8"
		exit(1)



if __name__ == '__main__':
    main()