# main libraries
import sys
from collections import deque

#  scraping libraries
import json
from bs4 import BeautifulSoup
import requests
import re



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
    json_file_path = "D:/Interviews/dataloop/results.json"
    init_results_file(json_file_path)  # Init the results file

    # run th scrapping process:
    images = find_page_images("https://www.geeksforgeeks.org/")
    urls = find_page_urls(url)

    # run the main crawling function:
    crawl_page(url, depth, json_file_path)

    # Testing section:
    print("IMAGES: ")
    # for img in images:
    #     write_json(img,json_file_path)

    # print(images)
    print("\nURLS: ")
    # print(urls)

# ---------- Parsing HTML functions --------------

def get_data(url):
    """
    Using the requests lib, getting the body of a given url
    :param url: String - The url to access
    :return: String - The response bodt
    """
    r = requests.get(url)
    return r.text


def find_page_images(url, depth):
    """
    Given a url, find all images included inside it's body
    :param url: String - the url to scan
    :return: a list of all images inside of it
    """
    images = []
    html_data = get_data(url)
    soup = BeautifulSoup(html_data, 'html.parser') # Parsing the response data, using BS

    # Getting all images on the passed link
    for item in soup.find_all('img'):
        current_image = {}
        current_image["imageUrl"] = item['src'] # add the current img url
        # print(item['src'])
        current_image["sourceUrl"] = url
        current_image["depth"] = str(depth) # TODO: update based on the node passed by
        # print(current_image)
        images.append(current_image) # TODO: append to the json file
    # print(images)
    return images


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
    """"""
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

def crawl_page(url, depth, json_file_path):
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
        if current_page._url not in my_urls_list:

            # add to my urls list
            my_urls_list.add(current_page._url)

            # add current node images:
            images = find_page_images(current_page._url, current_page._depth)
            for img in images:
                write_json(img,json_file_path)

            # find the current page urls:
            current_page_urls = find_page_urls(current_page._url)
            # append it to my queue
            for url in current_page_urls:
                if url not in my_urls_list:
                    pages_to_crawl.append(current_page, PageNode(url, current_page._depth + 1))
    

            print("scraping the page here")
            print("appending the new data to our results file")
    pass


def verify_url_path(url):
    """"""
    pass
def verify_input_arg():
    pass


if __name__ == "__main__":
    main()
