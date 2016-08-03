'''
Created on Aug 3, 2016

@author: Thomas Adriaan Hellinger
'''
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scenarios')
def scenarios():
    return render_template('scenarios.html')

if __name__ == '__main__':
    app.run(debug=True)
    