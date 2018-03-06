# test5: test retract and need to check whether the fact is assert or infered from other facts.

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
	_, fact4 = read.parse_input("fact: (goodman A)")
	_, ask1 = read.parse_input("fact: (goodman A)")
	_, ask2 = read.parse_input("fact: (doctor A)")
	_, ask3 = read.parse_input("rule: ((person A)) -> (goodman A)")

	KB.kb_assert(fact1)
	KB.kb_assert(fact2)
	KB.kb_assert(fact4)
	KB.kb_assert(rule1)
	KB.kb_assert(rule2)
	KB.kb_assert(fact3)
	
	print KB
	answer1 = KB.kb_ask(ask1)
	answer2 = KB.kb_ask(ask2)
	KB.kb_retract(fact1)
	answer3 = not Rule(ask3) in KB.rules
	answer4 = KB.kb_ask(ask1)
	answer5 = KB.kb_ask(ask2)

	KB2 = KnowledgeBase([], [])
	_, fact21 = read.parse_input("fact: (relaa A)")
	_, fact22 = read.parse_input("fact: (relab A)")
	_, rule21 = read.parse_input("rule: ((relaa ?x)) -> (good ?x)")
	_, rule22 = read.parse_input("rule: ((relab ?x)) -> (good ?x)")
	_, ask21 = read.parse_input("fact: (good ?x)")

	KB2.kb_assert(fact21)
	KB2.kb_assert(fact22)
	KB2.kb_assert(rule21)
	KB2.kb_assert(rule22)
	answer6 = KB2.kb_ask(ask21)
	KB2.kb_retract(fact21)
	answer7 = KB2.kb_ask(ask21)
	answer8 = not KB2.kb_ask(fact21)


	if answer1 and answer2 and answer3 and answer4 and answer5 and answer6 and answer7 and answer8:
		print "pass test5"
		exit(0)
	else:
		print "fail test5"
		exit(1)

	





if __name__ == '__main__':
	main()