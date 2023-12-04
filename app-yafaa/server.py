from flask import Flask
from flask import render_template
from datetime import datetime


app = Flask(__name__)


#****************** Home Page
@app.route('/')
def index_home():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var
    }
    return render_template('index.html', **additional_data)

#****************** Fixtures Page
@app.route('/fixtures')
def fixtures_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var
    }
    return render_template('fixture.html', **additional_data)


#****************** eng Page
@app.route('/eng')
def eng_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var,
        'active':'side-bar__list-item--active',
        'active_link':'eng'    
    }
    return render_template('fixt/eng.html', **additional_data)


#****************** fra Page
@app.route('/fra')
def fra_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var,
        'active':'side-bar__list-item--active',
        'active_link':'fra'    
    }
    return render_template('fixt/fra.html', **additional_data)


#****************** ger Page
@app.route('/ger')
def ger_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var,
        'active':'side-bar__list-item--active',
        'active_link':'ger'

    }
    return render_template('fixt/ger.html', **additional_data)

    #****************** esp Page
@app.route('/esp')
def esp_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var,
        'active':'side-bar__list-item--active',
        'active_link':'esp'

    }
    return render_template('fixt/esp.html', **additional_data)

    #****************** ita Page
@app.route('/ita')
def ita_func():
    date_var = datetime.now().year
    additional_data = {
        'current_date': date_var,
        'active':'side-bar__list-item--active',
        'active_link':'ita'

    }
    return render_template('fixt/ita.html', **additional_data)


if __name__ == '__main__':
    app.run(debug=True)
