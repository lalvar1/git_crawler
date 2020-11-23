# Python Crawler
## Introduction
The crawler will print the first's page urls, specifying the owner of each page,
based on the input keywords and search pattern type.

In the case of a repository search, will also print the languages used within each repo.


Supported types are: 
- repository 
- issues
- wikis

## How to use
The crawler will take as input a dictionary, with 3 different keys corresponding to:
- keywords: list of strings to search
- proxies: list of proxies to randomly use to perform http requests
- type: pattern/element type to be searched

e.g
```python
my_input = {
"keywords": [
    "openstack",
    "nova",
    "css"
],
"proxies": [
    "177.37.240.52:8080",
    "200.0.226.122:8080"
],
"type": "repository"
}
``` 

This is already mocked in ***main*** section and can be modified to execute different queries with the crawler,
by simply running **crawler.py** python code as follows:

python crawler.py
