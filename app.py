#Import packages
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

#Define webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    #Accept request payload
    req = request.get_json(silent=True, force=True)                             
    
    print("Request:")
    print(json.dumps(req, indent=4))
    
    #Call business logic    
    res = processRequest(req)                                                   

    #Prepare response message
    res = json.dumps(res, indent=4)
    r = make_response(res)                                                     
    r.headers['Content-Type'] = 'application/json'
    print(r)
    return r

#Execute business logic
def processRequest(req):

    # Check for correct action invocked
    if req.get("result").get("action") != "TrainRunningStatus":                  
        return {}
    
    # Extract input parameters
    result = req.get("result")                                                  
    parameters = result.get("parameters")
    inq_date = parameters.get("inq_date")
    cln_inq_date = inq_date.replace('-','')
    raw_train_num = parameters.get("train_num")
    train_num = raw_train_num.replace(" ","")
    key = os.getenv('API_KEY')
    
    # Prepare and call API URL
    link = "http://api.railwayapi.com/live/train/" + train_num + "/doj/" + cln_inq_date +"/apikey/" +key + "/"
    result = urllib.request.urlopen(link).read()
    data = json.loads(result)
                      
    # Extract train position
    raw_speech = data.get('position')                                            
    
    # Exception handling
    if (raw_speech == "-"):
        cln_speech = "Oops somthing went wrong, please try again later"
    else
        cln_speech = raw_speech
    
    #Prepare response speech
    speech = raw_train_num + "   " + cln_inq_date + "   " + cln_speech           
    
    return {
        "speech": speech,
        "displayText": speech,
        "source": "Indian Railway API"
    }

# Execute python app
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')


