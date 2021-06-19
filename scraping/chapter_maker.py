from PIL import Image
from io import BytesIO
from .utils import get_page_soup, clear, get_sorted_arr_from_dict
from datetime import datetime
from .request_getter import RequestGetter


class ChapterMaker():
    '''
    params:
        chap_name<str>: the name of chapter that is being downloaded
        url<str>: url of the chapter page that should be downloaded
    '''

    def __init__(self, chap_name, url, verbose=False):
        self.chap_name = chap_name
        self.url = url
        self.verbose = verbose

    def get_image_urls(self):
        '''
        retrieves a list of the urls of all img elements with a class of "text-center"

        returns:
            List<str>: image urls
        '''
        soup = get_page_soup(self.url)
        div = soup.find(class_="chapter-container")

        img_urls = []

        for img in div.find_all('img'):
            img_url = img['data-src']
            if img_url:
                img_urls.append(img_url)
        return img_urls

    def get_images(self):
        '''
        returns:
            List<Image>: A list of PIL Image objects
        '''
        img_urls = self.get_image_urls()
        if self.verbose:
            clear()
            print(f"Getting pages for {self.chap_name}")

        img_responses = RequestGetter.runner(img_urls)
        img_responses = get_sorted_arr_from_dict(img_responses)

        images = []
        for img_resp in img_responses:
            try:
                img = Image.open(BytesIO(img_resp)).convert('RGB')
                images.append(img)

            except IOError as e:
                # print("Error loading an image for this comic. It's likely a problem with the website's copy, so I'll skip it")
                return []
        if self.verbose:
            print("Got everything I needed, saving the file...")
        return images

    def create_pdf(self, dir):
        '''
        params:
            dir<str>: The filename/path the pdf should be saved under
        '''
        images = self.get_images()
        if len(images):
            images[0].save(dir, "PDF", resolution=100.0,
                           save_all=True, append_images=images[1:])
            del images
            if self.verbose:
                print(f"Saved {self.chap_name} : {dir}", end="\n")
            return True
        else:
            if self.verbose:
                print(f"Didn't find any images for {self.chap_name}")
            return False



# for debugging purposes
if __name__ == "__main__":
    url = 'https://wallcomic.com/comic/doomsday-clock/chapter-12/159078/all'
    cm = ChapterMaker("doomsday clock", url)
    cm.create_pdf('test/doomsday_clock.pdf', )
