# test9: test predicates with more parameters

import read, copy
from logical_classes import *
from student_code import KnowledgeBase


def main():
	KB = KnowledgeBase([], [])
	_, fact1 = read.parse_input("fact: (rela A B C D E F)")
	_, fact2 = read.parse_input("fact: (relb D E F G H I)")
	_, fact3 = read.parse_input("fact: (reld G H I)")

	_, rule1 = read.parse_input("rule: ((rela ?a ?b ?c ?d ?e ?f) (relb ?d ?e ?f ?g ?h ?i)) -> (relc ?a ?b ?c ?g ?h ?i)")
	_, rule2 = read.parse_input("rule: ((relc ?a ?b ?c ?g ?h ?i) (reld ?g ?h ?i)) -> (rele ?a ?b ?c)")


	_, ask1 = read.parse_input("fact: (rele A B C)")

	KB.kb_assert(fact1)
	KB.kb_assert(fact2)
	KB.kb_assert(fact3)
	KB.kb_assert(rule1)
	KB.kb_assert(rule2)
	
	answer1 = KB.kb_ask(ask1)
	KB.kb_retract(fact1)
	answer2 = KB.kb_ask(ask1)

	if answer1 and not answer2:
		print "pass test9"
		exit(0)
	else:
		print "fail test9"
		exit(1)



if __name__ == '__main__':
    main()