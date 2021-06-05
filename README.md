# A Comic Web Scraper

A collection of python classes for scraping images of Read Comic Online sites.

## chapter_controller.py

Takes in user input as the search string, then uses ChapterSearcher to send a request to the nominated website's api to retrieve the search results.

The results are displayed on the command line and the user can input the ID for the comic they would like to download. 

The desired comic is passed to ChaptersDownloader, which finds all the issues for said comic and initiates a download loop for all issues (working on allowing download of only some issues).


# ChapterController
>> gets the user input and controls ChapterSearcher and ChaptersDownloader

# ChapterSearcher
>> uses the website api to search for a comic and returns the list of results

# ChaptersDownloader
>> uses the top level comic url found from the selected comic from the searcher to find all the comic issues, then uses ChapterMaker to download all the issues

# ChapterMaker
>> takes in a chapter url, finds all the images for that issue then downloads and saves them into a pdf

# ChapterMerger
>> can be used to merge a number of pdfs into a single pdf