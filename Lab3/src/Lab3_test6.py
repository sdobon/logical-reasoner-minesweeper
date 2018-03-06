# test6: test long inference

import read, copy
from logical_classes import *
from student_code import KnowledgeBase


def main():
	KB = KnowledgeBase([], [])
	_, fact1 = read.parse_input("fact: (rela A B)")
	_, fact2 = read.parse_input("fact: (relb B C)")
	_, fact3 = read.parse_input("fact: (reld C D)")
	_, fact4 = read.parse_input("fact: (relf D E)")
	_, fact5 = read.parse_input("fact: (relh E F)")

	_, rule1 = read.parse_input("rule: ((rela ?x ?y) (relb ?y ?z)) -> (relc ?x ?z)")
	_, rule2 = read.parse_input("rule: ((relc ?x ?y) (reld ?y ?z)) -> (rele ?x ?z)")
	_, rule3 = read.parse_input("rule: ((rele ?x ?y) (relf ?y ?z)) -> (relg ?x ?z)")
	_, rule4 = read.parse_input("rule: ((relg ?x ?y) (relh ?y ?z)) -> (reli ?x ?z)")

	_, ask1 = read.parse_input("fact: (reli A F)")

	KB.kb_assert(fact1)
	KB.kb_assert(fact2)
	KB.kb_assert(fact3)
	KB.kb_assert(fact4)
	KB.kb_assert(fact5)
	KB.kb_assert(rule1)
	KB.kb_assert(rule2)
	KB.kb_assert(rule3)
	KB.kb_assert(rule4)
	
	answer1 = KB.kb_ask(ask1)

	if answer1:
		print "pass test6"
		exit(0)
	else:
		print "fail test6"
		exit(1)



if __name__ == '__main__':
    main()