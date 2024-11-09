import sys
from typing import Dict, List
from word_types import *
from sentence_structures import *


def get_message() -> str:
    pass

def split_text(original_text: str) -> str:
    pass

def remove_stopwords(small_text: str) -> str:
    pass

def make_lowercase(compact_text: str) -> str:
    pass

def remove_special_chars(lowercase_text: str) -> str:
    pass

def preprocess(message: str) -> str:
    small_text = split_text(message)
    compact_text = remove_stopwords(small_text)
    lowercase_text = make_lowercase(compact_text)
    clean_text = remove_special_chars(lowercase_text)
    return clean_text

def char_to_octal(chars: str) -> List[int]:
    octal_nums = []
    for char in chars:
        ascii_num = ord(char)
        octal_num = int(oct(ascii_num)[2:])
        octal_nums.append(octal_num)
    
    return octal_nums

def get_words(sents_structure: List[str], n: Dict[int, str],
              s: Dict[int, str], v: Dict[int, str], adj: Dict[int, str]):
    pass

def main():
    message = get_message()
    clean_text = preprocess(message)
    chars = char_to_octal(clean_text)

    cipher_text = get_words(simple_text_structure, nouns, subjects,
                            verbs, adjectives)
    
    return cipher_text

string = "banana"
print(char_to_octal(string))