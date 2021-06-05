import requests
from PIL import Image
from io import BytesIO
from utils import get_page_soup, print_progress
from datetime import datetime

class ChapterMaker():
    '''
    params:
        chap_name<str>: the name of chapter that is being downloaded
        url<str>: url of the chapter page that should be downloaded
    '''

    def __init__(self, chap_name, url):
        self.chap_name = chap_name
        self.url = url

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

    def stream_image(self, url):
        '''
        params:
            url<str>: an image url

        returns:
            response<obj>: a request object holding the loaded image
        '''
        try:
            return requests.get(url, stream=True)
        except:
            print(f"Couldn't stream {url}")

    def get_images(self):
        '''
        returns:
            List<Image>: A list of PIL Image objects
        '''
        img_urls = self.get_image_urls()

        images = []
        ctr = 0
        dot_string = '.'
        start_time = datetime.now()
        for url in img_urls:
            img_resp = self.stream_image(url)
            if img_resp:
                try:
                    img = Image.open(BytesIO(img_resp.content)).convert('RGB')
                    images.append(img)

                    ctr += 1
                    print_progress(self.chap_name, start_time, ctr, len(img_urls))
                except IOError as e:
                    print(e)
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
        else:
            print(f"Didn't find any images for {self.chap_name}")
        del images

    



# for debugging purposes
if __name__ == "__main__":
    url = 'https://wallcomic.com/comic/doomsday-clock/chapter-12/159078/all'
    cm = ChapterMaker("doomsday clock", url)
    cm.create_pdf('test/doomsday_clock.pdf', )
