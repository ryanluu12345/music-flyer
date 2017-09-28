from flask import Flask,render_template,url_for,request,redirect
from genius import genius
from spotify import search

app=Flask(__name__)

#Creates global lists that house artist information
blurbs=[]
artistFbs=""
artistTwitters=""
artistInstas=""
artistImg=""
artistDescriptions=""
artistSongs=""

#Variable for chosen artist info
artistName="Your Artist"

@app.route("/",methods=["POST","GET"])
def index():
    global artistName,artistImg,artistSongs

    if request.method=="POST":
        artistName=cleanString(request.form["artistName"])

        # Initializes genius and spotify to get data from the APIs
        GeniusCreator = genius()
        SpotifyCreator= search()

        SpotifyCreator.getAccessToken()
        SpotifyCreator.searchArtist(artistName)
        SpotifyCreator.searchArtistTopTracks()
        artistImg=SpotifyCreator.getArtistImage()
        artistSongs=SpotifyCreator.getSongNames()

        # Put this all in a loop later with all of the available songs
        songs = ["Yellow Coldplay", "Thats what I like", "Broke Lecrae", "Love me now John Legend"]
        blurb, artistFb, artistTwitter, artistInsta, artistImgNone, artistDescription = GeniusCreator.getArtistInfo(
            artistName)
        addToLists(blurb)

        return redirect(url_for("artists"))


    return render_template("index.html")


@app.route("/artists")
def artists():
    global artistName,artistImg,artistSongs
    return render_template("flyer.html",yourArtist=artistName,artistImg=artistImg,artistSongs=artistSongs)


#Method that appends items to a list since the list will later be used to provide info on a webpage
def addToLists(blurb):
    blurbs.append(blurb)


def cleanString(string):

    string=string.split(" ")
    return ' '.join([word.capitalize() for word in string])



if __name__=="__main__":
    app.run()
