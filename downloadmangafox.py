#!/usr/bin/env python
''' Downloads manga image files from mangafox.me, creating a folder for the manga
 series and subfolders for each chapter within it'''

import errno
import os
import requests
import sys
import threading

from math import ceil
from bs4 import BeautifulSoup

def mkdir_p(path):
    # Create a folder if it does not exist
    try:
        os.makedirs(path)
    except OSError as exc: 
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def get_next_ch(url, chapter):
    # Return the url for the next chapter
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    
    if int(chapter) == 1: # First chapter has no previous chapter link
        NextChapterElem = soup.select('#chnav a')
        url = NextChapterElem[0].get('href')
        chapter = str(int(chapter) + 1).zfill(3)        
    else:
        NextChapterElem = soup.select('#chnav a')
        url = NextChapterElem[1].get('href')
        chapter = str(int(chapter) + 1).zfill(3)
    return (url, chapter)


def count_ch(url, chapter):
    # Returns the number of chapters in the manga
    print 'Counting chapters in manga...'
    total_ch = int(chapter)
    
    while True:
        try:
            (url, chapter) = get_next_ch(url, chapter)
            total_ch += 1
        except IndexError:
            # Stops when no next chapter available
             print 'No next chapter found at {0} \n{1} chapters were found.'.format(url, total_ch)
             return total_ch
             break       

def download_ch(url, chapter):
    # Download manga chapter
    print 'Downloading Chapter {}...'.format(chapter)
    mkdir_p('Chapter_' + chapter)
    
    while True:
        
        try:
            res = requests.get(url)
            res.raise_for_status()        
        except requests.exceptions.ConnectionError:
                 print('The page {} does not exist'.format(url))
                 break
                
        soup = BeautifulSoup(res.text, 'html.parser')
        comicElem = soup.select('#viewer img')

        # Downloads manga image
        if comicElem == []:
             print('No Image at {}'.format(url))
             break           
        else:
            try:
                 comicUrl = comicElem[0].get('src')
                 res = requests.get(comicUrl)
                 res.raise_for_status()        
            except:
                 print('Problem Occured at ()'.format(comicUrl))
                 break

            imageFile = open(os.path.join('Chapter_{}'.format(chapter), os.path.basename(comicUrl)), 'wb')

            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

        # Goes to next page in chapter, or stops when chapter is finished    
        NextPageElem = soup.select('#viewer a')[0]

        if NextPageElem.get('href') == 'javascript:void(0);':
            break
        else:
            FirstPageElem = soup.select('#series a')[0]
            ChapterUrl = FirstPageElem.get('href').replace('1.html','')
            url = ChapterUrl + NextPageElem.get('href')

def dl_thread(url, chapter, ch_count):
    for i in range(ch_count):
        download_ch(url, chapter)
        try:
            (url, chapter) = get_next_ch(url, chapter)   
        except IndexError:
            print 'No next chapter found at {0}'.format(url)

def main():
    try:
        url = sys.argv[1]
    except IndexError:
        url = raw_input('Copy url (ie. http://mangafox.me/manga/kimi_no_iru_machi/v01/c001/1.html): \n')

    try:
        threads = float(sys.argv[2])
    except IndexError:
        threads = 3.0

    spliturl = url.split('/')
    folder = spliturl[4]
    mkdir_p(folder)
    os.chdir(folder) 
    ch0 = spliturl[-2] 
    ch0 = filter(lambda x: x.isdigit(), ch0) # Initial chapter

    total_ch = count_ch(url, ch0)

    # Create and start the Thread objects
    downloadThreads = []
    dl_interval = int(ceil(total_ch/threads))

    try:
        for i in range(1, total_ch + 1, dl_interval):
            thread_ch = str(i).zfill(3)
            turl = '/'.join(spliturl[:-2] + ['c{}'.format(thread_ch), spliturl[-1]])
            dlThread = threading.Thread(target=dl_thread, args=(turl, thread_ch, dl_interval))
            downloadThreads.append(dlThread)
            dlThread.start()

        #Wailt for all threads to end
        for runThread in downloadThreads:
            runThread.join()
        print 'Download Complete.'
    except KeyboardInterrupt:
        print 'Download stopped by user.'
        
        
if __name__ == '__main__':
    main()
