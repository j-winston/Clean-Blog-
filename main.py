import requests
from flask import Flask, render_template, request

app = Flask(__name__)


# Get blog posts
response = requests.get(url="https://api.npoint.io/1c1d666d0ff707b8e0d4")
blog_json = response.json()


@app.route("/")
def home():
    return render_template('index.html', blog_posts=blog_json)


@app.route("/about.html")
def about():
    return render_template("about.html")


@app.route("/contact.html")
def contact():
    return render_template("contact.html")


# for entry in blog_json:
#     @app.route(f"/{entry['title']}")
#     def post():
#         return render_template("post.html", post=entry.body)

@app.route("/post.html")
def post():
    return render_template("post.html", post=blog_json[1])


if __name__ == "__main__":
    app.run(debug=True)



