"""Very simple command line interface for testing specific parts of this
package's functionality"""

import hmm_utils
import cmd_utils
import stanford_parser

counts = hmm_utils.get_transition_counts()

# Flags that note that incode should be looked for in STDIN instead of
# in a test essay file
final_score_stdin = cmd_utils.cmd_flag('--final-score', None)
parse_stdin = cmd_utils.cmd_flag('--parse', None)
score_stdin = cmd_utils.cmd_flag('--score', None)
agreement_stdin = cmd_utils.cmd_flag('--agree', None)
sentence_parse_stdin = cmd_utils.cmd_flag('--sen-token', None)
word_order_parse_stdin = cmd_utils.cmd_flag('--word-order', None)


transition_count = cmd_utils.cmd_arg('--count', None)
transition_prob = cmd_utils.cmd_arg('--prob', None)


if score_stdin or parse_stdin:
    import tree_utils
    trees = stanford_parser.parse(cmd_utils.get_stdin())
    for tree in trees:
        print tree
        if score_stdin:
            sentence_transitions = tree_utils.transitions_in_tree(tree)
            sentence_probs = []
            for transition in sentence_transitions:
                print "Transitions: %s" % (transition)
                probs = hmm_utils.prob_of_all_transitions(transition, counts, gram_size=3)
                print "Probs: %s" % (probs)
                sentence_probs += probs
            total = 1
            for prob in sentence_probs:
                total *= prob
            print "Total: %f" % (total,)
elif sentence_parse_stdin:
    import sentence_tokenizer
    sentences = sentence_tokenizer.parse_sentences(cmd_utils.get_stdin(), use_cache=False)
    print sentences
elif word_order_parse_stdin:
    import sentence_tokenizer
    import word_order
    lines = cmd_utils.get_stdin_lines()
    issues_in_text = []
    for line in lines:
        sentences = sentence_tokenizer.parse_sentences(line)
        for sentence in sentences:
            issues = word_order.issues_in_sentence(sentence, use_cache=False)
            print sentence
            print issues
            issues_in_text += issues
    print "Found %d issues" % (len(issues_in_text),)
    print "Issues: %s" % (issues_in_text,)
elif agreement_stdin:
    import agreement_utils
    text = cmd_utils.get_stdin().strip()
    agreement_utils.parse(text)
elif final_score_stdin:
    import grade_utils
    text = cmd_utils.get_stdin().strip()
    for grade_type in grade_utils.implemented_grades:
        print "%s: %d" % (grade_type, grade_utils.grade_text(text, grade_type))
elif transition_count:
    print "Count: %d" % (counts[transition_count],)
elif transition_prob:
    transitions = transition_prob.split("@")
    bottom = counts["@".join(transitions[:-1])]
    top = counts[transition_prob]
    print "Prob: (%d/%d) -> %f" % (top, bottom, float(top)/bottom)
else:
    print "Error: Nothing to test"
