# Screenplay Parser

This is a screenplay parser that extracts dialogues between characters. However it extracts the dialogues **if the second character has a [paranthetical](https://writebetterscripts.com/parenthetical-script/)**. The scripts are crawled from http://www.imsdb.com/ . 

## Getting Started

1. Run scrapy : Go to brickset-scraper folder and run this in your terminal: 

		scrapy runspider scraper.py --output=data/names_links.json

	This will generate `data/names_links.json`.
    
1. Run "json_parser.py" via terminal command "python json_parser.py names_links.json". This will read "names_links.json" and will create "all_name_script.txt". This new txt file has a movie name and a link to its script for each movie in the json file. Note that each script takes 1-2 seconds.

1. Run "html_list_parser.py" . This will read "all_name_script.txt" and will generate "all_dialogues.txt". This file has all the relevant dialogues from the movie scripts.


### Prerequisites

You need to have 

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
- [Scraper]()
- Python 3 or above
- [Jupyter Notebook](http://jupyter.org/install.html)

## Authors

**Kamil Veli Toraman**:  [kvtoraman](https://github.com/kvtoraman)

## License

There is no licence for now. You can use as you please. This code tries to have a rule-based algorithm for movie scripts. If you have a better way, please inform me :)

## Acknowledgments

* This is a result of a 2 month internship in Data Science Lab, Kaist. 

