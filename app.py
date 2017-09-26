from flask import Flask,render_template,url_for

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("basic.html")


@app.route("/artists")
def artists():
    return "Artist info will be here"







if __name__=="__main__":
    app.run()
