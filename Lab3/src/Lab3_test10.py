# test10: test delete asserted and supported_by fact, only change flag

import read, copy
from logical_classes import *
from student_code import KnowledgeBase


def main():
	KB = KnowledgeBase([], [])
	_, fact1 = read.parse_input("fact: (hero A)")
	_, fact2 = read.parse_input("fact: (person A)")
	_, fact3 = read.parse_input("fact: (goodman A)")
	_, rule1 = read.parse_input("rule: ((hero ?x) (person ?x)) -> (goodman ?x)")

	KB.kb_assert(fact1)
	KB.kb_assert(fact2)
	KB.kb_assert(fact3)
	KB.kb_assert(rule1)
	answer1 = KB.facts[KB.facts.index(Fact(fact3))].asserted
	KB.kb_retract(fact3)
	answer2 = KB.facts[KB.facts.index(Fact(fact3))].asserted

	if answer1 and not answer2:
		print "pass test10"
		exit(0)
	else:
		print "fail test10"
		exit(1)



if __name__ == '__main__':
    main()