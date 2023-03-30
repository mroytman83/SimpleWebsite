from flask import Flask, render_template, request, redirect, url_for, session
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import services as dbc

os.environ['TWILIO_ACCOUNT_SID'] = 'AC67a4e9bf51b0741e691e617b1f07dd4a'
os.environ['TWILIO_AUTH_TOKEN'] = 'de17072d22404edd9096aa83f524e1aa'


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


app = Flask(__name__)
app.secret_key = 'thisisacomplicatedkey'

# Visual element, for developers only
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sms", methods=['POST'])
def	inbound_sms():
    resp = MessagingResponse()
    session['contact'] = 'https://www.bolic.io/'
    # Get the message from the user sent to our Twilio number
    body = request.values.get('Body', None)
    number = request.values.get('From', None)

    print(number)
    print(body)
    print(type(body))
    contact = session['contact']
    

    if(body=="STOP"):
        # Opt out of Bolic texts
        resp.message("You have chosen to Opt-out of Bolic. We're sorry to see you go, goodbye!")
        print(str(resp))
        return str(resp)

    # messages = client.messages.list(limit=20)
    # for record in messages:
    #     print(record.sid)
    
    
    resp.message(f'your message was {body}, we will get back to you shortly! If this is urgent, please contact us at {contact}')
    print(str(resp))
    return str(resp)

# test api endpoint
@app.route('/api')
def api():
    return{'API_KEY' : 'lmfao'}

# select query: query the database with any select sql query
@app.route('/signup', methods=['GET'])
def signup():
    return render_template("form.html")

@app.route('/submit', methods=['POST'])
def submit():
    # Get the data from the form
    username = request.form['username']
    password = request.form['password']
    session['username'] = username
    session['password'] = password
    # Do something with the data (e.g. store it in a database)
    print(f' Hi! {username}! Nice to meet you!')
    # Redirect the user to optin page
    return redirect('optin')

@app.route('/submit/optin', methods=['POST'])
def submit_optin():
    # Get the data from the form
    number = request.form['number']
    print(f' Hi! {number}! Nice to meet you!')
    ret = dbc.load_and_connect()
    print(ret)
    data = dbc.insert_phone_number(number)

    # Redirect the user to a thank you page
    return """
    <html><body>
    <h2> Thank you! Your information has been recorded </h2>
    </body></html>
    """

@app.route('/get/numbers')
def get_numbers():
    # Get the data from the form
    ret = dbc.load_and_connect()
    print(ret)
    data = dbc.fetch_records()
    return data

@app.route('/forgot')
def forgot():    
    return render_template('forgotpwd.html')

@app.route('/optin', methods=['GET', 'POST'])
def thankyou():
    if(request.method=='POST'):
        number = request.form['number']
        print(number)
    return render_template("optin.html", username=session['username'])


@app.route('/terms-of-service')
def termsofservice():
    return render_template("tos.html")

@app.route('/privacy-policy')
def privacy():
    return render_template("privacy-policy.html")

@app.route('/contact-us')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


             
