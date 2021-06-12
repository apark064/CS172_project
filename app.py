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
        print('a')
        output = ""
        # call ES with seed_url, query
        outputVal = crawler.elas(seed_url, query)
        print('b')
        for i in range(len(outputVal)):
            print('Document ' + str(i + 1))
            print('    ID: ' + outputVal[i]['_id'])  # result status
            scoreOutput = '    Score: ' + str(outputVal[i]['_score'])
            urlOutput = '    URL: ' + outputVal[i]['_source']['url']
            print(scoreOutput)
            print(urlOutput)
            # print('    Score: ' + str(outputVal[i]['_score']))
            # print('    URL: ' + outputVal[i]['_source']['url'])
            output += scoreOutput + urlOutput + "<br>"
        print("================================================ \n" + output)
        return output

    # elif request.method == 'GET':
    #     for i in range(len(response['hits']['hits'])):
    #         print('Document ' + str(i + 1))
    #         print('    ID: ' + response['hits']['hits'][i]['_id'])  # result status
    #         print('    Score: ' + str(response['hits']['hits'][i]['_score']))
    #         print('    URL: ' + response['hits']['hits'][i]['_source']['url'])
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
