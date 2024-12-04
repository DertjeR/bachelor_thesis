import random
from grammar_simplified import *
from collections import deque

def text_to_binary(message):
    """_summary_

    Args:
        message (_type_): _description_

    Returns:
        _type_: _description_
    """
    binary_message = ''.join(f"{ord(char):08b}" for char in message)
    binary_chunks = [binary_message[i:i + 2] for i in range(
        0, len(binary_message), 2)]  # 2-bit chunks
    print(f"Binary Chunks: {binary_chunks}")  # For debugging purposes

    return binary_chunks

def generate_sentence(symbol):
    """_summary_

    Args:
        symbol (_type_): _description_

    Returns:
        _type_: _description_
    """
    # If symbol is a terminal not in CFG, return a list containing itself
    if symbol not in CFG:
        return [symbol]  # Terminal is returned as a whole symbol in a list

    # Choose a random production rule for the symbol
    production = random.choice(CFG[symbol])

    # Recursively generate the structure for each part of the production rule
    structure = []
    for part in production:
        structure.extend(generate_sentence(part))  # Extend the list with the parts

    return structure

def equal_length(binary_values, sentence_structure):
    while len(binary_values) > len(sentence_structure):
        sentence_structure.extend(generate_sentence("S"))
    
    # TODO when sentence structure > pick random words that fit in 

    return sentence_structure

def ciphertext(binary_chunks, sentence_structure):
    ciphertext = []
    sents_structure = deque(sentence_structure)
    binary_values = deque(binary_chunks)

    while binary_values and sents_structure:
        word_type = sents_structure.popleft()
        binary_value = binary_values.popleft()

        if word_type == 'Det':
            ciphertext.append(det.get(binary_value, '?'))
        elif word_type == 'N':
            ciphertext.append(n.get(binary_value, '?'))
        elif word_type == 'Pron':
            ciphertext.append(pron.get(binary_value, '?'))
        elif word_type == 'Adj':
            ciphertext.append(adj.get(binary_value, '?'))
        elif word_type == 'V':
            ciphertext.append(v.get(binary_value, '?'))
        elif word_type == 'Adv':
            ciphertext.append(adv.get(binary_value, '?'))
        elif word_type == 'Prep':
            ciphertext.append(prep.get(binary_value, '?'))
        else:
            ciphertext.append('?')

    # Check for leftovers and handle them if necessary
    if binary_values:
        print("Warning: Leftover binary values:", list(binary_values))
    if sents_structure:
        print("Warning: Leftover sentence structure:", list(sents_structure))

    return ciphertext


def main():
    message = "hello"
    binary_values = text_to_binary(message)
    sentence_structure = generate_sentence("S")
    equal_length_sentence = equal_length(binary_values, sentence_structure)
    stego = ciphertext(binary_values, equal_length_sentence)

    encoded_message = ""
    for word in stego:
        encoded_message += word + " "

    print(f"Encoded message: {encoded_message}")

if __name__ == "__main__":
    main()


