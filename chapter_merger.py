from PyPDF2 import PdfFileMerger
import os
from scraping.utils import clear
import natsort

def merge_pdfs(in_dir, out_file, max=0):
    '''
    params:
        in_dir<str>: the directory containing pdf files with a trailing /
        out_file<str>: the filename for the merged pdf
        max<int>: (optional) the total number of pdf files to be merged
    '''
    merger = PdfFileMerger()
    pdfs = natsort.natsorted(os.listdir(in_dir))

    file_names = []
    # create the correctly ordered list of files
    for i, pdf in enumerate(pdfs):
        if  max > 0 and i == max:
            break

        clear()
        print(f"Merging - {round(100*i/len(pdfs), 1)}%")
        merger.append(in_dir+pdf)

    print("saving merged file (this can take some time)")
    merger.write(out_file)
    merger.close()


if __name__ == "__main__":
    in_dir = "comics/Invincible_(2003)/"
    out_file = "Invincible_TPB.pdf"
    merge_pdfs(in_dir, out_file)