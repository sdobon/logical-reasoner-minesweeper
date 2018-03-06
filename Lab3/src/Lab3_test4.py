# test4: test retract

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
	_, ask3 = read.parse_input("rule: ((person A)) -> (goodman A)")

	
	KB.kb_assert(fact1)
	KB.kb_assert(fact2)
	KB.kb_assert(rule1)
	KB.kb_assert(rule2)
	KB.kb_assert(fact3)
	answer1 = KB.kb_ask(ask1)
	answer2 = KB.kb_ask(ask2)
	answer3 = Rule(ask3) in KB.rules
	KB.kb_retract(fact1)
	answer4 = KB.kb_ask(ask1)
	answer5 = KB.kb_ask(ask2)
	answer6 = Rule(ask3) in KB.rules
	print KB


	if answer1 and answer2 and answer3 and not answer4 and not answer5 and not answer6:
		print "pass test4"
		exit(0)
	else:
		print "fail test4"
		exit(1)








if __name__ == '__main__':
    main()