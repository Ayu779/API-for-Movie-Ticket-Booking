# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 16:35:51 2020

@author: Ayush Saxena
"""
import flask
import json
import re
import time
import datetime
from bson.json_util import dumps
from flask import Flask, request,jsonify
from pymongo import MongoClient
from bson.objectid import *

def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False
    
app = Flask(__name__)

#mongoclient
client = MongoClient(host='localhost', port=27017)
db = client.moviedb	 #database
tickets = db.tickets
if "timings" not in db.list_collection_names():
    timings = db.timings
    timings.insert_one({"timing": "09:00", "slot" : 20})
    timings.insert_one({"timing": "10:00", "slot" : 20})
    timings.insert_one({"timing": "11:00", "slot" : 20})
    timings.insert_one({"timing": "12:00", "slot" : 20})
    timings.insert_one({"timing": "13:00", "slot" : 20})
    timings.insert_one({"timing": "14:00", "slot" : 20})
    timings.insert_one({"timing": "15:00", "slot" : 20})
    timings.insert_one({"timing": "16:00", "slot" : 20})
    timings.insert_one({"timing": "17:00", "slot" : 20})
    timings.insert_one({"timing": "18:00", "slot" : 20})
    timings.insert_one({"timing": "19:00", "slot" : 20})
    timings.insert_one({"timing": "20:00", "slot" : 20})
    timings.insert_one({"timing": "21:00", "slot" : 20})
timings = db.timings
#automatically deletes the expired ticket using TTL (time to live)
tickets.create_index("activation", expireAfterSeconds=28800) 
l= []
stri =''
@app.route('/', methods = ['GET'])
def viewslotsandtime():
    if request.method == 'GET':
        output = timings.find()
        for i in output:
            global stri 
            stri = stri + i['timing'] + " : " + str(i['slot']) + "\n"
        return stri

@app.route('/booktickets' , methods = ['POST'])
def book():
    data = request.json
    user_name = data.get('name','')
    phone = data.get('phone', '')
    timing = data.get('timing','')
    
    #checking input
    missing = []
    if user_name == '':
        missing.append("U")
    if phone == '':
        missing.append("P")
    if timing == '':
        missing.append("T")
    
    if len(missing) > 0:
        strii =''
        if 'U' in missing:
                strii = strii + "{'message' : 'No Username'}    "
        if 'P' in missing:
                strii = strii + "{'message' : 'No Phone'}    " 
        if 'T' in missing:
                strii = strii + "{'message' : 'No Timing'}"
        return jsonify(strii)
    
    error =[]
    reph = "^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$"
    if not re.search(reph, phone):
        error.append('P')
    if not isTimeFormat(timing):
        error.append('T')
    #checking valid  input
    if len(error) >0:
        strii=''
        if 'P' in error:
            strii = strii + "{'message' : 'Not valid Phone Number'}"
        if 'T' in error:
            strii = strii + "{'message' : 'Not valid TimeFormat, Valid Time Format is *HH:MM*'}"
        return jsonify(strii)
    hour = int(timing.split(':')[0])
    minute = int(timing.split(':')[1])
    print(hour,minute)
    if  hour < 9 or hour > 21 or minute != 0:
        response = {'alert' : 'No shows available at the time. Please go to http://127.0.0.1:5000/ to see available shows.'}
        return jsonify(response)
    try:
        checkvariable = timings.find({'timing' : timing})
        cv = 0
        for i in checkvariable:
            cv= int(i['slot'])
        if cv > 0:
            tickets.insert_one({'name' : user_name, 'phone' : phone, 'timing' : timing, 'activation' : datetime.datetime.utcnow() })
            timings.update_one({'timing' : timing},{'$inc': { 'slot': -1 } })
            for ii in tickets.find({'name': user_name}):
                idd = ii['_id']
            response = {"alert" : f"Ticket has been successfully booked. Ticket ID : {str(idd)}"}
            return jsonify(response)
        else: 
            response = {"alert" : "Sorry! All the slots have been already booked. No Seat Left"}
            return jsonify(response)
    except Exception as e:
        response = {'alert' : str(e)}
        return jsonify(response)
    

@app.route('/update', methods = ['POST'])
def updatetiming():
    error = []
    data = request.json
    ticket_id = data.get('ticket_id', '')
    phone = data.get('phone', '')
    timing_alter = data.get('time_alter', '' )
    
    #valid input
    reph = "^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$"
    if phone == '':
        error.append('NP')
    elif not re.search(reph, phone):
        error.append('P')
    if ticket_id == '':
        error.append('I')
    if timing_alter == '':
        error.append('TA')
    elif not isTimeFormat(timing_alter):
        error.append('T')
    if len(error) > 0:
        stre =''
        for i in error:
            if i == 'NP':
                stre = stre + "{'message' : 'No Phone'} "
            elif i == "P":
                stre = stre + "{'message' : 'Not valid Phone Number'} "
            elif i == "I":
                stre = stre + "{'message' : 'No Ticket ID'} "
            elif i == "TA":
                stre = stre +  "{'message' : 'No Time Provided'} "
            elif i == "T":
                stre = stre + "{'message' : 'Not valid TimeFormat, Valid Time Format is *HH:MM*'}"
        return jsonify(stre)
    
    #ticket altering time
    
    else:
        list1 = ''
        list2 =''
        x = tickets.find_one({"$and" : [{'_id': ObjectId(ticket_id)},{'phone': phone}]})
        if x is not None: #if exists
            list1 = ticket_id
            list2 = phone
        else: #if not exists
            if tickets.find_one({'_id': ObjectId(ticket_id)}):
                response = {"alert" : "Wrong Phone Number"}
                return jsonify(response)
            elif tickets.find_one({'phone': phone}):
                response = {"alert" : "Ticket ID do not exist"}
                return jsonify(response)
        hour = int(timing_alter.split(':')[0])
        minute = int(timing_alter.split(':')[1])
        if  hour < 9 or hour > 21 or minute != 0:
            response = {'alert' : 'No shows available at the time. Please go to http://127.0.0.1:5000/ to see available shows.'}
            return jsonify(response)
        else:
            timm =str(tickets.find_one({'_id': ObjectId(ticket_id)})['timing'])
            cv = int(timings.find_one({'timing' : timing_alter})['slot'])
            qqq = str(timings.find_one({'timing' : timm})['timing'])
            print(qqq, cv)
            if cv > 0 and qqq:
                tickets.update_one({'_id' : ObjectId(ticket_id)}, {'$set' : {'timing' : timing_alter}})
                timings.update_one({'timing' : timing_alter},{'$inc': { 'slot': -1 } })
                timings.update_one({'timing' : qqq},{'$inc': { 'slot': 1 } })
                response = {"alert" : "Time updated properly"}
                return jsonify(response)
            else: 
                response = {"alert" : "Sorry! All the slots have been already booked. No Seat Left"}
                return jsonify(response)
      

@app.route('/delete' , methods = ['POST'])
def deleteticket(): 
    data = request.json
    ticket_id = data.get('ticket_id', '')
    phone = data.get('phone', '')
    error = []
    
    #valid input
    reph = "^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$"
    if phone == '':
        error.append('NP')
    elif not re.search(reph, phone):
        error.append('P')
    if ticket_id == '':
        error.append('I')
    if len(error) > 0:
        stre =''
        for i in error:
            if i == 'NP':
                stre = stre + "{'message' : 'No Phone'} "
            elif i == "P":
                stre = stre + "{'message' : 'Not valid Phone Number'} "
            elif i == "I":
                stre = stre + "{'message' : 'No Ticket ID'} "
        return jsonify(stre)
    else:
        list1 = ''
        list2 =''
        x = tickets.find_one({"$and" : [{'_id': ObjectId(ticket_id)},{'phone': phone}]})
        if x is not None: #if exists
            list1 = ticket_id
            list2 = phone
        else: #if not exists
            if tickets.find_one({'_id': ObjectId(ticket_id)}):
                response = {"alert" : "Wrong Phone Number"}
                return jsonify(response)
            elif tickets.find_one({'phone': phone}):
                response = {"alert" : "Ticket ID do not exist"}
                return jsonify(response)
            
        timm =str(tickets.find_one({'_id': ObjectId(ticket_id)})['timing'])
        qqq = str(timings.find_one({'timing' : timm})['timing'])
        if qqq:
            timings.update_one({'timing' : qqq},{'$inc': { 'slot': 1 } })
            tickets.delete_one({'_id': ObjectId(ticket_id)})
            response = {'alert' : 'Ticket Deleted Successfully!'}
            return jsonify(response)

@app.route('/viewontime', methods = ['POST'])
def view():
    data = request.json
    timing = data.get('timing','')
    stre = ''
    if timing == '':
        stre = stre +  "{'message' : 'No Time Provided'} "
    elif not isTimeFormat(timing):
        stre = stre + "{'alert' : 'Not valid TimeFormat, Valid Time Format is *HH:MM*'}"
    hour = int(timing.split(':')[0])
    minute = int(timing.split(':')[1])
    if  hour < 9 or hour > 21 or minute != 0:
        response = {'alert' : 'No shows available at the time. Please go to http://127.0.0.1:5000/ to see available shows.'}
        return jsonify(response)
    else:
        res = tickets.find({'timing' : timing},{"_id" : 0})
        if len(list(res)) > 0:
            response = {
			'data' : list(tickets.find({'timing' : timing},{"_id" : 0}))
            }
            return jsonify(response)
        else:
             response = {'alert' : 'No ticket booked on the given time'}
             return jsonify(response)
    
@app.route('/viewuser', methods = ['POST'])
def viewuser():
    stre = ''
    data = request.json
    ticket_id = data.get ('ticket_id', '')
    if ticket_id =='':
        stre = "{'alert' : 'Please provide a ticket ID'}"
        return jsonify(stre)
    else:
        res = tickets.find_one({'_id' : ObjectId(ticket_id)}, {'_id' : 0})
        if len(list(res)) > 0:
            name = tickets.find_one({'_id' : ObjectId(ticket_id)}, {'_id' : 0})["name"]
            phone =tickets.find_one({'_id' : ObjectId(ticket_id)}, {'_id' : 0})["phone"]
            timing = tickets.find_one({'_id' : ObjectId(ticket_id)}, {'_id' : 0})["timing"]
            response= {'Name' : name, 'Phone' : phone, 'Timing': timing}
            return jsonify(response)
            
if __name__ == '__main__':
	app.run(debug=True)