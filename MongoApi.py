from flask import Flask,request,jsonify
from pymongo import MongoClient

client = MongoClient('127.0.0.1',27017)

db=client['hotel']
userCollections=db['users']
roomsCollection=db['rooms']

backend=Flask(_name_)

str_username='username'
str_password='password'

str_roomNumber ='roomNumber'
str_name='name'
str_adharNumber = 'adharNumber'
str_phoneNumber='phoneNumebr'

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

    roomsCollection.insert_one(dataDict)
    return 'data inserted'

@backend.route('/roomDetails')
def roomDetails():
    roomnumber=request.args.get(str_roomNumber)
    for i in roomsCollection.find({'_id':roomnumber}):
        dataDict={}
        dataDict[str_roomNumber] = i[str_roomNumber]
        dataDict[str_name]=i[str_name]
        dataDict[str_adharNumber]=i[str_adharNumber]
        dataDict[str_phoneNumber]=i[str_phoneNumber]

        return jsonify(dataDict)


@backend.route('/vacateRoom')
def vacateRoom():
    roomNumber=request.args.get(str_roomNumber)
    adharNumber=request.args.get(str_adharNumber)
    try:
         roomsCollection.delete_one({'_id':roomNumber,str_adharNumber:adharNumber})
         return 'room is now cleared'
    except:
        return 'data Not Found'

if(_name_ == '_main_'):
    backend.run('0.0.0.0',port=6969,debug=True)
