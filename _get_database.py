import pandas as pd
import nltk
import spacy
import re
import json
from typing import Dict, List


def read_file(file_name: json) -> List[str]:
    
    nlp = spacy.load("en_core_web_sm")
    texts = {}
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            json_obj = json.loads(line.strip())
            text = json_obj.get('text', '')
            doc = nlp(text)
            if doc is not None:
                texts[doc] = None

    return texts

