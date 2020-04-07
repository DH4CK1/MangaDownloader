#!/bin/python2.7
#-*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) <2020> <Dst_207>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

try:
     import requests,var_animate
except ModuleNotFoundError:
     exit('[!] Module Not installed!\n[!] "$ ./install" to installing')


import sys,os,time,re,json
from var_animate import *
# Menampung var Warna #
color = color()
me = color.show('red')
bi = color.show('blue')
cy = color.show('cyan')
pu = color.show('white')
i = color.show('green')
reset = color.show('reset')

# set input
input = animinput()
# set var
alert = animvar()
# Make a banner #
banner = banner('Manga','Dst_207','0.1 Downloader')

def search(query):
    c = {}
    r = requests.get('https://komiku.co.id/?post_type=manga&s='+query).text
    rgx = re.findall('<a href="https://komiku.co.id/manga/(.*?)/">',r)[0]
    r2 = requests.get('https://komiku.co.id/manga/'+rgx).text
    rgx2 = re.findall('<span>Chapter Baru </span><span>Chapter (.*?)</span>',r2)[0]
    c["judul"] = rgx
    c["komik"] = 'https://komiku.co.id/manga/'+rgx
    c["last_chapter"] = rgx2
    return json.dumps(c)


def download(link_komik,chapter):
    c = {}
    r = requests.get(link_komik).text
    rgx = re.search('</span> Chapter '+chapter+' </a> </td> <td class="tanggalseries"> <time class="post-date" datetime=".*?"> (.*?) </time> </td> <td class="tanggalseries dl"> <a href="(.*?)" rel="nofollow" target="_blank">DL</a>',r)
    r2 = requests.get(rgx.group(2)).text
    pdf_komik = re.findall('<a href="(.*?)" download>',r2)[0]
    c["rilis"] = rgx.group(1)
    c["download_pdf"] = pdf_komik
    return json.dumps(c)



print(banner)
print('{}<{}════════════════════════════════════════{}>').format(pu,bi,pu)
def main():
    key = input.ask('JudulManga')
    cari = search(key)
    j = json.loads(cari)
    print('{}<{}══════════{}[ {}Hasil Pencarian {}]{}═══════════{}>').format(pu,bi,me,cy,me,bi,pu)
    print('{}[{}+{}] JudulAnime{}: {}{}').format(pu,i,pu,me,cy,j["judul"])
    print('{}[{}+{}] JumlahChapter{}: {}1 {}- {}{}').format(pu,i,pu,me,cy,me,cy,j["last_chapter"])
    print('{}<{}══════════════{}[ {}Download {}]{}═══════════════{}>').format(pu,bi,me,cy,me,bi,pu)
    chapter = input.ask('DownloadChapter{}[{}1 {}- {}{}{}]'.format(bi,pu,me,pu,j["last_chapter"],bi))
    if int(chapter) > int(j["last_chapter"]):
       print(alert.false('Maaf Chapter tidak tersedia'))
       time.sleep(1)
       exit()
    else:
       down = download(j["komik"],chapter)
       j2 = json.loads(down)
       urlDown = j2["download_pdf"].replace(' ','%20')
       fileout = j["judul"]+'-chapter-'+chapter+'.pdf'
       os.system('curl '+urlDown+' > /sdcard/komik/'+fileout)
       time.sleep(1)
       print(alert.true('Berhasil Download'))
       time.sleep(1)
       print(alert.true('PATH{}: {}{}').format(me,cy,'/sdcard/komik/'+fileout))

try:
    main()
except:
    print(alert.false('Berhenti/Kesalahan!'))
