from flask import Flask,render_template,request,session,redirect,json
import urllib3


frontend = Flask(__name__)
frontend.secret_key="2b3c4d"

#defining backend
backend='127.0.0.1:6960'

signup_api = backend+'/signup'
login_api = backend+'/login'
br_api = backend+'/bookRoom'
vd_api = backend+'/roomDetails'
vcr_api = backend+'/vacateRoom'

#for homepage
@frontend.route('/')
def homepage():
    return render_template('home.html')

#for signup
@frontend.route('/signup')
def signup():
    return render_template('login.html')

#for login
@frontend.route('/login')
def login():
    return render_template('login.html')



#for booking room
@frontend.route('/bookRoom')
def bookroom():
    return render_template('roomDetails.html')


#for room details

@frontend.route('/roomDetails')
def roomDetails():
    return render_template('roomDetails.html')



#for vacating rooms

@frontend.route('/vacateRoom')
def vacateRoom():
    return render_template('roomDetails.html')





#for signup_api

@frontend.route('/signupform',methods=['post'])
def signupform():
    username=request.form['username']
    password=request.form['password']
    http=urllib3.PoolManager()
    respose=http.request('get',signup_api+'?username='+username+'&password='+password)
    respose=respose.data
    respose=respose.decode('utf-8')
    if respose=='Username Already exits':
        return render_template('login.html',res='Username Already exits')
    else:
        return render_template('roomDetails.html',res='Signup Successfull')

#for login_api
@frontend.route('/loginform',methods=['post'])
def loginform():
    username=request.form['username1']
    password=request.form['password1']
    http=urllib3.PoolManager()
    respose=http.request('get',login_api+'?username='+username+'&password='+password)
    respose=respose.data
    respose=respose.decode('utf-8')
    if respose=='You have enterd wrong details':
        return render_template('login.html',res1='login not')
    else:
        return render_template('roomDetails.html',res1='login done')


#for bookroom_api
@frontend.route('/bookroomform',methods=['post'])
def brform():
    roomno = request.form['bookRoomNumber']
    name = request.form['bookName']
    aadharno = request.form['bookAdharNumber']
    phoneno = request.form['bookPhoneNumber']
    print(roomno,name,aadharno,phoneno)

    http = urllib3.PoolManager()
    response = http.request('get',br_api+'?roomNumber='+roomno+'&name='+name+'&aadharNumber='+aadharno+'&phoneNumber='+phoneno)
    response = response.data
    response = response.decode('utf-8')
    if(response =='Room is already booked'):
        return render_template('roomDetails.html', err='Room is already booked')
    else:
        return render_template('roomDetails.html', res='Room is booked')

    




#for vd_api

@frontend.route('/viewdetailsform',methods=['post'])
def vdform():
    roomno = request.form['roomNumberDetails']
    http = urllib3.PoolManager()
    response = http.request('get',vd_api+'?roomNumber='+roomno)
    response=response.data
    response=response.decode('utf-8')
    response=json.loads(response)
    print (response)
    roomNumber=response['roomNumber']
    name=response['name']
    aadharNumber=response['aadharNumber']
    phoneNumber=response['phoneNumber']
    return render_template('roomDetails.html',roomNumber=roomNumber,name=name,aadharNumber=aadharNumber,phoneNumber=phoneNumber)


#for vcr_api

@frontend.route('/vacateroomform',methods=['post'])
def vcr():
    roomno=request.form['vacateRoomNumber']
    aadharno=request.form['vacateAdharNumber']
    http = urllib3.PoolManager()
    response = http.request('get',vcr_api, fields={'roomNumber':roomno , 'aadharNumber':aadharno})
    response = response.data.decode('utf-8')

    return render_template('roomDetails.html' , res2='Room Vacated')

if __name__=='__main__':
    frontend.run(host='0.0.0.0',port=6961,debug=True)
