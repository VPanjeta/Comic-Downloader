from __future__ import print_function
import os
from bs4 import BeautifulSoup
import urllib3

dir = os.path.dirname(os.path.abspath(__file__))
download_directory = dir + "/Comics"

minRang = int(input("Page First(1): "))
maxRang = int(input("Page Last(15): "))

if not os.path.exists(download_directory):
    os.makedirs(download_directory)


for url_range in range(minRang, maxRang):
    main_url = "http://theoatmeal.com/comics_pg/page:" + str(url_range)
    print("Entered Page " + str(url_range))

    http = urllib3.PoolManager()


    main_url_response = http.request('GET', main_url).data

    main_url_soup = BeautifulSoup(main_url_response, 'html.parser')
    mylist = []
    for comiclink in main_url_soup.find_all('a'):
        all_links = comiclink.get('href')
        split_links = all_links.split('/')
        try:
            if split_links[1] == "comics" and split_links[2] != "":
                if all_links not in mylist:
                    mylist.append(all_links)
        except:
            pass

    for element in mylist:
        old_source = element
        new_source = old_source.replace(
            '/comics/', 'http://theoatmeal.com/comics/')

        # Download stuff here
        url = new_source

        # Send an HTTP GET request to the comic URL
        response = http.request('GET', url).data

        soupedversion = BeautifulSoup(response, 'html.parser')

        comicname = soupedversion.title.string
        comicname = comicname.replace('_', '')
        comicname = comicname.replace('?', '')
        comicname = comicname.replace(':', '')
        comicname = comicname.replace('*', '')
        comicname = comicname.replace('"', '')

        comicdir = dir + "/Comics/" + comicname

        if not os.path.exists(comicdir):
            print(" Downloading " + comicname)
            os.makedirs(comicdir)
        else:
            if not len(os.listdir(comicdir)) == 0:
                print("Neglected " + comicname +" because it already exists in your directory.")
                continue
            else:
                print(" Downloading " + comicname)

        for imglink in soupedversion.find_all('img'):
            mylink = imglink.get('src')
            if mylink:
                current_comic_src = mylink.split('/')
                if current_comic_src[4] == "comics":
                    # Send an HTTP GET request to the image URL
                    img_data = http.request('GET', mylink).data
                    filename = current_comic_src[6]
                    filename = filename.replace('?reload', '')
                    path = os.path.join(comicdir, filename)
                    with open(path, "wb") as data:
                        data.write(img_data)

    print("Completed Download of Comic: " + comicname)
