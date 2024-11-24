import random
from grammar import *
from nltk import Nonterminal

# Convert plaintext to binary
def text_to_binary(message):
    """Convert plaintext to binary representation."""
    binary_message = ""
    for char in message:
        # Convert each character to an 8-bit binary string and add it to the result
        binary_message += f"{ord(char):08b}"
    return binary_message

# Split binary into chunks
def binary_to_chunks(binary, chunk_size=4):
    """Split binary string into chunks of specified size."""
    chunks = []
    for i in range(0, len(binary), chunk_size):
        chunks.append(binary[i:i + chunk_size])
    return chunks

# Map binary chunks to grammar rules
def map_chunks_to_rules(chunk, rule_mapping):
    """Map binary chunks to grammar rules."""
    prefix = {
        0: "A", 1: "N", 2: "V", 3: "ADV", 4: "PRON", 5: "DET", 6: "PREP"
    }
    if len(chunk) < 4:
        chunk = chunk.ljust(4, '0')  # Pad with zeros if chunk is too short
    
    try:
        category = int(chunk[:2], 2)
        rule_key = f"{chunk[2:]}{prefix[category]}"
        return rule_mapping.get(rule_key, "")
    except KeyError:
        print(f"Error: Could not map chunk '{chunk}' to a rule.")
        return ""

# Generate a sentence using the grammar
def generate_sentence(grammar, mapped_words, lhs_to_replace_list):
    root = Nonterminal("S")  # Start symbol
    sentence = []

    def expand(symbol, replace_idx=[0]):
        if str(symbol) in lhs_to_replace_list:  # Replace with mapped word
            sentence.append(mapped_words[replace_idx[0]])
            replace_idx[0] += 1
            return

        productions = [prod for prod in grammar.productions(lhs=symbol)]
        if not productions:  # Terminal symbol
            sentence.append(str(symbol))
            return

        chosen_prod = random.choice(productions)
        for rhs_symbol in chosen_prod.rhs():
            expand(rhs_symbol, replace_idx)

    expand(root)
    return " ".join(sentence)

# Encode plaintext into steganographic text
def encode_message(message, rule_mapping, grammar):
    binary_message = text_to_binary(message)
    print(f"Binary Message: {binary_message}")  # Debug output
    
    chunks = binary_to_chunks(binary_message, chunk_size=4)
    print(f"Binary Chunks: {chunks}")  # Debug output

    mapped_rules = [map_chunks_to_rules(chunk, rule_mapping) for chunk in chunks]
    print(f"Mapped Rules: {mapped_rules}")  # Debug output

    sentences = []
    for rule in mapped_rules:
        if not rule:  # Skip invalid mappings
            continue
        lhs, rhs = rule.split(" -> ")
        mapped_words = [rhs.strip("'")]
        sentence = generate_sentence(grammar, mapped_words, [lhs])
        sentences.append(sentence)

    return " ".join(sentences)

# Main function
def main():
    grammar = define_grammar()
    rule_mapping = define_rule_mapping()

    text = "hi"
    print(f"Original Message: {text}")
    encoded_text = encode_message(text, rule_mapping, grammar)
    print(f"Encoded Text: {encoded_text}")

if __name__ == "__main__":
    main()




# # Convert plaintext to binary
# def text_to_binary(message):
#     """Convert plaintext to binary representation."""
#     binary_message = ""
#     for char in message:
#         # Convert each character to an 8-bit binary string and add it to the result
#         binary_message += f"{ord(char):08b}"
#     return binary_message


# def binary_to_chunks(binary, chunk_size=2):
#     """Split binary string into chunks of specified size."""
#     chunks = []
#     for i in range(0, len(binary), chunk_size):
#         # Take a slice of the binary string of length 'chunk_size' and append it
#         chunks.append(binary[i:i + chunk_size])
#     return chunks


# def map_chunks_to_rules(chunks, rule_mapping):
#     """Map binary chunks to grammar rules."""
#     mapped_rules = []
#     for chunk in chunks:
#         if chunk in rule_mapping:
#             # Append the corresponding rule to the list if the chunk is in the mapping
#             mapped_rules.append(rule_mapping[chunk])
#     return mapped_rules

# # def generate_sentence(grammar, mapped_word, lhs_to_replace):
# #     """
# #     Generate a sentence by expanding the grammar recursively, using the mapped word for a specific LHS.
    
# #     Parameters:
# #     - grammar: The context-free grammar (CFG).
# #     - mapped_word: The word (RHS) mapped from binary.
# #     - lhs_to_replace: The grammar symbol (LHS) to replace with the mapped word.
    
