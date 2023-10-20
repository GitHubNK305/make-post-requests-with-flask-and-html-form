from flask import Flask, render_template, request, url_for
import smtplib
import requests

MY_EMAIL = "jintao.helsinki@gmail.com"
PASSWORD = "ufieqzafioenrwjx"

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    post_flag = False
    if request.method == "POST":
        post_flag = True
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="jintao.aalto@gmail.com",
                msg=f"Subject: New contact! \n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}."
            )
            connection.close()
        return render_template("contact.html", flag=post_flag)
    else:
        return render_template("contact.html", flag=post_flag)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
