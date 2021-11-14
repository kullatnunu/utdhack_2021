from flask import Flask
import requests
app = Flask(__name__)

baseUrl = 'https://aa-travel-experience.herokuapp.com'
airport = '/airports?code='
flight = '/flights?date='


def weather(lat, lon):
    return f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid=e3383f45c2735aa72f25500c44fa28b0"


@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!!"

@app.route('/airport/<string:location>/', methods=['GET', 'POST'])
def get_airport(location):
    res = requests.get(baseUrl+airport+location)
    return res.json()


@app.route('/flight/<string:date>/<int:depart_day>/', methods=['GET', 'POST'])
def get_flights(date, depart_day):
    res = requests.get(baseUrl+flight+date)
    airport_dict = {}
    res = res.json()
    clear_weather = []
    return_list = []
    return_value = {}
    for i in res:
        airport_dict[i['destination']['code']] = i['destination']['location']
    for j, k in airport_dict.items():
        weather_json = (requests.get(weather(k['latitude'], k['longitude'])).json())
        if weather_json['daily'][depart_day-1]['weather'][0]['main'] == "Clear":
            clear_weather.append(j)
    for l in res:
        if l['destination']['code'] in clear_weather and l['origin']['code'] == "DFW":
            return_list.append(l['flightNumber'])
    return_value['Recommand_list'] = list(set(return_list))
    return return_value


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)