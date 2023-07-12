1. Clone the repository:

2. Change your directory to the cloned repository directory

   cd DocumentUploader

3. Create and activate virtual environment

    python -m venv venv 
    
   . venv/bin/activate

4. Install the project dependencies
    
   pip install -r requirements.txt

5. Run the application

   flask -app app run or python app.py

   The application will run on localhost:5000

   go to http://localhost:5000/uploaddocument to upload the document and specify the wordlenght.The document uploader only suppports .txt file for now.

   go to http://localhost:5000/displaywordcount to view the word count for the specified wordlength.
 
For the redis part

1.You have to install redis locally on your machine. Go to wsl on windows and type this command
  
sudo apt-get install redis

2.Start the redis server

sudo service redis-server start

** Always make sure redis is running before starting the python application.




