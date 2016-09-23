#!/usr/bin/env python
''' Downloads manga image files from mangafox.me, creating a folder for the manga
 series and subfolders for each chapter within it'''

import errno
import os
import requests
import sys

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

def download_manga(url):
    # Download manga given url of first page
    [folder , volume, chapter] = url.split('/')[4:7]
    mkdir_p(folder)
    os.chdir(folder)
    chapter = filter(lambda x: x.isdigit(), chapter)

    while True:
        mkdir_p(chapter)
        # Downloads a chapter of the manga
        try:
            print('Downloading page %s...' % url)
            res = requests.get(url)
            res.raise_for_status()        
        except requests.exceptions.ConnectionError:
                # Stops when a bad URL is entered
                 print('The page %s does not exist' % url)
                 break
                
        soup = BeautifulSoup(res.text, 'html.parser')
        comicElem = soup.select('#viewer img')
        
        if comicElem == []:
             print('No Image at %s' % url)
             break
        else:
            # Download the image.
            try:
                 comicUrl = comicElem[0].get('src')
                 print('Downloading image %s...' % comicUrl)
                 res = requests.get(comicUrl)
                 res.raise_for_status()        
            except:
                # Stops when image failed to download
                 print('Problem Occured at %s' % comicUrl)
                 break
                # Save the image to folder
            imageFile = open(os.path.join(chapter, os.path.basename(comicUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            
        NextPageElem = soup.select('#viewer a')[0]
        
        # Goes to next chapter if chapter is finished
        if NextPageElem.get('href') == 'javascript:void(0);':
            try:
                if int(chapter) == 1: #First chapter has no previous chapter link
                    NextChapterElem = soup.select('#chnav a')[0]
                    url = NextChapterElem.get('href')
                    chapter = str(int(chapter) + 1).zfill(3)
                else:
                    NextChapterElem = soup.select('#chnav a')[1]
                    url = NextChapterElem.get('href')
                    chapter = str(int(chapter) + 1).zfill(3)               
            except IndexError:
                # Stops when no next chapter available
                 print('No Next Chapter Found at %s' % url)
                 break        
        # Else goes to next page in chapter
        else:
            FirstPageElem = soup.select('#series a')[0]
            ChapterUrl = FirstPageElem.get('href').replace('1.html','')
            url = ChapterUrl + NextPageElem.get('href')

    raw_input('Download Completed.')

if __name__ == '__main__':
    try:
        download_manga(sys.argv[1])
    except:
        url = raw_input('Copy url (ie. http://mangafox.me/manga/kimi_no_iru_machi/v01/c001/1.html): \n')
        download_manga(url)
                       
