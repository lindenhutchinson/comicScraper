# A Comic Web Scraper

A collection of python classes for scraping images of Read Comic Online sites.

## chapter_controller.py

Takes in user input as the search string, then uses ChapterSearcher to send a request to the nominated website's api to retrieve the search results.

The results are displayed on the command line and the user can input the ID for the comic they would like to download. 

The desired comic is passed to ChaptersDownloader, which finds all the issues for said comic and initiates a download loop for all issues (working on allowing download of only some issues).

