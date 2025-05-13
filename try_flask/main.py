from flask import Flask,render_template
import random

ANIMAL=['dog','cat','capybara']

app=Flask('my_app')

@app.route('/hello/<animal>')
def greet(animal):

    return render_template('hello.html',who=animal)

@app.route('/squares')
def tabulate():

    tab=[]
    for n in range(10):
        tab.append((n,n*n))
    return render_template('table.html',values=tab,funcname='x^2')

app.run(debug=True)

