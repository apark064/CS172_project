# CS172 Final Project

Team members: Abraham Park, Jorge Ruiz, Kevin To, Masashi Yamaguchi

Programming Language: Python, HTML

## Description
Super Duper Crawler creates a term-base index of website and returns relevant documents to the given query from the index.
This crawler can be used in .edu webpages and wikipedia

## Usage

To run the program, run the following commands
``
python app.py
``
and type "seed URL" and "query" on the provided link

## Dependencies
Install the following
```pip3 install BeautifulSoup```
```pip3 install requests```
```pip3 install elasticsearch```
```pip3 install pandas```
```pip3 install flask```
```pip3 install lxml```

## Extensions

- Web-based interface 
  
- Priority Queue by last updated time : sort_list_by_time()
    it can take more time to get the output but it is very useful for multi-threaded nodes