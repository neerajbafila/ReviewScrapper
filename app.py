from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)


@app.route('/', methods=['GET']) ## route to display the home page
@cross_origin()
def home():
    return render_template('index.html')


@app.route('/review', methods=['POST', 'GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            # print(searchString)
            flipkart_url = 'https://www.flipkart.com/search?q=' + searchString
            # print(flipkart_url)
            uClient = uReq(flipkart_url)
            flipKartPage = uClient.read()
            uClient.close()
            flipkartHtml =bs(flipKartPage, 'html.parser')
            bigBox = flipkartHtml.find_all('div', attrs={'class': 'bhgxx2 col-12-12'})
            # print(bigBox)
            # product_url = bigBox[2].find_all('div', attrs={'class': '_3O0U0u'})
            product_url = [a for i in range(len(bigBox)) for a in bigBox[i].find_all('div', attrs={'class': '_3O0U0u'})]
            # product_url = "https://www.flipkart.com" + bigBox.div.div.div.a['href']
            product_url = product_url[0].a['href']
            product_url = flipkart_url + product_url
            prodReq = requests.get(product_url)
            prodReq.encoding='utf-8'
            proHtml = bs(prodReq.text,'html.parser')
            reviewBox = proHtml.find_all('div', attrs={'class': 'bhgxx2 col-12-12'})
            # class':'_2aFisS
            reviewBox = proHtml.find_all('div', attrs={'class': 'col _390CkK'})
            productName = [dt.get_text() for i in range(len(bigBox)) for dt in bigBox[i].find_all('div', {'class': '_3wU53n'})][0]
            # productName = bigBox[4].find_all('div', attrs={'class':'_3wU53n'})
            # productName = productName[0].get_text()
            # productName = productName.get_text()
            # print(productName)
            reviews = []
            reviewBox[2].find_all('div', attrs={'hGSR34 E_uFuv'})

            for reviewData in reviewBox:
                name = []
                rating = []
                commentHead = []
                comtag = []

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
                    userComment = userComment[0].replace('READ MORE', '') # removing read more
                    # print(userComment)
                    comtag.append(userComment)
                    # print(comtag)

                except:
                    userComment = "No comment provided by user"
                    comtag.append(userComment)

                # mydict = {"Product": searchString + " " + productName, "Name": name[0], "Rating": rating[0],
                #           "CommentHead": commentHead[0], "Comment": comtag[0]}
                mydict = {"Product": productName, "Name": name[0], "Rating": rating[0],
                          "CommentHead": commentHead[0],
                          "Comment": comtag[0]}
                reviews.append(mydict)
                # print(reviews)

            return render_template('results.html', reviews=reviews)

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong. Please search something which is available in flipkart'

    else:
        return render_template('index.html')


port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	# app.run(debug=True)
    app.run(host='0.0.0.0', port=port)





