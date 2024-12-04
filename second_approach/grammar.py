from nltk import CFG

# Define the grammar
def define_grammar():
    return CFG.fromstring("""
        S -> NP VP
        NP -> Det N | Pron | Det Adj N
        VP -> V NP | V Adv | VP PP
        PP -> Prep NP
        Det -> 'de' | 'een'
        Adj -> 'nieuwe' | 'grote' | 'mooie' | 'oude'
        N -> 'kerk' | 'bibliotheek' | 'school' | 'bioscoop'
        Pron -> 'hij' | 'zij' | 'Jan' | 'Emma'
        V -> 'loopt' | 'sluipt' | 'rent' | 'springt'
        Adv -> 'snel' | 'dichtbij' | 'vaak' | 'graag'
        Prep -> 'naar' | 'naast' | 'op' | 'in'
    """)

# Define the binary-to-rule mapping
def define_rule_mapping():
    return {
        "00A": "Adj -> 'nieuwe'",
        "01A": "Adj -> 'grote'",
        "10A": "Adj -> 'mooie'",
        "11A": "Adj -> 'oude'",
        "00N": "N -> 'kerk'",
        "01N": "N -> 'bibliotheek'",
        "10N": "N -> 'school'",
        "11N": "N -> 'bioscoop'",
        "00V": "V -> 'loopt'",
        "01V": "V -> 'sluipt'",
        "10V": "V -> 'rent'",
        "11V": "V -> 'springt'",
        "00ADV": "Adv -> 'snel'",
        "01ADV": "Adv -> 'dichtbij'",
        "10ADV": "Adv -> 'vaak'",
        "11ADV": "Adv -> 'graag'",
        "00PRON": "Pron -> 'hij'",
        "01PRON": "Pron -> 'zij'",
        "10PRON": "Pron -> 'Jan'",
        "11PRON": "Pron -> 'Emma'",
        "00DET": "Det -> 'de'",
        "01DET": "Det -> 'een'",
        "10DET": "Det -> 'de'",
        "11DET": "Det -> 'een'",
        "00PREP": "Prep -> 'naar'",
        "01PREP": "Prep -> 'naast'",
        "10PREP": "Prep -> 'op'",
        "11PREP": "Prep -> 'in'"
    }

from nltk import CFG, Nonterminal

# Define a simple grammar
grammar = CFG.fromstring("""
        S -> NP VP
        NP -> Det N | Pron | Det Adj N
        VP -> V NP | V Adv | VP PP
        PP -> Prep NP
        Det -> 'de' | 'een'
        Adj -> 'nieuwe' | 'grote' | 'mooie' | 'oude'
        N -> 'kerk' | 'bibliotheek' | 'school' | 'bioscoop'
        Pron -> 'hij' | 'zij' | 'Jan' | 'Emma'
        V -> 'loopt' | 'sluipt' | 'rent' | 'springt'
        Adv -> 'snel' | 'dichtbij' | 'vaak' | 'graag'
        Prep -> 'naar' | 'naast' | 'op' | 'in'
    """)

# # Get productions for the start symbol
# start_symbol = Nonterminal("VP")
# productions = grammar.productions(lhs=start_symbol)

# print(grammar)

# for prod in productions:
#     print(f"Production: {prod}")
#     print(f"RHS: {prod.rhs()}")
