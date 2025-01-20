import json
from collections import Counter
from queue import PriorityQueue
from typing import Dict, Tuple
import random


# For better payload capacity
class HuffmanNode:
    def __init__(self, char: str, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(hidden_message: str) -> HuffmanNode:
    """Builds a Huffman tree for the given hidden message.

    Args:
        text (str): The message for which the Huffman tree will be built.

    Returns:
        HuffmanNode: The root node of the constructed Huffman tree.
    """
    freq = Counter(hidden_message)
    pq = PriorityQueue()

    for char, count in freq.items():
        pq.put(HuffmanNode(char, count))

    while pq.qsize() > 1:
        left = pq.get()
        right = pq.get()
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        pq.put(merged)

    return pq.get()


def generate_huffman_codes(node: HuffmanNode, prefix: str = "",
                           codebook: Dict[str, str] = None) -> Dict[str, str]:
    """Generates Huffman codes for characters based on a Huffman tree.

    Args:
        node (HuffmanNode): The root node of the Huffman tree
        prefix (str, optional): The current prefix of the binary code
            during traversal. Defaults to an empty string.
        codebook (dict, optional): A dictionary to store the generated
            codes. Defaults to None, in which case a new dictionary is created.

    Returns:
        dict: A dictionary containing characters as keys and
        their corresponding Huffman codes as values.
    """
    if codebook is None:
        codebook = {}
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)

    return codebook


def huffman_encode(hidden_message: str) -> Tuple[str, Dict[str, str]]:
    """Encodes a hidden message using Huffman coding.

    Args:
        hidden_message (str): The hidden message to be encoded

    Returns:
        Tuple[str, dict]: A tuple containing the encoded text
        as a binary string and the corresponding codebook.
    """
    tree = build_huffman_tree(hidden_message)
    codebook = generate_huffman_codes(tree)
    huffman_encoded = ''.join(codebook[char] for char in hidden_message)

    return huffman_encoded, codebook


def huffman_decode(binary_message: str, codebook: Dict[str, str]) -> str:
    """uses the given Huffman codebook to decode a binary
    string back into the original text.

    Args:
        binary_message (str): The binary string encoded using Huffman coding.
        codebook (Dict[str, str]): The Huffman codebook.

    Returns:
        str: The decoded hidden message.
    """
    reverse_codebook = {v: k for k, v in codebook.items()}
    decoded_text = ""
    buffer = ""
    for bit in binary_message:
        buffer += bit
        if buffer in reverse_codebook:
            decoded_text += reverse_codebook[buffer]
            buffer = ""

    return decoded_text


# For error handling
def hamming_encode(data: str) -> str:
    n = len(data)
    r = 0
    while (2**r < n + r + 1):
        r += 1

    hamming_code = [''] * (n + r)
    j = 0
    for i in range(1, len(hamming_code) + 1):
        if i & (i - 1) == 0:
            hamming_code[i - 1] = '0'
        else:
            hamming_code[i - 1] = data[j]
            j += 1

    for i in range(r):
        pos = 2**i
        parity = 0
        for j in range(1, len(hamming_code) + 1):
            if j & pos and hamming_code[j - 1] == '1':
                parity ^= 1
        hamming_code[pos - 1] = str(parity)

    return ''.join(hamming_code)


def hamming_decode(data: str) -> str:
    n = len(data)
    r = 0
    while (2**r < n):
        r += 1

    error_pos = 0
    for i in range(r):
        pos = 2**i
        parity = 0
        for j in range(1, n + 1):
            if j & pos and data[j - 1] == '1':
                parity ^= 1
        if parity != 0:
            error_pos += pos

    if error_pos > 0:
        error_pos -= 1
        data = data[:error_pos] + (
            '1' if data[error_pos] == '0' else '0') + data[error_pos + 1:]

    original_data = ''
    for i in range(1, n + 1):
        if i & (i - 1) != 0:
            original_data += data[i - 1]

    return original_data


