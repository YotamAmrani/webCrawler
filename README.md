# webCrawler
A web crawler CLI  
Given a URL, the crawler will scan the webpage for any images, continue to every link inside that page and scan it as well. 
The crawling should stop once <depth> is reached. depth=3 means we can go as deep as 3 pages from the source URL (denoted by the <url> param), and depth=0 
is just the first page. 

Results are saved to the results.json file in the following format:  
{
	results: [  
		{  
			imageUrl: string,  
			sourceUrl: string // the page url this image was found on  
			depth: number // the depth of the source at which this image was found on  
		}  
	]  
}  


# Files:
crawler.py - The main file to run.  
results.json - assumed to be empty, the json file to be filled with the images that were found.

# How to use the crawler:  
Assuming both files are at the same directory,  
Access the crawler directory through the CMD and Run the crawler:  
   python "your_starting_node_url" _depth  
  
 An example run would be: python "https://www.geeksforgeeks.org/" 1  
  



