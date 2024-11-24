import sys
from typing import Dict, List
from bachelor_thesis.first_approach.word_types_old import *
from bachelor_thesis.first_approach.sentence_structures import *
from bachelor_thesis.first_approach._get_database import *
from collections import deque


def retreive_first_sentence(texts: List[str]) -> str:
    """Get list of all messages and retreive the first sentence.

    Args:
        texts (List[str]): _description_

    Returns:
        str: soure text
    """
    pass

def split_at_140(original_text: str) -> str:
    """check if first sentence is > 140 chacters, if so -> split at 140 char.

    Args:
        original_text (str): _description_

    Returns:
        str: small enough source text
    """
    pass

def remove_stopwords(small_text: str) -> str:
    """Remove all the stopwords, such as articles.

    Args:
        small_text (str): _description_

    Returns:
        str: compact source text
    """
    pass

def make_lowercase(compact_text: str) -> str:
    """Make all characters lowercase.

    Args:
        compact_text (str): _description_

    Returns:
        str: lowercase source text
    """
    pass

def remove_special_chars(lowercase_text: str) -> str:
    """Remove all characters that are not a space or [a-z].

    Args:
        lowercase_text (str): _description_

    Returns:
        str: clean source text, completely preprocessed
    """
    pass

def preprocess(texts: List[str]) -> str:
    sentence = retreive_first_sentence(texts)
    max_140 = split_at_140(sentence)
    compact_text = remove_stopwords(max_140)
    lowercase_text = make_lowercase(compact_text)
    clean_text = remove_special_chars(lowercase_text)

    return clean_text

def char_to_octal(source_text: str) -> List[int]:
    octal_nums = []
    for char in source_text:
        ascii_num = ord(char)
        octal_num = int(oct(ascii_num)[2:])
        octal_nums.append(octal_num)
    
    return octal_nums

def get_cipher_text(sents_structure: List[str], n: Dict[int, str], s: Dict[int, str],
              v: Dict[int, str], adj: Dict[int, str], octal_values: List[int]):
    """_summary_

    Args:
        sents_structure (List[str]): _description_
        n (Dict[int, str]): _description_
        s (Dict[int, str]): _description_
        v (Dict[int, str]): _description_
        adj (Dict[int, str]): _description_
        octal_values (List[int]): _description_

    Returns:
        _type_: _description_
    """
    cipher_text_list = []
    sents_structure = deque(sents_structure)
    octal_values = deque(octal_values)

    while len(octal_values) != 0:
        word_type = sents_structure.popleft()  # Get current word type
        octal_value = octal_values.popleft()  # Get current octal value

        if word_type == 'nouns':
            cipher_text_list.append(n.get(octal_value, '?'))  # Use `get` to avoid KeyErrors
        elif word_type == 'subjects':
            cipher_text_list.append(s.get(octal_value, '?'))
        elif word_type == 'verbs':
            cipher_text_list.append(v.get(octal_value, '?'))
        elif word_type == 'adjectives':
            cipher_text_list.append(adj.get(octal_value, '?'))
        else:
            error = '?'

    return cipher_text_list

def main():
    file = "database.xml.gz"
    messages = make_database(file)
    clean_text = preprocess(messages)
    octal_chars = char_to_octal(clean_text)

    cipher_text = get_cipher_text(simple_text_structure, nouns, subjects,
                            verbs, adjectives, octal_chars)

    return cipher_text

string = "banana"
print(char_to_octal(string))
