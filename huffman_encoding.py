import json
from collections import Counter
from queue import PriorityQueue
from typing import Dict, Tuple
import random
# from huffman_encoding import huffman_encode, huffman_decode, dynamic_mapping

class HuffmanNode:
    def __init__(self, char: str, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text: str) -> HuffmanNode:
    """Build a Huffman tree for the given text.

    Args:
        text (str): The text to analyze and build a Huffman tree for.

    Returns:
        HuffmanNode: The root of the constructed Huffman tree.
    """
    freq = Counter(text)
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
    """Generate Huffman codes for the characters in the tree.

    Args:
        node (HuffmanNode): The root node of the Huffman tree.
        prefix (str, optional): The current prefix for codes. Defaults to "".
        codebook (Dict[str, str], optional): A dictionary to store the generated codes. Defaults to None.

    Returns:
        Dict[str, str]: A dictionary mapping characters to their Huffman codes.
    """
    if codebook is None:
        codebook = {}
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)

    return codebook


def huffman_encode(text: str) -> Tuple[str, Dict[str, str]]:
    """Encode a text using Huffman coding.

    Args:
        text (str): The text to encode.

    Returns:
        Tuple[str, Dict[str, str]]: A tuple containing the Huffman-encoded binary string and the codebook.
    """
    tree = build_huffman_tree(text)
    codebook = generate_huffman_codes(tree)
    huffman_encoded = ''.join(codebook[char] for char in text)

    return huffman_encoded, codebook


def huffman_decode(encoded_text: str, codebook: Dict[str, str]) -> str:
    """Decode a Huffman-encoded string.

    Args:
        encoded_text (str): The binary string encoded with Huffman coding.
        codebook (Dict[str, str]): The Huffman codebook used for encoding.

    Returns:
        str: The original decoded text.
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


def dynamic_mapping(seed: int) -> Dict[str, str]:
    """Generate a dynamic mapping for invisible characters based on a seed.

    Args:
        seed (int): The seed for the random number generator.

    Returns:
        Dict[str, str]: A dictionary mapping bits ('0', '1') to zero-width characters.
    """
    random.seed(seed)
    invisible_characters = ['\u200C', '\u200B']  # ZWNJ and ZWSP
    random.shuffle(invisible_characters)

    return {'0': invisible_characters[0], '1': invisible_characters[1]}

def encode_message(text: str, message: str, inv_char: Dict[str, str]) -> str:
    """Encode a hidden message and the Huffman codebook into cover text using invisible characters.

    Args:
        text (str): The cover text to embed the message into.
        message (str): The hidden message to encode.
        inv_char (Dict[str, str]): A dictionary mapping bits ('0', '1') to invisible characters.

    Returns:
        str: The stego text with the embedded hidden message and Huffman codebook.
    """
    # Huffman encode the message
    huffman_encoded, codebook = huffman_encode(message)
    print(codebook)

    # Serialize the Huffman codebook
    serialized_codebook = json.dumps(codebook)

    # Convert serialized codebook to binary and encode it
    codebook_binary = ''.join(format(ord(char), '08b') for char in serialized_codebook)
    encoded_codebook = ''.join(inv_char[bit] for bit in codebook_binary)

    # Encode the hidden message
    encoded_message = ''.join(inv_char[bit] for bit in huffman_encoded)

    # Combine the cover text, encoded codebook, and encoded message
    return text + encoded_codebook + '\u200D' + encoded_message  # Use '\u200D' (Zero-Width Joiner) as a separator


def decode_message(encoded_text: str, inv_char: Dict[str, str]) -> str:
    """Decode a hidden message and retrieve the Huffman codebook from stego text.

    Args:
        encoded_text (str): The stego text containing the hidden message and Huffman codebook.
        inv_char (Dict[str, str]): A dictionary mapping bits ('0', '1') to invisible characters.

    Returns:
        str: The decoded hidden message.
    """
    # Split the encoded text into the codebook and message parts
    invisible_part = ''.join(c for c in encoded_text if c in inv_char.values() or c == '\u200D')
    encoded_codebook, encoded_message = invisible_part.split('\u200D')

    # Decode the Huffman codebook
    inverted_mapping = {v: k for k, v in inv_char.items()}
    codebook_binary = ''.join(inverted_mapping[c] for c in encoded_codebook)
    serialized_codebook = ''.join(chr(int(codebook_binary[i:i+8], 2)) for i in range(0, len(codebook_binary), 8))
    codebook = json.loads(serialized_codebook)

    # Decode the hidden message
    huffman_encoded = ''.join(inverted_mapping[c] for c in encoded_message)
    decoded_message = huffman_decode(huffman_encoded, codebook)

    return decoded_message


def main():
    # Load the cover text
    file_path = "cover_texts/long_covertext.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        cover_text = file.read()

    # Hidden message
    hidden_message = "hoi"

    # Generate dynamic mapping
    seed = 42
    invisible_characters = dynamic_mapping(seed)
    print(invisible_characters)

    # Encode the message
    stego_text = encode_message(cover_text, hidden_message, invisible_characters)

    # Decode the message
    decoded_message = decode_message(stego_text, invisible_characters)

    # Output results
    # print("Cover text:", cover_text)
    # print("Stego text:", stego_text)
    print("Decoded message:", decoded_message)

    if hidden_message == decoded_message:
        print("Message successfully hidden and retrieved!")
    else:
        print("Error: Message not successfully hidden and retrieved.")


if __name__ == "__main__":
    main()
