from flask import Flask, render_template, url_for
import requests
from dotenv import load_dotenv
import os

load_dotenv()

MAPBOX_KEY = os.getenv('mapboxkey')

app = Flask(__name__)


def get_sheet_url(sheet_id):
    return "https://docs.google.com/spreadsheets/d/{}/export?format=csv".format(sheet_id)

SHEET_URL = get_sheet_url("1eo6L93Ck9Uz4EPqcXWxqfKpV2ndP2dfXJ_QapGoxMRs")


@app.route("/")
def index():
    
    data = []
    r = requests.get(SHEET_URL)
    if r.status_code != 200:
        return "Error"
    decoded = r.content.decode('utf-8')
    for line in decoded.split('\n')[1:]:
        line = line.strip()
        vals = line.split(',')
        new_rest = {}
        new_rest['name'] = vals[0]
        new_rest['city'] = vals[1]
        new_rest['location'] = [int(vals[2]), int(vals[3])]
        new_rest['description'] = vals[4]
        new_rest['link'] = vals[5]
        data.append(new_rest)

    chapters = []

    for i,rest in enumerate(data):
        rest_data = {'id': rest['name'],
            'alignment': 'right' if i%2==0 else 'left',
            'hidden': False,
            'title': rest['name'],
            'link': rest['link'],
            'date': rest['city'],
            'image': '',
            'description': rest['description'],
            'location': rest['location'],
            'mapAnimation': 'flyTo',
            'rotateAnimation': False,
            'callback': ''}
        chapters.append(rest_data)
    return render_template('index.html', chapters=chapters, MAPBOX_KEY =MAPBOX_KEY )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 8000, debug=True)