from flask import Flask, render_template, request, jsonify
from cassandra.cluster import Cluster
import json
import requests
import requests_cache
import pybase64

cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py')

#The twitter API requires a single key that is a string of a base64 encoded version
#of the two keys separated by a colon
client_key = app.config['CLIENT_KEY']
client_secret = app.config['CLIENT_SECRET']

key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = pybase64.standard_b64encode(key_secret).decode('ascii')

#/database/search/ returns the list of all tweets in the stored database through GET request
@app.route('/database/search/', methods=['POST','GET'])
def databasesearch():
    q = "Select * From tweettable.stats"
    q = list(session.execute(q))
    return jsonify(list(q))

#The UI asks user to enter the query in the URL
@app.route('/database')
def welcome():
    return('<h1>Hello, Enter in the URL to search the saved tweets: database/{query} </h1>')

#To search the results in the Cassandra database, User enters query in the form of database/{query}
@app.route('/database/<query>')
def profile(query):
    #Calling CQL select command from the database table tweettable to search for the query
    q = "Select * From tweettable.stats where Name = '{}' ".format(query)
    rows = list(session.execute(q))
    result = ""
    #Check if the record exists in the database or not, by checking the count of rows
    if len(rows) > 0:
        for e in rows:
            Header = str(e.name)+" was searched before, the result was :"
            User = str(e.datauser)
            Data = str(e.datatext)
            Fav = str(e.favourite)
            Ret = str(e.retweet)
    else:
        Header = "That query was not searched before!"
        User = "NA"
        Data = "NA"
        Fav = "NA"
        Ret = "NA"
    #Using the common HTML template to display the results on UI
    return render_template("tweetsearch.html",Header=Header, User=User, Data=Data, Fav=Fav, Ret=Ret)

#The main page is defined in the HTML template user interface, it takes query to search from the user
@app.route('/')
def welcomemain():
    IP = "The current IP is: " + str(request.remote_addr)
    return render_template('welcome.html')

@app.route('/tweetsearch', methods=['POST','GET'])
def tweetsearch():
    #For the entered query on the main UI page, search in the stored Cassandra database first
    query = request.form['text']
    qsql = "Select * From tweettable.stats where Name = '{}' ".format(query)
    rows = list(session.execute(qsql))
    result = ""
    #If record is found in the stored cassandra database, return the result from there, instead of connecting to external API
    if len(rows) > 0:
        for e in rows:
            Header = str(e.name)+" was searched before, returning the result from database :"
            User = str(e.datauser)
            Data = str(e.datatext)
            Fav = str(e.favourite)
            Ret = str(e.retweet)
        #Using the common HTML template to display the results on UI
        return render_template("tweetsearch.html",Header=Header, User=User, Data=Data, Fav=Fav, Ret=Ret)

    #As query result is not there in the database, connect to Twitter external API
    else:
        q = request.form['text']
        q = request.args.get('q', q)

        #to make a post request to the authentication endpoint
        #to obtain a Bearer Token to be included in subsequent API requests.
        base_url = 'https://api.twitter.com/'
        auth_url = '{}oauth2/token'.format(base_url)

        auth_headers = {
            'Authorization': 'Basic {}'.format(b64_encoded_key),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

        auth_data = {
            'grant_type': 'client_credentials'
        }

        auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

        # Check status code okay
        #print(auth_resp.status_code)

        # Keys in data response are token_type (bearer) and access_token (your access token)
        #print(auth_resp.json().keys())
        #print(auth_resp.json())

        access_token = auth_resp.json()['access_token']

        #Making Queries
        search_headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

        q = "'"+q+"'"
        search_params = {
            'q': q,                     #searched query parameter
            'result_type': 'popular',   #Ppopular tweet
            'lang':'en',                #English language
            'count': 1                  #returns one tweet
        }

        search_url = '{}1.1/search/tweets.json'.format(base_url)

        search_resp = requests.get(search_url, headers=search_headers, params=search_params)
        #print(search_resp.status_code)

        if search_resp.ok:
            tweet_data = search_resp.json()

            for s in tweet_data['statuses']:
                Header = "Fetching from Twitter live, The popular tweet for last seven days is :"
                User = str(s['user']['name'])
                Data = str(s['text'])
                Fav = str(s['favorite_count'])
                Ret = str(s['retweet_count'])
                #Store the results in the Cassandra database, by inserting the record
                session.execute("INSERT INTO tweettable.stats (ID, Name, Datatext, Datatime, Datauser, Favourite, Retweet) VALUES (20, '{}', '{}' , '{}', '{}', {}, {})".format(str(request.form['text']), s['text'], s['created_at'],s['user']['name'], s['favorite_count'], s['retweet_count']))

            #Using the common HTML template to display the search results on UI
            return render_template("tweetsearch.html",Header=Header, User=User, Data=Data, Fav=Fav, Ret=Ret)

        else:
            return render_template("tweetsearch.html",Header="", User="", Data="", Fav="", Ret="")

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080)
