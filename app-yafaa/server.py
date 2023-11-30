from flask import Flask
from flask import render_template
from datetime import datetime



app = Flask(__name__)

@app.route('/')
def index_home():
    date_var = datetime.now().year

    additional_data = {
        'current_date': date_var
    }
    return render_template('index.html', **additional_data)


if __name__ == '__main__':
    app.run(debug=True)
