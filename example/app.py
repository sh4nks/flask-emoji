from flask import Flask, render_template
from flask_emoji import Emoji, render_mistune, render_bbcode

# Default Settings
SECRET_KEY = "this-key-is-not-secure"

app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.filters["render_mistune"] = render_mistune
app.jinja_env.filters["render_bbcode"] = render_bbcode

emoji = Emoji(app)

bbcode_text = """
[b]BBCode Example[/b]

Powered by [url=https://github.com/dcwatson/bbcode]bbcode[/url].

Its raining :cat:s and :dog:s.
"""

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
    return render_template("index.html", bbcode=bbcode_text,
                           markdown=markdown_text, standalone=standalone_text)


if __name__ == "__main__":
    app.run(debug=True)
