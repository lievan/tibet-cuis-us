from flask import Flask, render_template, url_for
import requests
from dotenv import load_dotenv
import os
import csv
import pandas as pd
from io import StringIO

load_dotenv()

MAPBOX_KEY = os.getenv('mapboxkey')

app = Flask(__name__)


def get_sheet_url(sheet_id):
    return "https://docs.google.com/spreadsheets/d/{}/export?format=csv".format(sheet_id)

SHEET_URL = get_sheet_url("1eo6L93Ck9Uz4EPqcXWxqfKpV2ndP2dfXJ_QapGoxMRs")


@app.route("/")
def index():
    r = requests.get(SHEET_URL)
    if r.status_code != 200:
        return "Error"
    decoded = r.content.decode()
    df = pd.read_csv(StringIO(decoded))
    chapters = []
    header_data = {'id': 'intro',
                    'alignment': 'center',
                    'hidden': False,
                    'title': '',
                    'link': '',
                    'date':"",
                    'image': '',
                    'description': """This web app provides a tour of Tibetan food in the United States.
                                      Scroll slowly to jump from restaurants to restaurants.<br><br>
                                      The restaraunts were found from a variety of sources, primarily inspired by this
                                      <a href=https://www.farandwide.com/s/best-tibetan-restaurants-usa-074f18478b4c41eb>article</a> 
                                      on America's top Tibetan Restaraunts. Related links are at the bottom of the website.
                                      <br><br>
                                      The following restaurants showcase a variety of authentic Tibetan dishes and demonstrate how
                                      Tibetan cuisine has adapted to different environments in the states, ranging from
                                      immigrant hubs such as Queens to places where the Tibetan community is not prominent.
                                      Many of the owners and chefs mentioned below have a unique journey in the restaurant industry, 
                                      gaining experience in a variety of different cuisines after moving to the states before opening 
                                      their own establishments. You'll often see the menus of these 
                                      restaurants also including American-Chinese food, Indian food, and Nepalese food and utilizing  concepts
                                      such as set menus, buffets, and more.
                                      <br><br>
                                      If you would like to add a restaraunt to this site, please use 
                                      this <a href=https://forms.gle/brPyQYc1KKzEvmkR8>Google Form</a>.
                                      <br><br>
                                      For more resources on Tibetan culture, feel free to check out this
                                      <a href=https://tibetanculture.weai.columbia.edu/>Tibetan Culture</a> by Columbia's Tibetan studies department""",
                    'location': [-73.963036, 40.807384],
                    'mapAnimation': 'flyTo',
                    'rotateAnimation': False,
                    'callback': ''
                }
    footer_data = {'id': 'conclusion',
                    'alignment': 'center',
                    'hidden': False,
                    'title': '',
                    'link': '',
                    'date':"Related links",
                    'image': '',
                    'description': """
                                      <a href=https://www.farandwide.com/s/best-tibetan-restaurants-usa-074f18478b4c41eb>America's 
                                        Top Tibetan Restaurants Will Have You Asking for Seconds</a> 
                                        <br><br>
                                      <a href=https://tibetanculture.weai.columbia.edu/tibetan-cuisine-nyc/>
                                        Tibetan Cuisine in NYC</a> 
                                        <br><br>
                                      <a href=https://driftingclouds.net/2021/03/28/34-province-project-tibet-%E8%A5%BF%E8%97%8F/>
                                        Header Background Image Source</a> 
                                    """,
                    'location': [-73.9626, 40.8075],
                    'mapAnimation': 'flyTo',
                    'rotateAnimation': False,
                    'callback': ''
                }
    chapters.append(header_data)
    for i, row in df.iterrows():
        rest_data = {'id': row['name'],
            'alignment': 'right' if i%2==0 else 'left',
            'hidden': False,
            'title': row['name'],
            'link': row['link'],
            'date': row['city'] + ', ' + row['state'],
            'image': '',
            'description': row['description'].replace('"', '').strip().replace("\n", "<br>"),
            'location': [float(row['long']), float(row['lat'])],
            'mapAnimation': 'flyTo',
            'rotateAnimation': False,
            'callback': ''}
        chapters.append(rest_data)
    chapters.append(footer_data)
    return render_template('index.html', chapters=chapters, MAPBOX_KEY =MAPBOX_KEY )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 8000, debug=True)