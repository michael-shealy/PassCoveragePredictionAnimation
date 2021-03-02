# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 15:15:51 2021

@author: CaleShealy
"""

from flask import Flask, render_template, request
app = Flask(__name__)
#app.debug = True


@app.route('/', methods=['GET'])
def dropdown():
    colours = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('test.html', colours=colours)


if __name__ == "__main__":
    app.run()