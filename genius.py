''' Module that focuses on extracting contextual data from the genius website to be used on our webpage'''
import requests
import time
import json

class genius:

    def __init__(self):
        self.baseUrl="https://api.genius.com"
        self.CLIENT_ACCESS_TOKEN="YT_ZO2npD-RqvQOm9PJQhUXhY0b1Shnht3QqPAIXflUeuTy8_s5OCEdEMSgmfRaY"
        self.headers={}
        self.artistPath=""
        self.blurb=""
        self.artistTwitter=""
        self.artistInsta=""
        self.artistFb=""
        self.artistImg = ""
        self.artistDescription=""


    def getJson(self,path,params=None,headers=None):

        #Joins the base URL with the inputted path
        url="/".join([self.baseUrl,path])

        print(url)

        #Sets the bearer field with the client access token
        token="Bearer {}".format(self.CLIENT_ACCESS_TOKEN)

        #Checks for authorization
        if self.headers:
            self.headers["Authorization"]=token
        else:
            self.headers={"Authorization":token}

        # Gets repsonse from the path to the data
        response=requests.get(url=url,params=params,headers=self.headers)
        response.raise_for_status()

        return response.json()

    def getArtistInfo(self,song):

        #Builds the path for the search method
        basePath="search?q="
        queryPath=basePath+song

        #Gets the JSON response of the search result
        songInfo=self.getJson(queryPath)
        self.artistPath=songInfo["response"]["hits"][0]["result"]["primary_artist"]["api_path"]
        id=songInfo["response"]["hits"][0]["result"]["id"]
        print(self.artistPath)

        #Gets the artist information
        self.getArtist(self.artistPath)


        self.getSong(id)

        '''print(self.blurb)
        print(self.artistFb)
        print(self.artistTwitter)
        print(self.artistInsta)
        print(self.artistDescription)
        print(self.artistImg)'''

        return self.blurb,self.artistFb,self.artistTwitter,self.artistInsta,self.artistImg,self.artistDescription


    #Gets the annotation from the chosen song
    def getSong(self,id):
        songPath="songs/{}".format(id)
        self.blurb=self.getJson(songPath)["response"]["song"]["description"]["dom"]["children"][0]["children"][0]

    #Gets artist information
    def getArtist(self,artistPath):

        #Gets the response body from the artist path
        artistData=self.getJson(artistPath[1:])["response"]["artist"]
        self.artistFb="https://www.facebook.com/{}".format(artistData["facebook_name"])
        self.artistTwitter = "https://www.twitter.com/{}".format(artistData["twitter_name"])
        self.artistInsta = "https://www.instagram.com/{}".format(artistData["instagram_name"])
        self.artistImg=artistData["image_url"]
        self.description= artistData["description"]["dom"]["children"][0]["children"][0]



    def getAnnotations(self,id):
        print(self.getJson(id))
        return





if __name__=="__main__":

    #Remember to make the search query a combination of the song name and the artists name
    GeniusLoader=genius()
    songs=["Yellow Coldplay","Thats what I like","Broke Lecrae","Love me now John Legend"]

    for song in songs:
        GeniusLoader.getArtistInfo(song)