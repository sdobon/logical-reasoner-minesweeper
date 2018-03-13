import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB

        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added

        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)

        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)

    def kb_assert(self, statement):
        """Assert a fact or rule into the KB

        Args:
            statement (Statement): Statement we're asserting in the format produced by read.py
        """
        printv("Asserting {!r}", 0, verbose, [statement])
        self.kb_add(Fact(statement) if factq(statement) else Rule(statement))

    def kb_ask(self, statement):
        """Ask if a fact is in the KB

        Args:
            statement (Statement) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        printv("Asking {!r}", 0, verbose, [statement])
        if factq(statement):
            f = Fact(statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else False

        else:
            print "Invalid ask:", statement
            return False

    def kb_remove_fact_rule(self, fact_rule):

        if not fact_rule.supported_by:
            if not fact_rule.asserted:
                print fact_rule
                if isinstance(fact_rule, Fact):
                    self.facts.remove(fact_rule) #remove rule from kb
                else:
                    self.rules.remove(fact_rule)


                for fact in fact_rule.supports_facts: #check all facts that the rule supports
                    for supported in fact.supported_by: #check all supports for that fact
                        if fact_rule in supported: #if rule is in the supported
                            fact.supported_by.remove(supported) #remove it
                    self.kb_remove_fact_rule(fact)

                for supported_rule in fact_rule.supports_rules: #check all rules that the rule supports
                    for supported in supported_rule.supported_by: #look at all supports of the supported rule
                        if fact_rule in supported: #if rule is in the supported
                            supported_rule.supported_by.remove(supported) #remove from the supported rull that support
                    self.kb_remove_fact_rule(supported_rule)


    def kb_retract(self, statement):
        """Retract a fact from the KB

        Args:
            statement (Statement) - Statement to be asked (will be converted into a Fact)

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [statement])
        ####################################################
        # Student code goes here
        fact_to_retract = False #no fact to retract
        for fact in self.facts: #loop through all facts and see if we can find a fact that matches up
            if Fact(statement) == fact:
                fact_to_retract = fact


        if fact_to_retract: #if fact to retract exists
            if not fact_to_retract.supported_by and fact_to_retract.asserted: #has no support
                    self.facts.remove(fact_to_retract) #remove from facts in kb

                    for fact in fact_to_retract.supports_facts: #look at all facts that the fact we removed support
                        for supported in fact.supported_by: #for each fact, look at what supports that fact
                            if fact_to_retract in supported: #see if our fact is in the support
                                fact.supported_by.remove(supported) #if so go into the supported by of that fact and remove the support
                        self.kb_remove_fact_rule(fact) #recurse on that fact

                    for rule in fact_to_retract.supports_rules: #look at all rules that our fact we remove supports
                        for supported in rule.supported_by: #for each rule, look at what supports that rule
                            if fact_to_retract in supported: #if the fact is in that support
                                rule.supported_by.remove(supported) #remove that support from the rules support
                        self.kb_remove_fact_rule(rule)
            else:
                fact_to_retract.asserted = False



        

class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing            
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here


        bindings = match(fact.statement, rule.lhs[0]) #find bindings for first statement of left hand

        if bindings:
            if len(rule.lhs) == 1: #lsh only has 1 statement

                new_statement = instantiate(rule.rhs, bindings) #new statement
                new_fact = Fact(new_statement, [(fact,rule)])

                for known_fact in kb.facts:
                    if new_fact == known_fact:
                        known_fact.supported_by.append((fact,rule))
                        fact.supports_facts.append(known_fact)
                        rule.supports_facts.append(known_fact)
                        return

                fact.supports_facts.append(new_fact) #add new _fact to support facts of fact
                rule.supports_facts.append(new_fact) #add new fact to support facts of rule
                kb.kb_add(new_fact) #add new fact ot the kb

            else: #lhs has more than 1 statement
                new_statements = [] #empty array of statements
                for statement in range(1, len(rule.lhs)):
                    new_statements.append(instantiate(rule.lhs[statement], bindings)) #add statements with binding
                new_rhs = instantiate(rule.rhs, bindings) #new rhs
                new_rule_statements = [new_statements, new_rhs]

                new_rule = Rule(new_rule_statements, [(fact,rule)])

                for known_rules in kb.rules:
                    if new_rule == known_rules:
                        known_rules.supported_by.append((fact,rule))
                        fact.supports_rules.append(known_rules)
                        rule.supports_rules.append(known_rules)
                        return

                fact.supports_rules.append(new_rule)
                rule.supports_rules.append(new_rule)

                kb.kb_add(new_rule)


