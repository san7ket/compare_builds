from BeautifulSoup import BeautifulSoup

import os
import sys
import urllib2
import wget

flag = flag1 = flag2 = 0
signature = sys.argv[3]

os.mkdir('packages')
DIR = 'packages'


def get_packages_name(html):
    soup = BeautifulSoup(html)
    anchors = soup.findAll('a')
    links = []
    for a in anchors:
        links.append(a['href'])
    links = filter(lambda k: 'rpm' in k, links)
    return links


def get_packages(package_name):
    wget.download(sys.argv[1]+package_name, DIR)

list1 = get_packages_name(urllib2.urlopen(sys.argv[1]).read())
list1.sort()
list2 = get_packages_name(urllib2.urlopen(sys.argv[2]).read())
list2.sort()
print(
    "There are " + str(len(list1)) + " packages in build1 and "
    + str(len(list2)) + " packages in build2."
)

for x in range(len(list1)):
    if list1[x] == list2[x]:
        flag = flag+1
    else:
        print(
            "The version of package " + list1[x] +
            " from build1 is not similar to version of package " + list2[x] +
            " from build2."
        )

if flag == len(list1)-1:
    print("Versions in both builds are same")
else:
    print(str((len(list1))-flag) + " packages version found mismatched!")

for x in range(len(list1)):
    get_packages(list1[x])

for x in range(len(list1)):
    if 'OK' in os.popen('rpm -K packages/' + list1[x]).read():
        flag1 = flag1 + 1
        if signature in os.popen('rpm -qpi packages/' + list1[x] + '| grep "Signature" ').read():
            flag2 = flag2 + 1
        else:
            print('signature not matched for ' + list1[x])
    else:
        print(list1[x] + 'package is not signed')

if flag1 == len(list1):
    print "All packages are signed!"
else:
    print(str(len(list1)-flag1) + 'packages are not signed!!')

if flag2 == len(list1):
    print("Signature matched for all packages!!")
else:
    print('Signature for ' + str(len(list1)-flag2) + ' packages not matched!!')
