

class PageNode:
    """
    The class represent a web page.
    given a url of a site to crawl, and it's current depth (according to current crawling process).
    """
    def __init__(self, source_url, depth):
        self.__url = source_url
        self.__depth = depth

    def get_source_url(self):
        return self.__url

    def get_node_depth(self):
        return self.__depth
