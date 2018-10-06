# Screenplay Parser

This is a screenplay parser that extracts dialogues between characters. However it extracts the dialogues **if the second character has a [paranthetical](http://www.screenwriting.info/08.php)**. The scripts are crawled from http://www.imsdb.com/ . 

## Getting Started

1. Run scrapy : Go to brickset-scraper folder and run this in your terminal: 

		scrapy runspider scraper.py

	This will generate "all_movies.json" file in the same folder.
    
1. Copy all_movies.json to html_crawlers folder. Run "json_parser.py" through jupyter notebook. This will read "all_movies.json" and will create "all_name_script.txt". This new txt file has a movie name and a link to its script for each movie in the json file.

1. Run "html_list_parser.ipynb" . This will read "all_name_script.txt" and will generate "All_out.txt". This file has all the relevant dialogues from the movie scripts.


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

