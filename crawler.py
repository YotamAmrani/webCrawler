# main libraries
import sys
from collections import deque

#  scraping libraries
import json
from bs4 import BeautifulSoup
import requests
import re

# GLOBAL VARS
json_file_path = "D:/Interviews/dataloop/results.json" # TODO: handle the first time access bug

"""
useful Links:
- https://www.geeksforgeeks.org/image-scraping-with-python/
- https://www.geeksforgeeks.org/beautifulsoup-scraping-link-from-html/

- https://www.geeksforgeeks.org/append-to-json-file-using-python/
"""


# TODO: mark them if we have visited the page
class PageNode:
    def __init__(self, source_url,depth):
        self._url = source_url
        self._depth = depth


def main():
    args = sys.argv[1:]  # TODO: add test for the input args

    # Init the url and depth
    url = args[0]
    depth = int(args[1])

    # Init  local files
    init_results_file(json_file_path)  # Init the results file

    # run the main crawling function:
    crawl_page(url, depth)

    # Testing section:

# ---------- Parsing HTML functions --------------

def get_data(url):
    """
    Using the requests lib, getting the body of a given url
    :param url: String - The url to access
    :return: String - The response bodt
    """
    r = requests.get(url)
    return r.text


def find_page_images(pageNode):
    """
    Given a url, find all images included inside it's body and append them to the results file
    :param pageNode: A PageNode holding the current page depth and url
    :return: None
    """
    html_data = get_data(pageNode._url)
    soup = BeautifulSoup(html_data, 'html.parser') # Parsing the response data, using BS

    # Getting all images on the passed link
    for item in soup.find_all('img'):
        if item.has_attr('src'):
            current_image = {}
            current_image["imageUrl"] = item['src'] # add the current img url
            current_image["sourceUrl"] = pageNode._url
            current_image["depth"] = str(pageNode._depth) # TODO: update based on the node passed by
            # print(current_image)

            # images.append(current_image) # TODO: append to the json file
            write_json(current_image, json_file_path)


def find_page_urls(url):
    """"""
    html_data = get_data(url)
    soup = BeautifulSoup(html_data, 'html.parser') # to be discussed, should I pass it twice?
    current_node_urls = []

    # Getting all urls inside the  main url
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
        # display the actual urls
        # print(link.get('href'))
        current_node_urls.append(link.get('href'))

    return current_node_urls


# ---------- Appending to JSON file functions --------------

def init_results_file(filename):
    """"""
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["results"] = []
        # # Sets file's current position at offset.
        file.seek(0)
        # # convert back to json.
        json.dump(file_data, file, indent=4)


def write_json(new_data, filename='results.json'):
    """
    Help function, appending new data to the given json file
    :param new_data: the data to append
    :param filename: the json file path
    :return: None
    """
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["results"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


# ---------- Main crawler functions --------------

# TODO: to be completed
def crawl_page(url, depth):
    """"""
    # init a queue for pages to crawl
    pages_to_crawl = deque()

    # init set to look for duplications
    my_urls_list = set()

    # init the
    current_page = PageNode(url, 0)
    pages_to_crawl.append(current_page)


    # run BFS as long as we are on the matching depth
    while current_page._depth <= depth:
        current_page = pages_to_crawl.popleft() # get the current page
        if current_page._url not in my_urls_list and current_page._depth <= depth:

            # add to my urls list
            my_urls_list.add(current_page._url)

            # add current node images:
            find_page_images(current_page)

            # find the current page urls:
            current_page_urls = find_page_urls(current_page._url)

            # append it to my queue
            for url in current_page_urls:
                if url not in my_urls_list:
                    pages_to_crawl.append(PageNode(url, current_page._depth + 1))
            print("Adding site to crawl: " + current_page._url + " , depth:" + str(current_page._depth))



def verify_url_path(url):
    """"""
    pass
def verify_input_arg():
    pass


if __name__ == "__main__":
    main()
