# test2: test whether only match the first element in the LHS of a rule

import read, copy
from logical_classes import *
from student_code import KnowledgeBase


def main():
	KB = KnowledgeBase([], [])
	_, fact1 = read.parse_input("fact: (hero A)")
	_, fact2 = read.parse_input("fact: (person B)")
	_, rule1 = read.parse_input("rule: ((hero ?x) (person ?x)) -> (goodman ?x)")
	_, ask1 = read.parse_input("rule: ((person A)) -> (goodman A)")
	_, ask2 = read.parse_input("rule: ((hero B)) -> (goodman B)")
	KB.kb_assert(fact1)
	KB.kb_assert(fact2)
	KB.kb_assert(rule1)
	ask_rule1 = Rule(ask1)
	ask_rule2 = Rule(ask2)
		

	if ask_rule1 in KB.rules and ask_rule2 not in KB.rules:
		print "pass test2"
		exit(0)
	else:
		print "fail test2"
		exit(1)








if __name__ == '__main__':
    main()