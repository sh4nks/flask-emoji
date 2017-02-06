from flask import Flask, render_template
from flask_emoji import Emoji

# Default Settings
SECRET_KEY = "this-key-is-not-secure"

app = Flask(__name__)
app.config.from_object(__name__)

emoji = Emoji(app)


markdown_text = """
**Markdown Example**

Powered by [mistune](https://github.com/lepture/mistune).

Its raining :cat:s and :dog:s.
"""

standalone_text = """
Standalone example <br />

Its raining :cat:s and :dog:s.
"""


@app.route("/")
def index():
    return render_template("index.html", markdown=markdown_text,
                           standalone=standalone_text)


if __name__ == "__main__":
    app.run(debug=True)
