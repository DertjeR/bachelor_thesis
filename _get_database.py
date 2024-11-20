import gzip
from typing import List
from lxml import etree

def make_database(gz_file) -> List[str]:
    abstracts_list = []

    # Set the maximum number of abstracts to collect to increase efficiency
    max_abstracts = 20

    # Open the gzipped file and parse with lxml
    with gzip.open(gz_file, "rb") as f:
        for _, elem in etree.iterparse(f, tag="doc"):
            abstract = elem.find("abstract")
            if abstract is not None and abstract.text:
                abstracts_list.append(abstract.text.strip())

            if len(abstracts_list) >= max_abstracts:
                break

            elem.clear()

    # For test purposes
    for abstract in abstracts_list:
        print(abstract, '\n')
    
    return abstracts_list
