from PyPDF2 import PdfFileMerger
import os
from utils import clear


def merge_pdfs(in_dir, out_file, max=0):
    '''
    params:
        in_dir<str>: the directory containing pdf files with a trailing /
        out_file<str>: the filename for the merged pdf
        max<int>: (optional) the total number of pdf files to be merged
    '''
    merger = PdfFileMerger()
    pdfs = os.listdir(in_dir)
    prev = pdfs[0]
    file_names = []
    # create the correctly ordered list of files
    for i, pdf in enumerate(pdfs):
        if i == max and max > 0:
            break
        # .5 chapters are listed before their numbered chapter, but they should be placed after while merging
        # so check if the previous chapter was a .5 chapter
        # if it was, remove it, add the numbered chapter first,
        # then add the .5 chapter back so that the order remains accurate
        if '.5.pdf' in prev:
            file_names.pop()
            file_names.append(in_dir+pdf)
            file_names.append(in_dir+prev)
        else:
            file_names.append(in_dir+pdf)

        prev = pdf

    for i, fname in enumerate(file_names):
        merger.append(fname)

        dot_ctr = '.' * round(10*i/len(file_names))
        clear()
        print(f"working{dot_ctr}")

    print("saving merged file (this can take some time)")
    merger.write(out_file)
    merger.close()
