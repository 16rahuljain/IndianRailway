from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print(r)
    return r

def processRequest(req):
    
    if req.get("result").get("action") != "TrainRunningStatus":
        return {}
    
    result = req.get("result")
    parameters = result.get("parameters")
    inq_date = parameters.get("inq_date")
    cln_inq_date = inq_date.replace('-','')
    train_num = parameters.get("train_num")
    
    link = "http://api.railwayapi.com/live/train/" + train_num + "/doj/" + cln_inq_date_date +"/apikey/1fb6d392/"
    resp = requests.get(link)
    jData = json.loads(resp.content)
    speech = jData['position']
    print speech
    
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "indian railway API"
    }


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')


