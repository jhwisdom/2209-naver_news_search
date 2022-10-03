import os

from flask import Flask, render_template, request, redirect, send_file
from naver import naver_search
from save2file import save_to_file

app = Flask(__name__)

db = {}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    start_page = request.args.get("start_page")
    limit = request.args.get("limit")
    if start_page > limit:
        print("Wrong directive")
        return redirect("/")

    if keyword == None:
        return redirect("/")
    if keyword in db:
        news = db[keyword]
    else:
        result = naver_search(keyword, start_page, limit)
        print("search done")
        db[keyword] = result
        news = db[keyword]
    return render_template("search.html", keyword=keyword, news_lists=news)    
        
        
    
@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    print("saved")
    return send_file(f"{keyword}.csv", as_attachment=True)
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug = True)