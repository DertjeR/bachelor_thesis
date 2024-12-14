import random
from nltk import Nonterminal
from grammar import *

# Expand grammar to produce non-terminal sequence (e.g., Det, N, V)
def expand_to_non_terminals(grammar, symbols):
    """
    Expands grammar symbols to produce a sequence of non-terminals (e.g., Det, N, V).
    Stops expansion if it encounters a terminal symbol and retains the non-terminal type.
    """
    result = []
    for symbol in symbols:
        if isinstance(symbol, Nonterminal):  # Expand only non-terminals
            result.append(symbol.symbol())  # Append the non-terminal type
            productions = grammar.productions(lhs=symbol)
            if productions:
                # Randomly choose a production and recursively expand
                chosen_production = random.choice(productions)
                result.extend(expand_to_non_terminals(grammar, chosen_production.rhs()))
    return result



# Generate a random sentence structure using non-terminals
def get_random_sentence_structure(grammar):
    start_symbol = Nonterminal("S")
    productions = grammar.productions(lhs=start_symbol)
    chosen_production = random.choice(productions)  # Random production for S
    print(f"Chosen Production: {chosen_production}")  # Debugging: Show chosen production
    structure = expand_to_non_terminals(grammar, chosen_production.rhs())
    print(f"Generated Sentence Structure (non-terminals only): {structure}")  # Debugging: Show structure

    return structure

# Convert plaintext to binary
def text_to_binary(message):
    return ''.join(f"{ord(char):08b}" for char in message)

def map_binary_to_word(binary_chunk, word_type, rule_mapping):
    """
    Map a binary chunk to a word of the given type (e.g., Det, N, V) using the rule mapping.
    """
    key = f"{binary_chunk}{word_type}"
    rule = rule_mapping.get(key)

    if rule:
        word = rule.split(" -> ")[1].strip("'")  # Extract the terminal word
        print(f"Mapped {key} -> {word}")  # Debugging: Show successful mapping
        return word
    else:
        # Fallback: Choose a random word of the correct type
        candidates = [r.split(" -> ")[1].strip("'") for k, r in rule_mapping.items() if k.endswith(word_type)]
        if candidates:
            word = random.choice(candidates)
            print(f"Fallback for {word_type}: Chose random word '{word}'")  # Debugging: Show fallback selection
            return word
        else:
            print(f"No candidates found for word type: {word_type}")  # Debugging: Show error
            return "unknown"

def generate_sentence(message, grammar, rule_mapping):
    """
    Generate a sentence based on the input message, grammar, and rule mapping.
    """
    binary_message = text_to_binary(message)
    print(f"Binary Message: {binary_message}")  # Debugging: Show binary message
    binary_chunks = [binary_message[i:i + 2] for i in range(0, len(binary_message), 2)]  # 2-bit chunks
    print(f"Binary Chunks: {binary_chunks}")  # Debugging: Show binary chunks
    sentence = []

    while binary_chunks:
        # Generate a random sentence structure from non-terminals
        sentence_structure = get_random_sentence_structure(grammar)
        print(f"Random Sentence Structure (non-terminals only): {sentence_structure}")  # Debugging: Show structure

        for word_type in sentence_structure:
            if binary_chunks:
                # Map binary chunk to a word
                binary_chunk = binary_chunks.pop(0)
                word = map_binary_to_word(binary_chunk, word_type, rule_mapping)
            else:
                # If no binary chunks left, use random fallback
                print(f"No binary chunk left for word type: {word_type}, selecting random.")  # Debugging
                word = map_binary_to_word("00", word_type, rule_mapping)
            sentence.append(word)

    return " ".join(sentence)

# Main function
def main():
    grammar = define_grammar()
    rule_mapping = define_rule_mapping()
    message = "me"

    print(f"Original Message: {message}")
    sentence = generate_sentence(message, grammar, rule_mapping)
    print(f"Generated Sentence: {sentence}")

if __name__ == "__main__":
    main()
