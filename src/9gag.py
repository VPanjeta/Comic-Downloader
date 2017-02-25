import re
import json
import urllib
from urllib2 import *

def download(images):
	opener = build_opener()
	for image in images:
		try:
			temp = opener.open(image)
			print "Saving image....[%s]" %(image.split("/")[-1:][0])
		except URLError: 
			continue
		except HTTPError, e:
			print " Cannot get [%s] Reason: [%s]" %((image.split("/")[-1:][0],e.reason))
			
		filen = image.split("/")[-1:][0]
		ft = open(filen,"wb")
		ft.write(temp.read())
		ft.close

def extcheck(imglist):
	count = 0
	for img in imglist:
		if img.split(".")[-1:][0] != "tiff" and img.split(".")[-1:][0] != "png" and img.split(".")[-1:][0] != "gif":
			if img.split(".")[-1:][0] != "jpg" and img.split(".")[-1:][0] != "bmp":
				imglist.pop(count)
		count += 1
	return imglist

def uniqsort(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def gag(wlist,startid):
	url = 'https://9gag.com/new/json'
	payload = {'list': wlist, 'id': str(startid)}
	headers = {'Accept': 'application/json',
	'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}

	req = Request(url, urllib.urlencode(payload), headers)
	f = urlopen(req)
	source = f.read()
	content = json.loads(source)

	source_html=""
	for text,con in content['items'].iteritems():
		source_html += con

	regex = re.compile("[(htt|ft)]+[ps]+:\/\/[^<>]{3,}\.[(jpg|png|gif|tiff|bmp)]{3,4}")
	r = regex.search(source_html)
	imagelist =  extcheck(uniqsort(regex.findall(source_html)))
	download(imagelist)
	f.close()
	return int(imagelist[-1:][0].split('_')[0].split('/')[-1:][0])

def main():
	limit = 10
	print '1. Hot\n2. Trending'
	choice = input('Enter your choice:')
	print '--------------------------------'

	wl = ''
	host = ''

	if choice == 1: 
		wl = 'hot'
		host = 'http://9gag.com'
	else: 
		wl = 'trending'
		host = 'http://9gag.com/trending'

	g = urlopen(host)
	src = g.read()
	src_html = ""
	for lines in src:
			src_html += lines
	regex = re.compile("[(htt|ft)]+[ps]+:\/\/[^<>]{3,}\.[(jpg|png|gif|tiff|bmp)]{3,4}")
	r = regex.search(src_html)
	imagelist =  extcheck(uniqsort(regex.findall(src_html)))
	download(imagelist)
	start_id = int(imagelist[-1:][0].split('_')[0].split('/')[-1:][0])
	g.close()
	for itr in range(0,limit-10,10):
		temp = gag(wl,start_id)
		start_id = temp
		
if __name__ == "__main__":
	main()
	exit()