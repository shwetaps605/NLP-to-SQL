from br2_spacy import generate_data

#import files
from flask import Flask, render_template, request

application =app = Flask(__name__)

@app.route("/")
def home():    
    return render_template("home.html") 
@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')
    print(userText) 
    data=generate_data(userText.lower())
    data=data.replace("\n","<br/>")
    data=data.replace("\t","&nbsp")
    print(data)  
    if (len(data)==0):
        return ("No result found, try again!")  
    else:
        return data
if __name__ == "__main__":    
    app.run()