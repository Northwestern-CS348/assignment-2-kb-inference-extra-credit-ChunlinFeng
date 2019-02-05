import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()
        self.space_count = 0

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
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
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
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_or_rule):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_or_rule])
        ####################################################
        # Student code goes here

        # List several rules here
        # An asserted fact should only be removed if it is unsupported.
        # Rules must never be retracted and an asserted rule should never be removed.
        # Use the supports_rules and supports_facts fields to find and adjust facts and rules that are supported by a retracted fact.
        # The supported_by lists in each fact/rule that it supports needs to be adjusted accordingly.
        # If a supported fact/rule is no longer supported as a result of retracting this fact (and is not asserted), it should also be removed.

        # if fact or rule has more than one supported_by, do not remove
        if isinstance(fact_or_rule, Fact):
            if fact_or_rule not in self.facts:
                return None
            else:
                ind = self.facts.index(fact_or_rule)
                fact_or_rule = self.facts[ind]
        elif isinstance(fact_or_rule, Rule):
            if fact_or_rule not in self.rules:
                return None
            else:
                ind = self.rules.index(fact_or_rule)
                fact_or_rule = self.rules[ind]



        if len(fact_or_rule.supported_by)>0: pass;
        else:
        # able to delete
            if isinstance(fact_or_rule, Fact):
                # find the fact

                for item in fact_or_rule.supports_facts:
                    # syn the item
                    if item in self.facts:
                        index_item = self.facts.index(item)
                        item = self.facts[index_item]

                    # find the supported one and del it
                    i_flag = - 0;
                    length = len(item.supported_by)
                    for i in range(length):
                        real_i = i + i_flag
                        if item.supported_by[real_i][0] == fact_or_rule:
                            del item.supported_by[real_i]
                            i_flag -= 1
                            self.kb_retract(item)
                for item in fact_or_rule.supports_rules:
                    # syn the item
                    if item in self.rules:
                        index_item = self.rules.index(item)
                        item = self.rules[index_item]

                    i_flag = - 0;
                    length = len(item.supported_by)
                    for i in range(length):
                        real_i = i + i_flag
                        if item.supported_by[real_i][0] == fact_or_rule:
                            del item.supported_by[real_i]
                            i_flag -= 1
                            self.kb_retract(item)

                # del the fact_or_rule
                ind = self.facts.index(fact_or_rule)
                del self.facts[ind]

            elif isinstance(fact_or_rule, Rule):
                if fact_or_rule.asserted == True: pass;
                else:
                    for item in fact_or_rule.supports_facts:
                        # syn the item
                        if item in self.facts:
                            index_item = self.facts.index(item)
                            item = self.facts[index_item]

                        # find the supported one and del it
                        i_flag = - 0;
                        length = len(item.supported_by)
                        for i in range(length):
                            real_i = i + i_flag
                            if item.supported_by[real_i][1] == fact_or_rule:
                                del item.supported_by[real_i]
                                i_flag -= 1
                                self.kb_retract(item)
                    for item in fact_or_rule.supports_rules:
                        # syn the item
                        if item in self.rules:
                            index_item = self.rules.index(item)
                            item = self.rules[index_item]

                        i_flag = - 0;
                        length = len(item.supported_by)
                        for i in range(length):
                            real_i = i + i_flag
                            if item.supported_by[real_i][1] == fact_or_rule:
                                del item.supported_by[real_i]
                                i_flag -= 1
                                self.kb_retract(item)

                    # del the fact_or_rule
                    ind = self.rules.index(fact_or_rule)
                    del self.rules[ind]

    def kb_explain(self, fact_or_rule):
        """
        Explain where the fact or rule comes from

        Args:
            fact_or_rule (Fact or Rule) - Fact or rule to be explained

        Returns:
            string explaining hierarchical support from other Facts and rules
        """
        ####################################################
        # Student code goes here

        # sample is a FACT
        if isinstance(fact_or_rule, Fact):
            # not exist in KB
            if fact_or_rule not in self.facts: return "Fact is not in the KB"
            else:
                # get the right fact and convert
                fact = self._get_fact(fact_or_rule)
                result = self.statement_converter(fact,1,self.space_count)

                if len(fact.supported_by) >0:
                    for supported_by in fact.supported_by:
                        result += "\n" + self.statement_converter("", 0, self.space_count)  # +SUPPORTED BY
                        statement = "\n    " + self.statement_converter(supported_by[0], 1,self.space_count) + "\n"
                        statement += "    " + self.statement_converter(supported_by[1], 2,self.space_count)
                        result += statement

                        inner_rule = self._get_rule(supported_by[1])
                        if len(inner_rule.supported_by) > 0:
                            self.space_count += 1;
                            result += self.kb_explain(inner_rule)
                            self.space_count -= 1;

                return result




        # sample is a RULE
        elif isinstance(fact_or_rule, Rule):
            # Rule not exist in KB
            if fact_or_rule not in self.rules: return "Rule is not in the KB"
            else:
                # get the right rule and convert
                rule = self._get_rule(fact_or_rule)
                statement = self.statement_converter(rule,2,self.space_count)

                if len(rule.supported_by) >0:
                    for supported_by in rule.supported_by:
                        result = "\n" + self.statement_converter("", 0, self.space_count)  # +SUPPORTED BY
                        statement = "\n    " + self.statement_converter(supported_by[0], 1, self.space_count) + "\n"
                        statement += "    " + self.statement_converter(supported_by[1], 2, self.space_count)
                        result += statement

                        inner_rule = self._get_rule(supported_by[1])
                        if len(inner_rule.supported_by) > 0:
                            self.space_count += 1;
                            result += self.kb_explain(inner_rule)
                            self.space_count -= 1;
                return result






        else: return False;

    def statement_converter(self, fact_or_rule, type, space_count):
        if type == 0: return "    "*space_count + "  " + "SUPPORTED BY";
        if type == 1:
            result = "fact: " + str(fact_or_rule.statement)

        elif type == 2:
            lhs_length = len(fact_or_rule.lhs)
            if lhs_length == 0:
                lhs = str(fact_or_rule.lhs);
            else:
                lhs = str(fact_or_rule.lhs[0])
                for ind,item in enumerate(fact_or_rule.lhs[1:]):
                    lhs += ", " + str(item)

            rhs = str(fact_or_rule.rhs)
            result ="rule: " + "(" + lhs + ")" + " -> " + rhs

        if fact_or_rule.asserted == True: result += " ASSERTED";
        return "    "*space_count + result



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
        # Implementation goes here
        # Not required for the extra credit assignment
        # match LHS and fact
        match_result = match(fact.statement, rule.lhs[0])

        # successfully match a LHS and a Rule
        # which means a new rule or fact can be generate
        if match_result != False:

            # if LHS only have one statement, then it is a new fact
            if len(rule.lhs) == 1:
                # in this condition, no new rule will generate
                fact_add = Fact(instantiate(rule.rhs, match_result))

                # modify the support area
                fact_add.asserted = False
                # add supported_by rule and facts
                fact_add.supported_by.append([fact, rule])

                # merge supports_fact and rules
                fact.supports_facts.append(fact_add)
                rule.supports_facts.append(fact_add)

                # add the new fact and modified rule
                kb.kb_add(fact_add)

            elif len(rule.lhs) > 1:
                # a new rule can be generated
                rule_add = copy.deepcopy(rule)
                rule_add.lhs = []
                rule_add.rhs = []

                # LHS
                for statements in rule.lhs[1:]:
                    new_statement = instantiate(statements, match_result)
                    rule_add.lhs.append(new_statement)
                # RHS
                rule_add.rhs = instantiate(rule.rhs, match_result)

                rule_add.asserted = False
                # modify the support area
                # merge supported_by
                rule_add.supported_by.append([fact, rule])

                # merge supports_rule
                fact.supports_rules.append(rule_add)
                rule.supports_rules.append(rule_add)

                # add the new rule and modified fact
                kb.kb_add(rule_add)