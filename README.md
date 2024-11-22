# Bachelor thesis Information science
Number oriented steganography



























## Description



## Getting Started

### Dependencies

This program complies with the following requirements:
* libraries: sys, pandas, nltk, wikiextractor, wget, spacy, json, xml.etree.ElementTree, os
* python version: 3.8

### Installing <- old version
To use the program in your terminal go to your preferred repository
* Clone the program into your repository with the command ```git clone https://github.com/DertjeR/bachelor_thesis.git```
* Navigate to the program repository with the command ```cd bachelor_thesis```
* The program comes with a pre-defined database with the latest wikipedia dump of Dutch articles on november 18th 2024 at 12.05 pm.
* In the case that you want to use newer articles go to [latest wikipedia dump](https://dumps.wikimedia.org/nlwiki/latest/)
* Download the file 'nlwiki-latest-pages-articles-multistream.xml.bz2' to get the newest articles
* Remove the file containing the existing database 'dutch_database'
* Unfold all articles:
    * To save the full extracted dump and unfold it, in your terminal run ```wikiextractor nlwiki-latest-pages-articles-multistream.xml.bz2 -o dutch_database```.
    * The file will unfold into multiple .txt files that contain multiple articles each.
    * Depending on your machine, unfolding the full dump will take around 10 - 30 minutes and will return about 1 million articles.
* Unfold only a number of articles
    * To shorten the process and extract a smaller database to ensure time efficiency. When you have a size of the database that you want (check your repository) stop the unfolding process with the keyboard interrupt `Ctrl + C` on windows.


### Installing 2 <- CORRECT
abstract wikipedia file (smaller)
download on mac: curl -o /Users/dertje/Documents/Informatiekunde/Year3/thesis/bachelor_thesis/database.xml.gz https://dumps.wikimedia.org/nlwiki/latest/nlwiki-latest-abstract.xml.gz
download on windows: wget -P /Users/dertje/Documents/Informatiekunde/Year3/thesis/bachelor_thesis https://dumps.wikimedia.org/nlwiki/latest/nlwiki-latest-abstract.xml.gz

run _get_database.py to extract abstracts and output a list where each abstract is an element in the list


### Executing program
_get_database.py is used to process the text in the database that I used. If you want to use your own database (or a database that is not the same type of file), do not use _get_database.py. Instead define your own preprocess database file. Its output should be a list of strings (aka a list of messages).

* How to run the program
* Step-by-step bullets

```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Author

Dertje Roggeveen
d.j.roggeveen@student.rug.nl