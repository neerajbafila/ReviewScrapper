# from flask import Flask, render_template, request,jsonify
# from flask_cors import CORS,cross_origin
# import requests
# from bs4 import BeautifulSoup as bs
# from urllib.request import urlopen as uReq
# searchString = 'apple'
# flipkart_url = "https://www.flipkart.com/search?q=" + searchString
# uClient = uReq(flipkart_url)
# flipkartPage = uClient.read()
# uClient.close()
# flipkart_html = bs(flipkartPage, "html.parser")
# bigboxes = flipkart_html.findAll("div", {"class": "bhgxx2 col-12-12"})
# del bigboxes[0:3]
# box = bigboxes[0]
# productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
# prodRes = requests.get(productLink)
# prodRes.encoding='utf-8'
# prod_html = bs(prodRes.text, "html.parser")
# print(prod_html)
# commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})
# filename = searchString + ".csv"
# fw = open(filename, "w")
# headers = "Product, Customer Name, Rating, Heading, Comment \n"
# fw.write(headers)
# reviews = []
# for commentbox in commentboxes:
#     try:
#
#         name = commentbox.div.div.find_all('p', {'class': '_3LYOAd _3sxSiS'})[0].text
#     except:
#
#         name = 'No Name'
#     try:
#         rating = commentbox.div.div.div.div.text
#     except:
#         rating = 'No Rating'
#
#     try:
#         commentHead = commentbox.div.div.div.p.text
#     except:
#         commentHead = 'No Comment Heading'
#     try:
#
#         comtag = commentbox.div.div.find_all('div', {'class': ''})
#         custComment = comtag[0].div.text
#         print(comtag)
#
#     except Exception as e:
#         print("Exception while creating dictionary: ",e)
#
# mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
#                           "Comment": custComment}
# reviews.append(mydict)
# print(reviews)
#
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

searchString = 'apple'
flipkart_url = 'https://www.flipkart.com/search?q=' + searchString
uClient = uReq(flipkart_url)
flipKartPage = uClient.read()

    # flipKartPage

uClient.close()
flipkartHtml =bs(flipKartPage, 'html.parser')
# flipkartHtml
bigBox = flipkartHtml.find_all('div', attrs={'class':'bhgxx2 col-12-12'})
print(bigBox)
product_url = bigBox[2].find_all('div', attrs={'class':'_1UoZlX'})

product_url = product_url[0].a['href']
product_url = flipkart_url + product_url
print(product_url)
prodReq = requests.get(product_url)
prodReq.encoding='utf-8'
proHtml = bs(prodReq.text,'html.parser')
reviewBox = proHtml.find_all('div', attrs={'class':'bhgxx2 col-12-12'})
# class':'_2aFisS
reviewBox = proHtml.find_all('div', attrs={'class':'col _390CkK'})
reviewBox[2].find_all('div', attrs={'hGSR34 E_uFuv'})
name = []
rating = []
commentHead = []
comtag = []
allReview = []
for reviewData in reviewBox:
    try:
        userName = reviewData.find_all('p', attrs={'class': '_3LYOAd _3sxSiS'})
        userName = [name.get_text() for name in userName]
        name.append(userName[0])
    except:
        userName = 'No Name'
        name.append(userName)

    try:
        userRating = reviewData.find_all('div', {'class': 'hGSR34 E_uFuv'})
        userRating = [rat.get_text() for rat in userRating]
        rating.append(userRating[0])
    except:
        userRating= 'No Rating'
        rating.append(userRating)

    try:
        userCommentHead = reviewData.find_all('p', {'class': '_2xg6Ul'})
        userCommentHead = [commentHe.get_text() for commentHe in userCommentHead]
        commentHead.append(userCommentHead[0])
    except:
        userCommentHead = 'No Heading'
        commentHead.append(userCommentHead)

    try:
        userComment = reviewData.find_all('div', {'class': 'qwjRop'})
        userComment = [comt.get_text() for comt in userComment]
        comtag.append(userComment[0])
    except:
        userComment = "No comment provided by user"
        comtag.append(userComment)
    mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                              "Comment": comtag}
    allReview.append(mydict)
print(allReview)
print('*'*8)
print(len(allReview))
print(allReview[0:(len(allReview)-1)])

    # except Exception as e:
    #     print('The Exception message is: ', e)
    #     return 'something is wrong'













