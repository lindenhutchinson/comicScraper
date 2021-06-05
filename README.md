# A Comic Web Scraper

A collection of python scripts with the goal of downloading comics as pdfs


## ChapterController
Run this to get started downloading comics.
> gets the user input and controls ChapterSearcher and ChaptersDownloader


## ChapterSearcher
> uses the website api to search for a comic and returns the list of results

## ChaptersDownloader
> uses the top level comic url found from the selected comic from the searcher to find all the comic issues, then uses ChapterMaker to download all the issues

## ChapterMaker
> takes in a chapter url, finds all the images for that issue then downloads and saves them into a pdf

## ChapterMerger
> can be used to merge a number of pdfs into a single pdf