# #     Returns:
# #     - str: A generated sentence.
# #     """
# #     # Start with the grammar's root symbol (e.g., "S")
# #     root = Nonterminal("S")
# #     sentence = []

# #     # Recursive function to expand symbols
# #     def expand(symbol):
# #         if symbol == lhs_to_replace:  # Insert the mapped word when matching the LHS
# #             sentence.append(mapped_word)
# #             return

# #         # Find all productions for the current symbol
# #         productions = [prod for prod in grammar.productions(lhs=symbol)]
# #         if not productions:  # If it's a terminal, add it to the sentence
# #             sentence.append(str(symbol))
# #             return

# #         # Randomly choose one production to expand
# #         chosen_prod = random.choice(productions)
# #         for rhs_symbol in chosen_prod.rhs():  # Expand all RHS symbols
# #             expand(rhs_symbol)

# #     # Begin expansion from the root
# #     expand(root)
# #     return " ".join(sentence)



# # Encode a plaintext message into steganographic text
# # def encode_message(message, rule_mapping, grammar):
# #     """Encode a plaintext message into steganographic text."""
# #     # Convert to binary and split into 2-bit chunks
# #     binary_message = text_to_binary(message)
# #     chunks = binary_to_chunks(binary_message, chunk_size=2)

# #     # Map chunks to grammar rules
# #     mapped_rules = map_chunks_to_rules(chunks, rule_mapping)

# #     # Generate sentences dynamically
# #     sentences = []
# #     for rule in mapped_rules:
# #         lhs, rhs = rule.split(" -> ")
# #         rhs_word = rhs.strip("'")

# #         # Generate a sentence starting from the grammar's root symbol (e.g., "S")
# #         sentence = generate_sentence(grammar, rhs_word, Nonterminal(lhs))
# #         sentences.append(sentence)

# #     return " ".join(sentences)

# def generate_sentence(grammar, mapped_words, lhs_to_replace_list):
#     """
#     Generate a sentence by expanding the grammar recursively, using multiple mapped words.
    
#     Parameters:
#     - grammar: The context-free grammar (CFG).
#     - mapped_words: A list of words (RHS) mapped from binary.
#     - lhs_to_replace_list: A list of grammar symbols (LHS) to replace with the mapped words.
    
#     Returns:
#     - str: A generated sentence.
#     """
#     root = Nonterminal("S")
#     sentence = []

#     # Recursive function to expand symbols
#     def expand(symbol, replace_idx=[0]):
#         if symbol in lhs_to_replace_list:  # Insert the next mapped word
#             sentence.append(mapped_words[replace_idx[0]])
#             replace_idx[0] += 1
#             return

#         # Find all productions for the current symbol
#         productions = [prod for prod in grammar.productions(lhs=symbol)]
#         if not productions:  # If it's a terminal, add it to the sentence
#             sentence.append(str(symbol))
#             return

#         # Randomly choose one production to expand
#         chosen_prod = random.choice(productions)
#         for rhs_symbol in chosen_prod.rhs():  # Expand all RHS symbols
#             expand(rhs_symbol, replace_idx)

#     # Begin expansion from the root
#     expand(root)
#     return " ".join(sentence)



# def encode_message(message, rule_mapping, grammar):
#     """Encode a plaintext message into steganographic text using the CFG."""
#     # Step 1: Convert message to binary
#     binary_message = text_to_binary(message)

#     # Step 2: Split binary into 4-bit chunks (2 pairs of 2 bits)
#     chunks = binary_to_chunks(binary_message, chunk_size=4)  # Use larger chunks for compact sentences

#     # Step 3: Map binary chunks to grammar rules
#     mapped_rules = [map_chunks_to_rules(chunk[:2], rule_mapping) + map_chunks_to_rules(chunk[2:], rule_mapping) for chunk in chunks]

#     # Step 4: Generate sentences dynamically using the grammar
#     sentences = []
#     for rules in mapped_rules:
#         lhs_list, rhs_list = zip(*(rule.split(" -> ") for rule in rules))
#         mapped_words = [rhs.strip("'") for rhs in rhs_list]

#         # Generate a sentence starting from the grammar's root symbol (e.g., "S")
#         sentence = generate_sentence(grammar, mapped_words, lhs_list)
#         sentences.append(sentence)

#     return " ".join(sentences)



# def main():
#     grammar = define_grammar()
#     rule_mapping = define_rule_mapping()

#     # Input plaintext message
#     text = "hi"

#     # Encode the message
#     print(f"Original Message: {text}")
#     encoded_text = encode_message(text, rule_mapping, grammar)
#     print(f"Encoded Text: {encoded_text}")

# if __name__ == "__main__":
#     main()