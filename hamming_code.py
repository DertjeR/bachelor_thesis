#encoding with invisible characters, huffman ancoding,
#hamming code and dynamic mapping

from collections import Counter
from queue import PriorityQueue
from typing import Dict, Tuple
import random


# For better payload capacity
class HuffmanNode:
    """Node class for representing a character and its frequency in a Huffman tree.

    Attributes:
        char (str): The character represented by the node. None for non-leaf nodes.
        freq (int): The frequency of the character.
        left (HuffmanNode): The left child node.
        right (HuffmanNode): The right child node.
    """

    def __init__(self, char: str, freq: int):
        """Initialize a HuffmanNode.

        Args:
            char (str): The character represented by the node.
            freq (int): The frequency of the character.
        """
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        """Comparison operator for priority queue placement.

        Args:
            other (HuffmanNode): The other node to compare.

        Returns:
            bool: True if this node's frequency is less than the other node's.
        """
        return self.freq < other.freq

def build_huffman_tree(hidden_message: str) -> HuffmanNode:
    """Build a Huffman tree for the given message.

    Args:
        hidden_message (str): The message to encode.

    Returns:
        HuffmanNode: The root of the Huffman tree.
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

def generate_huffman_codes(node: HuffmanNode, prefix: str = "", codebook: Dict[str, str] = None) -> Dict[str, str]:
    """Generate Huffman codes for each character.

    Args:
        node (HuffmanNode): The root node of the Huffman tree.
        prefix (str, optional): The current prefix for codes. Defaults to "".
        codebook (Dict[str, str], optional): A dictionary to store character codes. Defaults to None.

    Returns:
        Dict[str, str]: The mapping of characters to their Huffman codes.
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
    """Encode a message using Huffman coding.

    Args:
        hidden_message (str): The message to encode.

    Returns:
        Tuple[str, Dict[str, str]]: The Huffman-encoded binary string and the codebook.
    """
    tree = build_huffman_tree(hidden_message)
    codebook = generate_huffman_codes(tree)
    huffman_encoded = ''.join(codebook[char] for char in hidden_message)

    return huffman_encoded, codebook

def huffman_decode(encoded_text: str, codebook: Dict[str, str]) -> str:
    """Decode a Huffman-encoded string.

    Args:
        encoded_text (str): The Huffman-encoded binary string.
        codebook (Dict[str, str]): The mapping of characters to codes.

    Returns:
        str: The decoded message.
    """
    reverse_codebook = {v: k for k, v in codebook.items()}
    decoded_text = ""
    buffer = ""

    for bit in encoded_text:
        buffer += bit
        if buffer in reverse_codebook:
            decoded_text += reverse_codebook[buffer]
            buffer = ""

    return decoded_text

def hamming_encode(data: str) -> str:
    """Encode a binary string using Hamming code.

    Args:
        data (str): The binary string to encode.

    Returns:
        str: The Hamming-encoded binary string.
    """
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
    """Decode a binary string encoded with Hamming code.

    Args:
        data (str): The Hamming-encoded binary string.

    Returns:
        str: The original binary string with errors corrected.
    """
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
        print(f"Error detected at position: {error_pos}")
        error_pos -= 1
        data = data[:error_pos] + ('1' if data[error_pos] == '0' else '0') + data[error_pos + 1:]

    original_data = ''
    for i in range(1, n + 1):
        if i & (i - 1) != 0:
            original_data += data[i - 1]

    return original_data

def dynamic_mapping(seed: int) -> Dict[str, str]:
    """Generate a dynamic mapping for invisible characters based on a seed.

    Args:
        seed (int): The seed for the random number generator.

    Returns:
        Dict[str, str]: A dictionary mapping bits ('0', '1') to invisible characters.
    """
    random.seed(seed)
    invisible_characters = ['\u200C', '\u200B']
    random.shuffle(invisible_characters)

    return {'0': invisible_characters[0], '1': invisible_characters[1]}

def encode_message(cover_text: str, hidden_message: str, inv_chars: Dict[str, str]) -> Tuple[str, Dict[str, str]]:
    """Encode a hidden message into a cover text.

    Args:
        cover_text (str): The cover text to embed the message into.
        hidden_message (str): The message to hide.
        inv_chars (Dict[str, str]): Mapping of bits to invisible characters.

    Returns:
        Tuple[str, Dict[str, str]]: The stego object and the Huffman codebook.
    """
    huffman_encoded, codebook = huffman_encode(hidden_message)
    hamming_encoded = hamming_encode(huffman_encoded)
    stego_object = cover_text + ''.join(inv_chars[bit] for bit in hamming_encoded)

    return stego_object, codebook

def decode_message(stego_object: str, inv_chars: Dict[str, str], codebook: Dict[str, str]) -> str:
    """Decode a hidden message from a stego object.

    Args:
        stego_object (str): The text containing the hidden message.
        inv_chars (Dict[str, str]): Mapping of bits to invisible characters.
        codebook (Dict[str, str]): The Huffman codebook.

    Returns:
        str: The decoded hidden message.
    """
    invisible_chars = ''.join(c for c in stego_object if c in inv_chars.values())
    inverted_mapping = {v: k for k, v in inv_chars.items()}
    hamming_encoded = ''.join(inverted_mapping[c] for c in invisible_chars)
    huffman_encoded = hamming_decode(hamming_encoded)
    decoded_hidden_message = huffman_decode(huffman_encoded, codebook)

    return decoded_hidden_message

def main():
    file_path = "input1.txt"  # TODO: Add command-line argument for file input
    with open(file_path, "r", encoding="utf-8") as file:
        cover_text = file.read()

    hidden_message = "Hallootjes woehoeeeeeeeee!"  # TODO: Add command-line argument for hidden message input

    seed = 42  # TODO: Replace with user input or system-generated random seed
    invisible_characters = dynamic_mapping(seed)

    stego_object, codebook = encode_message(cover_text, hidden_message, invisible_characters)
    decoded_hidden_message = decode_message(stego_object, invisible_characters, codebook)

    print("Cover text:", cover_text)
    print("Stego text:", stego_object)
    print("Codebook:", codebook)
    print("Decoded message:", decoded_hidden_message)


if __name__ == "__main__":
    main()
