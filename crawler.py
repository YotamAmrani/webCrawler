# main libraries
import sys
from collections import deque

#  scraping libraries
import json
from bs4 import BeautifulSoup
import requests
import re

# GLOBAL VARS
# JSON_FILE_PATH = "D:/Interviews/dataloop/results.json"
JSON_FILE_PATH = "results.json"

"""
useful Links:
- https://www.geeksforgeeks.org/image-scraping-with-python/
- https://www.geeksforgeeks.org/beautifulsoup-scraping-link-from-html/
- https://www.geeksforgeeks.org/append-to-json-file-using-python/
"""


class PageNode:
    """
    The class represent a web page.
    given a url to crawl, and it's current depth node could be created.
    """
    def __init__(self, source_url, depth):
        self._url = source_url
        self._depth = depth

    def get_source_url(self):
        return self._url

    def get_node_depth(self):
        return self._depth


def main():
    args = sys.argv[1:]  # TODO: add test for the input args

    # Init the url and depth
    url = args[0]
    depth = int(args[1])

    # Init  local files
    init_results_file(JSON_FILE_PATH)  # Init the results file

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


def find_page_images(page_node):
    """
    Given a url, find all images included inside it's body and append them to the results file
    :param page_node: A PageNode holding the current page depth and url
    :return: None
    """
    html_data = get_data(page_node.get_source_url())
    soup = BeautifulSoup(html_data, 'html.parser')  # Parsing the response data, using BS

    # Getting all images on the passed link
    for item in soup.find_all('img'):
        if item.has_attr('src'):
            current_image = {"imageUrl": item['src'], "sourceUrl": page_node.get_source_url(),
                             "depth": str(page_node.get_node_depth())}
            # print(current_image)
            write_json(current_image, JSON_FILE_PATH)


def find_page_urls(url):
    """"""
    html_data = get_data(url)
    soup = BeautifulSoup(html_data, 'html.parser')  # to be discussed, should I pass it twice?
    current_node_urls = []

    # Getting all urls inside the  main url
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
        # display the actual urls
        # print(link.get('href'))
        current_node_urls.append(link.get('href'))

    return current_node_urls


# ---------- Appending to JSON file functions --------------

def init_results_file(filename):
    """
    Initializing the local results file, assuming it is empty
    :param filename: String - The local file path
    :return: None
    """
    with open(filename, 'r+') as file:
        file_data = {"results": []}
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
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

def crawl_page(url, depth):
    """
    Web crawler using BFS algorithm.
    The crawler start by searching for images of a given web page (declared as a node with depth 0),
    and move on to it's surrounding web pages (i.e. - links to pages within it), adding images
    from their pages as well. The process will continue up to a given depth.


    :param url: The starting page url
    :param depth: The maximum depth of neighbors pages to crawl
    :return: None
    """
    # init a queue for pages to crawl
    pages_to_crawl = deque()

    # init set to look for duplications
    my_urls_list = set()

    # init the
    current_page = PageNode(url, 0)
    pages_to_crawl.append(current_page)

    # run BFS as long as we are on the matching depth
    while current_page.get_node_depth() <= depth:
        current_page = pages_to_crawl.popleft()  # get the current page
        if current_page.get_source_url() not in my_urls_list and current_page.get_node_depth() <= depth:

            # add to my urls list
            my_urls_list.add(current_page.get_source_url())

            # add current node images:
            find_page_images(current_page)

            # find the current page urls:
            current_page_urls = find_page_urls(current_page.get_source_url())

            # append it to my queue
            for url in current_page_urls:
                if url not in my_urls_list:
                    pages_to_crawl.append(PageNode(url, current_page.get_node_depth() + 1))
            print("Adding site to crawl: " + current_page.get_source_url() + " , depth:"
                  + str(current_page.get_node_depth()))


def verify_url_path():
    """"""
    pass


def verify_input_arg():
    pass


if __name__ == "__main__":
    main()