# For better security
def dynamic_mapping(seed: int) -> Dict[str, str]:
    """Generate a dynamic mapping for invisible characters based on a seed.

    Args:
        seed (int): The seed for the random number generator.

    Returns:
        Dict[str, str]: A dict mapping '0' and '1' to invisible characters.
    """
    random.seed(seed)
    invisible_characters = ['\u200C', '\u200B']
    random.shuffle(invisible_characters)

    return {'0': invisible_characters[0], '1': invisible_characters[1]}


def encode_message(cover_text: str, hidden_message: str,
                   inv_chars: Dict[str, str]) -> str:
    """Encode a hidden message and the Huffman codebook into cover text
    using invisible characters and hamming code for error correction.

    Args:
        cover_text (str): The cover text to embed the hidden message into.
        hidden_message (str): The message to be hidden.
        inv_char (dict): A dictionary mapping bits ('0', '1') to
        invisible characters.

    Returns:
        str: The resulting stego object containing the hidden message.
    """
    # Huffman encode the hidden message
    huffman_encoded, codebook = huffman_encode(hidden_message)

    # Serialize the Huffman codebook
    serialized_codebook = json.dumps(codebook)

    # Convert serialized codebook to binary and encode it
    codebook_binary = ''.join(format(ord(char), '08b')
                              for char in serialized_codebook)
    encoded_codebook = ''.join(inv_chars[bit] for bit in codebook_binary)

    # Hamming encode the Huffman-encoded message and convert to inv chars
    hamming_encoded = hamming_encode(huffman_encoded)
    invisible_message = ''.join(inv_chars[bit] for bit in hamming_encoded)

    # Split cover text into words
    words = cover_text.split()
    stego_object = []
    char_index = 0

    # Distribute invisible characters between words
    for word in words:
        stego_object.append(word)
        if char_index < len(invisible_message):
            stego_object.append(invisible_message[char_index])
            char_index += 1

    # Append remaining invisible characters of the message
    if char_index < len(invisible_message):
        stego_object.append(invisible_message[char_index:])

    # Add separator and encode the serialized codebook
    separator = '\u200D'
    stego_object.append(separator)
    stego_object.append(encoded_codebook)

    return ' '.join(stego_object)


def decode_message(stego_object: str, inv_chars: Dict[str, str]) -> str:
    """Extracts the binary message from the invisible characters embedded in
    the stego object and converts it back to the original hidden message.

    Args:
        stego_object (str): The stego object containing the hidden message.
        inv_chars (dict): A dictionary mapping bits ('0', '1') to invisible
        characters.

    Returns:
        str: The decoded hidden message.
    """
    # Extract invisible characters and separator
    separator = '\u200D'
    invisible_parts = ''.join(c for c in stego_object
                              if c in inv_chars.values() or c == separator)
    encoded_message, encoded_codebook = invisible_parts.split(separator)

    # Decode the Huffman codebook
    inverted_mapping = {v: k for k, v in inv_chars.items()}
    codebook_binary = ''.join(inverted_mapping[c] for c in encoded_codebook)
    serialized_codebook = ''.join(chr(int(codebook_binary[i:i+8], 2))
                                  for i in range(0, len(codebook_binary), 8))
    codebook = json.loads(serialized_codebook)

    # Decode the hidden message
    hamming_encoded = ''.join(inverted_mapping[c] for c in encoded_message)
    huffman_encoded = hamming_decode(hamming_encoded)
    return huffman_decode(huffman_encoded, codebook)


def main():
    file_path = "cover_texts/small_covertext.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        cover_text = file.read()

    hidden_message = "Hallootjes woehoeeeeeeeee!"
    seed = 42
    invisible_chars = dynamic_mapping(seed)

    stego_object = encode_message(cover_text, hidden_message, invisible_chars)
    decoded_hidden_message = decode_message(stego_object, invisible_chars)

    print("Cover text:", cover_text)
    print("Stego text:", stego_object)
    print("Decoded message:", decoded_hidden_message)

    if hidden_message == decoded_hidden_message:
        print("Message successfully hidden and retrieved!")
    else:
        print("Error: Message not successfully hidden and retrieved.")


if __name__ == "__main__":
    main()
