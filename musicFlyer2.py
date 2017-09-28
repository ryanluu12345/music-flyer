import requests
import json

class search:
    def __init__(self):
        self.accessToken = None
        self.artist = None
        self.artistUrl = None
        self.artistImage = None
        self.artistId = None
        self.songNames = {}
        self.artistEmbed = None
        
    def getAccessToken(self):
        url = 'https://accounts.spotify.com/api/token'
        clientID = '35f0eceb93b64bd99da23d2517513a37'
        clientSecret = 'ecdacecd08894c6f9f7cd07ed6e1b9c9'
        grantType = 'client_credentials'

        body_params = { 'grant_type': grantType}

        requestToken = requests.post(url, data = body_params, auth = (clientID, clientSecret))

        jsonData = json.loads(requestToken.text)
        accessToken = jsonData["access_token"]
        self.accessToken = accessToken
        
    def searchArtist(self, artist):
        searchUrl = 'https://api.spotify.com/v1/search'
        searchParams = { 'q': artist, 'type': 'artist'}
        headers = {"Authorization":"Bearer " + self.accessToken}
        requestArtist = requests.get(searchUrl, params = searchParams, headers =headers)
 
        jsonArtist = requestArtist.json()
        self.artist = jsonArtist
        self.artistUrl = jsonArtist["artists"]["items"][0]["external_urls"]["spotify"]
        self.artistImage = jsonArtist["artists"]["items"][0]["images"][0]["url"]
        self.artistId = jsonArtist["artists"]["items"][0]["id"]

    def addEmbedtoUrl(self, url):
        newUrl = url[0:25]+'embed/'+url[25:]
        return newUrl


    def searchArtistEmbed(self):
        searchUrl = 'https://api.spotify.com/v1/artists/'+self.artistId
        headers = {"Authorization":"Bearer " + self.accessToken}
        requestArtistInfo = requests.get(searchUrl, headers = headers)
        jsonArtist = requestArtistInfo.json()
        self.artistEmbed = self.addEmbedtoUrl(jsonArtist["external_urls"]["spotify"])
        print(self.artistEmbed)
        
    def searchArtistTopTracks(self):
        tracksUrl = 'https://api.spotify.com/v1/artists/'+self.artistId+'/top-tracks'
        tracksParams = { 'country': 'US' }
        headers = {"Authorization":"Bearer " + self.accessToken}
        requestArtistTopTracks = requests.get(tracksUrl, params = tracksParams, headers  = headers)
        jsonArtist = requestArtistTopTracks.json()
        for i in range (0,5):
            self.songNames[jsonArtist["tracks"][i]["name"]] = self.addEmbedtoUrl(jsonArtist["tracks"][i]["external_urls"]["spotify"])          
    def getArtist(self):
        return self.artist

    def getArtistUrl(self):
        return self.artistUrl

    def getArtistImage(self):
        return self.artistImage

    def getArtistId(self):
        return self.artistId
    
    def getSongNames(self):
        return self.songNames
    
    def getGenres(self):
        self.artist

    def getArtistEmbed(self):
        return self.artistEmbed

if __name__=="__main__":
    searched=search()
    searched.getAccessToken()
    searched.searchArtist("khalid")
    searched.searchArtistTopTracks()
    searched.searchArtistEmbed()
    #print(searched.getArtistImage())
  #  print(searched.getArtistId())
   # print(searched.getSongNames())
    
