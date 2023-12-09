from flask import Flask,request,jsonify
from pymongo import MongoClient

client = MongoClient('127.0.0.1',27017)

db=client['hotel']
userCollections=db['users']
roomsCollection=db['rooms']
feedbackCollection=db['feedback']

backend=Flask(__name__)

str_username='username'
str_password='password'

str_roomNumber ='roomNumber'
str_name='name'
str_adharNumber = 'aadharNumber'
str_phoneNumber='phoneNumber'

@backend.route('/')
def homepage():
    return 'server is running'

@backend.route('/signup',methods=['get'])
def signup():
    username=request.args.get(str_username)
    password=request.args.get(str_password)
    dataDict={}
    dataDict['_id'] = username
    dataDict[str_username]=username
    dataDict[str_password]=password
    try:
        userCollections.insert_one(dataDict)
        return 'Signup Successful'
    except:
        return 'Username Already exits'

@backend.route('/login',methods=['get'])
def login():
    username=request.args.get(str_username)
    password=request.args.get(str_password)
    flag = 0
    for i in userCollections.find({'_id':username}):
        if(password == i[str_password]):
            flag=1
            return 'You are logged in '
    if flag == 0:
        return 'You have enterd wrong details'

@backend.route('/bookRoom')
def bookroom():
    roomnumber=request.args.get(str_roomNumber)
    name=request.args.get(str_name)
    adharNumber=request.args.get(str_adharNumber)
    phoneNumber=request.args.get(str_phoneNumber)

    dataDict={}
    dataDict['_id']=roomnumber
    dataDict[str_roomNumber] = roomnumber
    dataDict[str_name]=name
    dataDict[str_adharNumber]=adharNumber
    dataDict[str_phoneNumber]=phoneNumber
    try:
        roomsCollection.insert_one(dataDict)
        return 'data inserted'
    except:
        return 'Room is already booked'


@backend.route('/roomDetails')
def roomDetails():
    roomnumber = request.args.get(str_roomNumber)
    try:
        room_document = roomsCollection.find_one({'_id': roomnumber})
    except:
        return jsonify({"error": "Room is not booked"}), 404
    if room_document:
        dataDict = {
            str_roomNumber: room_document[str_roomNumber],
            str_name: room_document[str_name],
            str_adharNumber: room_document[str_adharNumber],
            str_phoneNumber: room_document[str_phoneNumber]
        }

        return jsonify(dataDict)
    else:
        # Handle the case where the room is not found
        return jsonify({"error": "Room not found"}), 404


@backend.route('/vacateRoom')
def vacateRoom():
    roomNumber=request.args.get(str_roomNumber)
    adharNumber=request.args.get(str_adharNumber)
    try:
         roomsCollection.delete_one({'_id':roomNumber,str_adharNumber:adharNumber})
         return 'room is now cleared'
    except:
        return 'data Not Found'

@backend.route('/deleteEverything', methods=['get'])
def delete_all_room_details():
    try:
        # Delete all documents from the roomsCollection collection
        roomsCollection.delete_many({})
        userCollections.delete_many({})
        return 'All room details deleted successfully'
    except:
        return 'Error deleting room details'

@backend.route('/all', methods=['get'])
def all_room_details():
    all_room_data = []
    for room in roomsCollection.find():
        room_data = {
            str_roomNumber: room[str_roomNumber],
            str_name: room[str_name],
            str_adharNumber: room[str_adharNumber],
            str_phoneNumber: room[str_phoneNumber]
        }
        all_room_data.append(room_data)

    return jsonify(all_room_data)

@backend.route('/feedback',)
def feedback():
    feedback=request.args.get('feedback')
    feedbackCollection['feedback'] = feedback
    return str(feedback)

if(__name__ == '__main__'):
    backend.run('0.0.0.0',port=6960,debug=True)
