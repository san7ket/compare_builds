#This is the script to compare packages in two different release engineering builds

import os
import subprocess
import urllib2

try:
    from BeautifulSoup import BeautifulSoup
    import wget
except Exception as e:
    subprocess.call(['pip', 'install', 'BeautifulSoup'])
    subprocess.call(['pip', 'install', 'wget'])
    from BeautifulSoup import BeautifulSoup
    import wget

flag = flag1 = flag2 = 0
signature = os.getenv('SIGNATURE')

#os.mkdir('packages')
#DIR = 'packages'
#print "chal raha hai"
signature = os.getenv('SIGNATURE')

def get_packages_name(html):
    soup = BeautifulSoup(html)
    anchors = soup.findAll('a')
    links = []
    for a in anchors:
        links.append(a['href'])
    links = filter(lambda k: 'rpm' in k, links)
    return links


def get_packages(package_name):
    print "Before sleep"
    DIR1 = 'packages'
    wget.download(os.getenv('SATELLITE_SNAP_URL')+package_name, DIR1)
    import time
    time.sleep(10)
def fun():
    signature = os.getenv('SIGNATURE')

    os.mkdir('packages')
    DIR1 = 'packages'
    flag = 0
    flag1 = 0
    flag2 = 0
    print "fun chalu"
    list1 = get_packages_name(urllib2.urlopen(os.getenv('SATELLITE_SNAP_URL')).read())
    list1.sort()
    print list1
    list2 = get_packages_name(urllib2.urlopen(os.getenv('RCM_COMPOSE_URL')).read())
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
    
def main():
    signature = os.getenv('SIGNATURE')
    print "chal raha hai"
    fun()

if __name__== "__main__":
  main()
