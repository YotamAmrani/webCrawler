import sys
import json
import selenium
from collections import deque

# TODO: create a class of a web page to crawl?
# TODO: mark them if we have visited the page


class PageNode:
    def __init__(self, url, depth):
        self._url = url
        self._depth = depth




def main():
    args = sys.argv[1:]
    print(args)

def find_page_images(PageNode):
    """"""
    pass


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
    while current_page._depth  <= depth:
        current_page = pages_to_crawl.popleft() # get the current page
        if current_page._url not in my_urls_list:
            my_urls_list.add(current_page._url) # add to my urls list
            print("scraping the page here")
            print("appending the new data to our results file")










def init_results_file():
    results = []

def insert_images():
    pass

def verify_url_path(url):
    """"""
    pass
def verify_input_arg():
    pass



if __name__ == "__main__":
    main()
