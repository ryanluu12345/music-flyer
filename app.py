from flask import Flask,render_template,url_for,request,redirect
from genius import genius
from musicFlyer2 import search

app=Flask(__name__)

#Creates global lists that house artist information
blurbs=[]
artistFbs=""
artistTwitters=""
artistInstas=""
artistImg=""
artistDescription=""
artistSongs=""
artistTopSongs=""
errorText=None

#Variable for chosen artist info
artistName="Your Artist"

#Routes to the index
@app.route("/",methods=["POST","GET"])
def index():
    #Accesses global variables defined outside the function
    global artistName,artistImg,artistSongs,artistTopSongs,artistDescription,errorText

    if request.method=="POST":
        artistName=cleanString(request.form["artistName"])

        # Initializes genius and spotify to get data from the APIs
        GeniusCreator = genius()
        SpotifyCreator= search()

        #Accesses all information about a given artist
        try:
            SpotifyCreator.getAccessToken()
            SpotifyCreator.searchArtist(artistName)
            SpotifyCreator.searchArtistEmbed()
            SpotifyCreator.searchArtistTopTracks()
            SpotifyCreator.searchRelatedArtists()
            artistImg=SpotifyCreator.getArtistImage()
            artistSongs=SpotifyCreator.getSongNames()
            artistTopSongs=SpotifyCreator.getArtistEmbed()
            artistRelated=SpotifyCreator.getRelatedArtists()

            print(artistRelated)

            blurb, artistFb, artistTwitter, artistInsta, artistImgNone, artistDescription = GeniusCreator.getArtistInfo(
                artistName)
            addToLists(artistInsta)
            addToLists(artistFb)
            addToLists(blurb)
            addToLists(artistRelated)

            #Redirects to the artist page with all the info of artists
            return redirect(url_for("artists"))

        except:
            errorText="Please enter a valid artist name!"
            return render_template("index.html", errorText=errorText)

    return render_template("index.html",errorText=errorText)


#Routes to artist page with all the info and links to pages
@app.route("/artists")
def artists():
    global artistName,artistImg,artistSongs,artistTopSongs,artistDescription,errorText,blurbs
    return render_template("flyer.html",yourArtist=artistName,artistImg=artistImg,artistSongs=artistSongs,artistTopSongs=artistTopSongs,artistInsta=blurbs[0],artistFb=blurbs[1],blurb=blurbs[2],relatedArtists=blurbs[3])


#Method that appends items to a list since the list will later be used to provide info on a webpage
def addToLists(blurb):
    global blurbs
    blurbs.append(blurb)


#Cleans strings in order to get a capitalized version of words
def cleanString(string):

    string=string.split(" ")
    return ' '.join([word.capitalize() for word in string])



if __name__=="__main__":
    app.run()
