from flask import Flask, request, jsonify
from flask_api import status
from pymongo import MongoClient
from bson import json_util, ObjectId
import configparser, datetime, json, os, subprocess

import switch_classes

app = Flask(__name__)

def get_db():
    client = MongoClient('mongodb://db:27017/', connect=False)
    return client.application_database

@app.route("/api/v1/ding", methods=['GET'])
def ding():
    return 'dong dong dong'

@app.route("/api/v1/ping", methods=['GET'])
def ping():
    return 'pong pong pong'

@app.route("/api/v1/switch-events", methods=['POST'])
def log_switch_events():
    try:
        uid = request.form["uid"]
        name = request.form["name"]
        action = request.form["action"]
        event_id = get_db().switchevents.insert_one({'uid':uid,'name': name,'action':action,'timestamp':datetime.datetime.utcnow()}).inserted_id
        return jsonify({"status": "success", "payload": str(event_id)})
    except Exception:
        return jsonify({"status": "failed", "payload": "Please insert a unique identifiy (uid) and name (name)"}),status.HTTP_400_BAD_REQUEST

@app.route("/api/v1/switch-events", methods=['GET'])
def get_switch_events():
    events = []
    for event in get_db().switchevents.find():
        events.append(event)
    sanitized_events = json.loads(json_util.dumps(events))
    return jsonify({"status": "success", "payload": sanitized_events})


@app.route("/api/v1/switch/<switch_id>", methods=['GET'])
def get_switch_info(switch_id):
    try:
        idx, last_event, events, response = 0, None, [], {}
        for event in get_db().switchevents.find({'uid': switch_id}).sort('timestamp',1):
            last_event = event
            events.append(event)
            idx = idx + 1
        sanitized_events = json.loads(json_util.dumps(events))
        response['state'], response['name'], response['history'] = last_event['action'], last_event['name'], sanitized_events
        return jsonify({"status": "success", "payload": response}),status.HTTP_200_OK
    except Exception as e :
        print (str(e))
        return jsonify({"status": "failed", "payload": "Bad Request", "exception": str(e)}),status.HTTP_400_BAD_REQUEST

@app.route("/api/v1/switch/<switch_id>", methods=['PUT'])
def switch_action(switch_id):
    try:
        config = configparser.ConfigParser()
        config.read("/project/server-conf/app.conf")
        rf_host = config.get("SWITCH", "Host")
        rf_port = config.get("SWITCH", "Port")
        action = request.form["action"]
        switch_cmd = "echo 'rf " + switch_id + " " + action + " '| nc " + rf_host + " " + rf_port 
        return jsonify({"status": "success", "payload": switch_cmd}),status.HTTP_202_ACCEPTED
        process = subprocess.Popen(switch_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = process.stderr.read()
        if err: 
            raise Exception (err)
        message = switch_id + " " + action.upper() + " accepted. executed: " + switch_cmd
        return jsonify({"status": "success", "payload": message}),status.HTTP_202_ACCEPTED
    except Exception as e :
        return jsonify({"status": "failed", "payload": "Bad Request", "exception": str(e)}),status.HTTP_400_BAD_REQUEST


myHouse = switch_classes.House('Richs Rad Pad')




if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
