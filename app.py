from flask import Flask, render_template
from views import user_api

app = Flask(__name__)
app.register_blueprint(user_api.user)

@app.route("/")
def home():
    return render_template('main.html')



if __name__ == "__main__":
    app.run(debug=True)