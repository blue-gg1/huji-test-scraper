import requests, re
from datetime import datetime



def SearchTestDb(CourseNumber, Year):
    UrlGui = 'https://www4.huji.ac.il/htbin/exams/exams.cgi'
    UrlHeaders = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:154.0) Gecko/20100101 Firefox/154.0',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, br, zstd',
        'Referer' : 'https://www4.huji.ac.il/htbin/exams/exams.cgi',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    UrlCookies = {
    'glassix-visitor-id-v2-ae4edaa7-9020-46d9-8df3-114f0e6fec3c' : '9d669d7b-4c23-4c0d-9139-48ed91c6be25',
    'TS016ac11e': '01b025178ec1e04961ec26c47a2e5805a325b38aa3071eb788d5c4a208995fef56c7b6be369b200b155fb8044497a2abe192ee3dab',
    'TS6368d62d027': '082149a1b4ab2000d3cf882c57f91c9cf9e733b1dd0b30091d81ed29c62017648d6bb5adb3df2726084756c3b91130008f560bed0e525baa92753f2fdc7b2cfbde0348df7da96b04117a6b3b42022b9b527f31d2f13e04c3716005cae46d6bca'
    }
    UrlData = f'action=mode2&coursenum={CourseNumber}&coursename=&teachername=&keywords=&year2={Year}&year1=2000&moed=0&semester=0&Submit=%F9%EC%E7'  

    r = requests.post(UrlGui,UrlData,headers=UrlHeaders,cookies=UrlCookies)
    if r.status_code == 200:
        return {
            'HtmlContent' :r.content
            }
    else:
        print("did not get 200")
        exit()


html = SearchTestDb(80131,(str(datetime.now().year)))['HtmlContent']
print(html)
UrlPdfRegex = re.compile('https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*).pdf')
print(re.search(UrlPdfRegex,str(html)))