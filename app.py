from feature import *

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"msg": "active"})

@app.route('/months', methods=['GET'])
def get_months(year: int):
    if not year:
        raise ValueError("You need to pass a year.")
    else:
        pass
            

if __name__ == '__main__':
   #search(url='www.google.com', year=1998, day=2, month_name='DEC')
   app.run(debug=True)