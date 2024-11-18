# Bachelor thesis Information science
Number oriented steganography



























## Description



## Getting Started

### Dependencies

This program complies with the following requirements:
* libraries: sys, pandas, nltk, wikiextractor
* python version: 3.8

### Installing
To use the program in your terminal go to your preferred repository
* Clone the program to your repository with the command ```py git clone https://github.com/DertjeR/bachelor_thesis.git```
* Navigate to the program repository with the command ```py cd bachelor_thesis```
* The program comes with a pre-defined database with the latest wikipedia dump of Dutch articles on november 18th 2024 at 12.05 pm.
* * In the case that you want to use newer articles go to (latest wikipedia dump)[https://dumps.wikimedia.org/nlwiki/latest/]
* * Download the file 'nlwiki-latest-pages-articles-multistream.xml.bz2' 
* * Remove all the files in the repository 'dutch_database'
* * To save the full extracted dump and unfold it, run ```py wikiextractor nlwiki-20241101-pages-articles-multistream.xml.bz2 -o dutch_database``` in your terminal.
* * The file will unfold into multiple .txt files that contain multiple articles each.
* * Depending on your machine, unfolding the full dump will take around 10 - 30 minutes and will return about 1 million articles.
* * To shorten the process and extract a smaller database to ensure time efficiency instead of running the above command, run ```py wikiextractor nlwiki-latest-pages-articles-multistream.xml.bz2 -o dutch_database --processes 1 --max_articles 100 `` (change the maximum number of articles to your preference).


### Executing program

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