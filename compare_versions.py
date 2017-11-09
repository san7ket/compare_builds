import sys,urllib2
from BeautifulSoup import BeautifulSoup

flag = 0

def get_packages(html):
	soup = BeautifulSoup(html)
	anchors = soup.findAll("a")
	links =[]
	for a in anchors:
		links.append(a['href'])

	links = filter(lambda k:'rpm' in k, links)
	return links

list1 = get_packages(urllib2.urlopen(sys.argv[1]).read())
list1.sort()
list2 = get_packages(urllib2.urlopen(sys.argv[2]).read())
list2.sort()
print "There are " + str(len(list1)) + " packages in build1 and " + str(len(list2)) + " packages in build2."

for x in range(0,len(list1)-1):
	if list1[x] == list2[x]:
		flag=flag+1
	else:
		print "The version of package " + list1[x] + " from build1 is not similar to version of package " + list2[x] + " from build2."

if flag == len(list1)-1:
	print "Versions in both builds are same"
else:
	print str((len(list1)-1)-flag) + " packages version found mismatched!"
