from flask import Flask,render_template,url_for,request,redirect
from genius import genius

app=Flask(__name__)

#Creates global lists that house artist information
blurbs=[]
artistFbs=[]
artistTwitters=[]
artistInstas=[]
artistImgs=[]
artistDescriptions=[]

#Variable for chosen artist info
artistName="Your Artist"

@app.route("/",methods=["POST","GET"])
def index():
    global artistName

    if request.method=="POST":
        artistName=request.form["artistName"]
        return redirect(url_for("artists"))

    #Initializes genius to get data from the API
    GeniusCreator=genius()

    #Put this all in a loop later with all of the available songs
    songs=["Yellow Coldplay","Thats what I like","Broke Lecrae","Love me now John Legend"]
    blurb, artistFb, artistTwitter, artistInsta, artistImg,artistDescription =GeniusCreator.getArtistInfo(songs[0])
    addToLists(blurb,artistFb,artistTwitter,artistInsta,artistImg,artistDescription)

    return render_template("index.html",blurb=blurb,artistFb=artistFb,artistTwitter=artistTwitter,artistInsta=artistInsta)


@app.route("/artists")
def artists():
    global artistName

    return render_template("flyer.html",yourArtist=artistName)


#Method that appends items to a list since the list will later be used to provide info on a webpage
def addToLists(blurb,artistFb,artistTwitter,artistInsta,artistImg,artistDescription):
    blurbs.append(blurb)
    artistFbs.append(artistFb)
    artistTwitters.append(artistTwitter)
    artistInstas.append(artistInsta)
    artistImgs.append(artistImg)
    artistDescriptions.append(artistDescription)




if __name__=="__main__":
    app.run()
