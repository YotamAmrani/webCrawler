import requests
import sys
import re
import json
from bs4 import BeautifulSoup
from collections import deque
from PageNode import PageNode


""" GLOBAL VARS """
RESULTS_FILE_PATH = "results.json"
ROOT_URL_ARG_IDX = 0
DEPTH_ARG_IDX = 1


"""
A web crawler CLI:
Given a URL string and depth, the crawler will scan the web page for any images, continue to every link inside that page 
and scan it as well. The crawling should stop once it reached the desired depth (denoted by the input param, where 
depth=0 is the first page).

The Images source paths will be saved to the 'results.json' file in the following format:
{
    results: [ 
        { 
            imageUrl: string,
            sourceUrl: string 
            depth: number  
        ] 
}

"""


def main():
    argument_list = sys.argv[1:]
    root_url, max_depth = argument_list[ROOT_URL_ARG_IDX], int(argument_list[DEPTH_ARG_IDX])
    if not is_file_exists(RESULTS_FILE_PATH):
        init_results_file(RESULTS_FILE_PATH)
    crawl_page(root_url, max_depth)


def is_file_exists(file_name):
    """
    Test if a file already exist in the file system
    :param file_name: the file path to test
    :return: True if it exist, False elsewhere.
    """
    with open(file_name, 'wb+') as file:
        test = file.read(1)
        file.seek(0)
        return len(test) >= 1


def init_results_file(file_name):
    """
    Initialize the local results file, assuming it is empty
    :param file_name: String - The local file path
    :return: None
    """
    with open(file_name, 'r+') as file:
        file_data = {"results": []}
        file.seek(0)
        json.dump(file_data, file, indent=4)


# ---------- The crawler function -------------- #

def crawl_page(root_url, max_crawling_depth):
    """
    The Web crawler's main function - Based on the BFS traversing algorithm.
    The crawler starts by searching for images of a given web page (declared as the root node with depth 0),
    and moves on to its adjacent web pages (i.e. - URL links to pages within it), adding images
    from their pages as well. The process will continue until the required depth is reached.

    :param root_url: The starting page url
    :param max_crawling_depth: The maximum depth of neighbors pages to crawl
    :return:
    """

    current_page = PageNode(root_url, 0)
    pages_to_crawl = deque()
    pages_to_crawl.append(current_page)
    visited_urls = set(current_page.get_source_url())

    while current_page.get_node_depth() <= max_crawling_depth:
        current_page = pages_to_crawl.popleft()
        current_depth = current_page.get_node_depth()

        if current_depth <= max_crawling_depth:
            extract_images_source_paths(current_page)
            adjacent_urls = extract_adjacent_urls(current_page)
            for adjacent_url in adjacent_urls:
                if adjacent_url not in visited_urls:
                    visited_urls.add(adjacent_url)
                    pages_to_crawl.append(PageNode(adjacent_url, current_depth + 1))


def extract_images_source_paths(page_node):
    """
    Given a URL path, write all images source paths to the results file.
    :param page_node: A PageNode instance
    :return:
    """
    html_data = get_page_body(page_node)
    soup = BeautifulSoup(html_data, 'html.parser')

    for item in soup.find_all('img'):
        if item.has_attr('src'):
            current_image = {"imageUrl": item['src'],
                             "sourceUrl": page_node.get_source_url(),
                             "depth": str(page_node.get_node_depth())}

            write_to_results_file(current_image, RESULTS_FILE_PATH)


def extract_adjacent_urls(page_node):
    """
    Given a URL path, find all URL paths included inside its body, and return them
    :param page_node: the given page to extract URLs from
    :return: returns a list of URL paths contained in the given page body element.
    """
    soup = BeautifulSoup(get_page_body(page_node), 'html.parser')
    adjacent_urls = []

    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
        adjacent_urls.append(link.get('href'))

    return adjacent_urls


def get_page_body(page_node):
    """
    Returns the html body of a given url
    :param page_node: Page node holding the URL to access
    :return: String - The HTML response body
    """
    url = page_node.get_source_url()
    response = requests.get(url)
    return response.text


def write_to_results_file(new_data, file_name=RESULTS_FILE_PATH):
    """
    Append new data to the given json file
    :param new_data: the data to append
    :param file_name: the json file path
    :return:
    """
    with open(file_name, 'r+') as file:
        file_data = json.load(file)
        file_data["results"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)


if __name__ == "__main__":
    main()
