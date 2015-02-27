from flask import Flask, render_template
from flask_emoji import Emoji

# Default Settings
SECRET_KEY = "this-key-is-not-secure"

app = Flask(__name__)
app.config.from_object(__name__)
emoji = Emoji(app)

test_single = ":smile:"
test_multiple = ":smile: :smiley:"
test_other = "![test](test.png) ![test2](test2.png)"

print "Single Emoji:"
print emoji.render_mistune(test_single)

print "Multiple in one line:"
print emoji.render_mistune(test_multiple)

print "Other:"
print emoji.render_mistune(test_other)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bbcode")
def bbcode():
    return render_template("bbcode.html")


@app.route("/markdown")
def markdown():
    return render_template("markdown.html")


if __name__ == "__main__":
    app.run(debug=True)
