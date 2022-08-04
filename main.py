from smtplib import SMTP
import requests
from flask import Flask, render_template, request
from user_auth import USER_NAME, PASSWORD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



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


@app.route("/post/blog/<post_id>")
def get_blog(post_id):
    for entry in blog_json:
        if entry['id'] == int(post_id):
            post_body = entry['body']
            post_title = entry['title']
            post_subtitle = entry['subtitle']
            break
        else:
            post_body = "No entry found"
            post_title = "none"
    return render_template('post.html', subtitle=post_subtitle, title=post_title, body=post_body)


@app.route("/contact.html", methods=['POST', 'GET'])
def form():
    if request.method == 'GET':
        return render_template("contact.html")
    else:
        # Extract relevant information
        email = request.form['email']
        name = request.form['username']
        phone_number = request.form['phone-number']
        message_text = request.form['message']

        # Setup MIME
        message = MIMEMultipart()
        message['from'] = email
        message['to'] = USER_NAME
        message['subject'] = "New form submission!"
        message_content = message_text
        message.attach(MIMEText(message_content, 'plain'))

        string = message.as_string()

        # Send via smtlib
        with SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.starttls()
            smtp.login(user=USER_NAME, password=PASSWORD)
            smtp.sendmail(from_addr=email, to_addrs=USER_NAME, msg=string)
            smtp.quit()

        return "<h1>Successfully sent your message</h1>"





if __name__ == "__main__":
    app.run(debug=True)



