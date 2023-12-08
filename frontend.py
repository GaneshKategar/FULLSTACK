from flask import Flask,render_template,request,session,redirect
import urllib3
import json


frontend = Flask(__name__)


#defining backend
backend='127.0.0.1:6969'

signup_api = backend+'/signup'
login_api = backend+'/login'
br_api = backend+'/bookroom'
vd_api = backend+'/viewdetails'
vcr_api = backend+'/vacateRoom'

#for homepage
@frontend.route('/')
def homepage():
    return render_template('random.html')



#for booking room
@frontend.route('/bookRoom')
def bookroom():
    return render_template('random.html')


#for room details

@frontend.route('/roomDetails')
def roomDetails():
    return render_template('random.html')



#for vacating rooms

@frontend.route('/vacateRoom')
def vacateRoom():
    return render_template('random.html')





#for signup_api

@frontend.route('/signupform',methods=['post'])
def signupform():
    username = request.form('username')
    password = request.form('password')

    http = urllib3.PoolManager
    response = http.request('get',signup_api+'?username='+username+'&password='+password)  
    # change the username and password in the string if data is not sent bcz of different name in get of backend server
    response = response.data
    response = response.decode('utf-8')


    #return to where you wanna go after login
    return render_template('')


#for login_api
@frontend.route('/loginform',methods=['post'])
def loginform():
    username = request.form('username1')
    password = request.form('password1')

    http = urllib3.PoolManager
    response = http.request('get',login_api+'?username='+username+'&password='+password)

    reponse = response.data
    response = response.decode('utf-8')

    return render_template('')


#for bookroom_api
@frontend.route('/bookroomform',methods=['post'])
def brform():

    roomno = request.form['bookRoomNumber']
    name = request.form['bookName']
    aadharno = request.form['bookAdharNumber']
    phoneno = request.form['bookPhoneNumber']
    print(roomno,name,aadharno,phoneno)

    http = urllib3.PoolManager()
    response = http.request('get',br_api+'?roomnumber='+roomno+'&name='+name+'&aadharNumber='+aadharno+'&phoneNumber='+phoneno)
    response = response.data
    response = response.decode('utf-8')
    print(response)

    return render_template('random.html', res='Room Booked')




#for vd_api

@frontend.route('/viewdetailsform',methods=['post'])
def vdform():
    roomno = request.form['roomNumberDetails']
    print(roomno)
    http = urllib3.PoolManager()
    response = http.request('get',vd_api+'?roomno')
    response = response.data.decode('utf-8')
    print(response)

    return render_template('random.html',data=response,res1='Details displayed')


#for vcr_api

@frontend.route('/vacateroomform',methods=['post'])
def vcr():
    roomno=request.form['vacateRoomNumber']
    aadharno=request.form['vacateAdharNumber']
    http = urllib3.PoolManager()
    response = http.request('get',vcr_api, fields={'roomNumber':roomno , 'adharNumber':aadharno})
    response = response.data.decode('utf-8')

    return render_template('random.html' , res2='Room Vacated')


if __name__=='__main__':
    frontend.run(host='0.0.0.0',port=6960,debug=True)



