import requests, re, os, glob
import textwrap, requests, cv2, json
from PIL import Image, ImageFont, ImageDraw
import numpy as np
from random import randint
import pandas as pd
import pprint
from pypdf import PdfWriter, PdfReader
from pypdf.errors import PdfReadError
from urllib.parse import urlparse
from datetime import datetime

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


def SearchTestDb(CourseNumber, Year):
    UrlGui = 'https://www4.huji.ac.il/htbin/exams/exams.cgi'
    UrlData = f'action=mode2&coursenum={CourseNumber}&coursename=&teachername=&keywords=&year2={Year}&year1=2000&moed=0&semester=0&Submit=%F9%EC%E7'  

    r = requests.post(UrlGui,UrlData,headers=UrlHeaders,cookies=UrlCookies)
    if r.status_code == 200:
        return r.content
    else:
        print("did not get 200")
        exit()

def DownloadTests(CourseNumber, Html):
    UrlPdfRegex = r'https?://[^"\']+\.pdf'
    PdfUrls = re.findall(UrlPdfRegex,str(Html))

    PdfFileList = []
    for UrlOfPdf in PdfUrls:
        print(UrlOfPdf)
        PdfFileName = os.path.basename(urlparse(UrlOfPdf).path)
        pdf = requests.get(UrlOfPdf,headers=UrlHeaders,cookies=UrlCookies)

        if os.path.isdir("tests/"+CourseNumber) == True:
            pass
        else:
            os.mkdir("tests/"+CourseNumber)

        with open("tests/"+CourseNumber+"/"+PdfFileName,'wb') as Pdf:
            Pdf.write(pdf.content)
        pdf.close()

        PdfFileList.append("tests/"+CourseNumber+"/"+PdfFileName)
    return {
        'PdfList' : PdfUrls,
        'PdfFileList' : PdfFileList
    }



def PdfCombine(CourseNumber, List):
    writer = PdfWriter()

    for PdfFile in List[::-1]:
        try:
            PdfReader(PdfFile)
        except PdfReadError:
            print("invalid PDF file")
        else:
            writer.append(PdfFile)
    writer.write(str(CourseNumber)+".pdf")
    writer.close()

def PdfFirstPage(CourseId, Year):
# def TextToIcon(Text, TemplateImage, Font, FilePath, CourseSeed):
    # Open image with OpenCV
    im_o = np.zeros((1000,1000,3), np.uint8)

    # im_o = cv2.imread(TemplateImage) # read from image.

    # Make into PIL Image
    im_p = Image.fromarray(im_o)

    # Get a drawing context
    draw = ImageDraw.Draw(im_p)
    monospace = ImageFont.truetype(Font,130)

    draw.rectangle( # make the backaround a solid colour
        (0,0,1000,1000),
        fill = (randint(0,50),randint(0,50),randint(0,50)) # make it a dark pallet
    )

    draw.ellipse( # draw the main circle
        (20, 20, 1000, 1000), # circle covers the entire image
        fill = (randint(20,255),randint(20,255),randint(20,255)),  # random colour for the circle. make it a not too dark pallet.
        outline = (randint(0,255),randint(0,255),randint(0,255)), # random colour for the outline
        width=20
    )

    draw.multiline_text( # place the text
        # (im_p.width / 2, (im_p.height / 2)+40),
        (im_p.width / 2, (im_p.height / 2)), # make it be the middle
        Text,
        fill="black", # make the text black
        font=monospace,
        align="center",
        anchor="mm", # make it the middle
        stroke_width=4, # add the outline
        stroke_fill="white" # make the outline white
    )
    result_o = np.array(im_p)
    cv2.imwrite(FilePath, result_o)

def GetNamesFromShnaton(CourseNumber: int, Year: int): # the year is from the PDF. assume current year always,. not going back to 2000
    # get the json from the shanton:
    # TODO: fake headers to look like a browser (only needed if blocked.)
    ShnatonJson = requests.get("https://shnaton.huji.ac.il/api/courses/code/"+str(CourseNumber)+"?year="+str(Year))

    if ShnatonJson.status_code == 200: # dont trip over the network TODO: make this an assert.
        ShantonObject = json.loads(ShnatonJson.content)
        if ShantonObject[0]['code'] == (CourseNumber): # make sure we got the right course. TODO: make this an assert.
            print(str(CourseNumber) + "good")
            return(ShantonObject[0]['name']['he'])
        else:
            print(str(CourseNumber) + "bad. is not "+str(CourseNumber))
            print("issue with the shanton id abort.")
            print(ShantonObject[0]['code'])
            print(ShantonObject)
            exit()
    else:
        print("page is not 200, abort")
        exit()


def __main__(CourseIds,Year):
    # PdfHtmlPage = SearchTestDb(CourseIds,Year)
    # PdfFileList = DownloadTests(str(CourseIds),PdfHtmlPage)['PdfFileList']
    print(GetNamesFromShnaton(CourseIds,Year))

    # PdfCombine(CourseIds,PdfFileList)

Example = [80131, 80181]


for i in Example:
    __main__(i, 2026)
