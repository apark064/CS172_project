from flask import Flask, render_template, url_for, request
import crawler
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        seed_url = request.form['seed_url']
        query = request.form['query']
        dict = {'seed': seed_url, 'query': query}

        # call ES with seed_url, query
        crawler.elas(seed_url, query)
        return dict
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
