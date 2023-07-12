from flask import Flask,request,render_template,redirect
import os
import redis
import json
import time
import threading
import re
app=Flask(__name__)

app.config['document_upload']='documents'

redis_client=redis.Redis(host='localhost', port=6379)

'''
This route handles the functionlaity for uploading the document 

Steps

First the user selects a document and specifies the desired word length.Then a check is done to see if its a .txt file.

If it passes the check the file gets uploaded and stored in local storage

Then a message is published to the redis broker that a new file is available.

'''

def checkextension(file):
    filextension=file.filename.split('.')[1]
    if filextension=='txt':
        return True
    else:
        return False

@app.route("/uploaddocument",methods=["GET","POST"])

def upload_document():
    if request.method == "POST":
        wordlength = request.form['wordlength']
        if request.files:
            file=request.files['document']
            if checkextension(file):
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['document_upload'],file.filename))
                location=os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['document_upload'])


                message={"filename":file.filename,'location':location,"wordlength":wordlength}

                redis_client.publish('newdocument',json.dumps(message))

                return redirect(request.url)
            else:
                return render_template('error.html')
    else:
        return render_template('upload_document.html')


def update_data(message):
    file=open('wordcounthistory.txt','a')
    file.write(message+'\n')


'''
This function handles the processing of the word document.
It counts the number of words of the specifed word length by user and then store it in a file in localstorage.

'''

def process_document(filename,location,wordlength):
    filename=filename
    file=open(location+"\\"+filename,'r',encoding='utf-8')
    words=[]
    new_word_list=[]
    for i in file:
        if i=='.':
            i.replace(i,i+' ')
        words = i.split(" ")
    print(words)
    for word in words:
        cleaned_word = re.sub(r'[^\w\s]', '',
                              word)
        if cleaned_word:
            new_word_list.append(cleaned_word)
    print(new_word_list)
    wordlength=int(wordlength)
    cnt=0
    for word in new_word_list:
        wl=len(word)

        if wl==wordlength:
            cnt+=1
    message=f'{filename} has  {cnt} words of wordlength {wordlength}'
    update_data(message)


'''
This function handles the communication between uploader and worker service

Steps

it keeps running in the background to listen if any new file is available

if a file becomes available it sends the file with its filename,location and wordlenght to the worker service for processing.

'''
def handle_broker():
    while True:
        print("Test")

        pubsub=redis_client.pubsub()
        pubsub.subscribe('newdocument')
        for message in pubsub.listen():
            if message['type'] == 'message':
                document = message['data'].decode('utf-8')
                des_message=json.loads(document)
                filename=des_message['filename']
                location=des_message['location']
                wordlength=des_message['wordlength']

                process_document(filename,location,wordlength)



'''
This route is for displaying the word counts
'''

@app.route('/displaywordcount',methods=['GET'])
def display_wordcount():
    file = open('wordcounthistory.txt', 'r')
    resultlist=[]
    for i in file:
        resultlist.append(i)
    resultlist=resultlist[::-1]
    return render_template('word_counts.html',resultlist=resultlist)




t = threading.Thread(target=handle_broker)
t.start()


if __name__=='__main__':
    app.run(debug=True)



