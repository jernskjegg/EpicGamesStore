import requests
import json
import urllib, time
import datetime as dt
from datetime import date

url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=NO&allowCountries=NO"
response = urllib.request.urlopen(url)
data = json.loads(response.read())

markPos= []
listOfDates = []
for i in range(0,25):
    try:
        checkTest = data["data"]["Catalog"]["searchStore"]["elements"][i]["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]
        if "startDate" in checkTest.keys():
            takeDate = checkTest.get("startDate")
            listOfDates.append(takeDate)
            markPos.append(i)
        else:
            listOfDates.append("X")
    except (TypeError, IndexError):
        pass

timeNow = dt.datetime.today()
timeNowForm = str(timeNow.strftime("%Y-%D%H%M%SZ"))

games=[]
imageURLs = []
if takeDate < timeNowForm:
    try:
        for i in markPos :
            games.append(data["data"]["Catalog"]["searchStore"]["elements"][i].get("title"))
            imageURLs.append(data["data"]["Catalog"]["searchStore"]["elements"][i]["keyImages"][1].get("url"))
    except IndexError:
        pass
else:
    imageURLs.append("This game is probably vaulted")
        
finalDict = dict(zip(games, imageURLs))
for key in list(finalDict.keys()):
    if key == "Mystery Game":
        finalDict.pop(key)
        
finalStr = str(finalDict)
webhookUrl = "yourWebhookURLHere"
slackNotif = {"text": finalStr.strip("{}")}
response = requests.post(webhookUrl, data=json.dumps(slackNotif))
error = ("Request returned error code {}, the response is: {}").format(response.status_code, response.text)
if response.status_code != 200:
    raise ValueError(error)
