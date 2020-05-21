from guizero import App, Text, Picture, Box
from lxml import html, etree
import requests
import urllib
import random
import datetime
import re

app = App(title="RIP CITY BABY")
teamUrl = "https://www.espn.com/nba/team/_/name/por/portland-trail-blazers"
espnUrl = "https://www.espn.com"
newGame = False
midnightAfterGame = False

def main():
    global app
    global teamUrl
    global espnUrl
    global newGame
    global midnightAfterGame
   
    teamPage = requests.get(teamUrl)
    teamDom = html.fromstring(teamPage.content)    
    liveGame = len(teamDom.xpath('//div[@class="time live"]/text()')) > 0
    links = teamDom.xpath('//a[@rel="nbagamecast"]//@href')
    linkIndex = 0
    if not liveGame:
        linkIndex = len(links) - 1
        if not midnightAfterGame:
            if str(datetime.datetime.now().hour) == '0':
                midnightAfterGame = True
                newGame = False
            else:
                linkIndex = len(links) - 2
    else:
        midnightAfterGame = False
    gameUrl = espnUrl + links[linkIndex]
    gamePage = requests.get(gameUrl)
    gameDom = html.fromstring(gamePage.content)
    timeArr = gameDom.xpath('//span[@class="status-detail"]/text()')
    if not midnightAfterGame:
        homeTeamScore = gameDom.xpath('//div[@class="score icon-font-before"]/text()')[0]
        awayTeamScore = gameDom.xpath('//div[@class="score icon-font-after"]/text()')[0]
        score.value = " " + homeTeamScore + " - " + awayTeamScore + " "
    else:
        score.value = "  VS  "
    if liveGame or midnightAfterGame:
        if len(timeArr) > 0:
            time.value = timeArr[0]
        else:
            date = teamDom.xpath('//span[@data-dateformat="date8"]/text()')[0]
            tipoff = teamDom.xpath('//div[@class="time"]/text()')[0]
            time.value = date + "  " + tipoff
    else:
        homeTeamName = gameDom.xpath('//span[@class="short-name"]/text()')[1]
        awayTeamName = gameDom.xpath('//span[@class="short-name"]/text()')[0]
        if awayTeamName == "Knicks" or homeTeamName == "Knicks":
            time.value = "THAT'S A BALL GAME HERE IN NY"
        else:
            blazersWereHomeTeam = homeTeamName == "Trail Blazers"
            homeTeamWon = int(float(homeTeamScore)) > int(float(awayTeamScore))
            if (homeTeamWon and blazersWereHomeTeam) or (not homeTeamWon and not blazersWereHomeTeam):
                if awayTeamName == "Lakers":
                    time.value = "SUCK IT LLLAKERS!"
                else:
                    time.value = "BLAZERS WIN!"
            else:
                time.value = "FINAL"
    updateTime = 1000
    if not liveGame:
        updateTime = 60000
    if not newGame:
        newGame = True
        logoSrc = gameDom.xpath('//img[@class="team-logo"]//@src')
        urllib.request.urlretrieve(logoSrc[0], "away_team.png")
        urllib.request.urlretrieve(logoSrc[1], "home_team.png")
        awayTeamLogo.value = "away_team.png"
        homeTeamLogo.value = "home_team.png"
    score.after(updateTime, main)

outerBox = Box(app,  height="fill")
innerBox = Box(outerBox, align="right")
scoreBox = Box(innerBox)
timeBox = Box(innerBox)
homeTeamLogo = Picture(scoreBox, image="home_team.png", align="left")
score = Text(scoreBox, "", size="30", align="left")
awayTeamLogo = Picture(scoreBox, image="away_team.png", align="left")
time = Text(timeBox, "", size=20)
score.after(1000, main)
app.display()