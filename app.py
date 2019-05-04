from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pandas as pd

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

@app.route('/')
def index():
    mars_data = mongo.db.mars.find_one()
    facts_html = pd.read_html(mars_data['facts'])[0]
    facts_html.set_index('Description', inplace=True)
    return render_template('index.html', mars_data=mars_data, tables=[facts_html.to_html(classes='data')], titles=facts_html.columns.values)

@app.route('/scrape')
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)