from flask import Flask, render_template, request, jsonify
import json
import requests
import os
import webbrowser

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    tower_list = ['tower1', 'tower2', 'tower3', 'tower4']
    if request.method == 'POST':
        tower_name = request.form['tower_name']
        file_folder = "converted_files"

        with open(os.path.join(file_folder, tower_name, f"{tower_name}.json"), "r") as data_file:
            data = json.load(data_file)

        app_list = []
        for app_name in data:
            app_list.append(app_name)

        app_name = request.form['app_name']
        env_name = request.form['env_name']

        url_list = [url.strip() for url in data[app_name][env_name]["urls"]]

        # Send a GET request to each URL and store the status code
        status_codes = []
        for url in url_list:
            try:
                response = requests.get(url)
                status_codes.append(response.status_code)
                webbrowser.open_new_tab(url)
            except requests.exceptions.RequestException as e:
                webbrowser.open_new_tab(url)
                print(f"URL: {url} is not accessible due to an error: {e}")
                status_codes.append(None)

        return render_template("result.html", url_list=url_list, status_codes=status_codes, zip=zip , app_name=app_name)
    else:
        app_list = []

    return render_template('index.html', tower_list=tower_list, app_list=app_list)

@app.route('/app_names', methods=['GET'])
def app_names():
    tower_name = request.args.get('tower_name')
    file_folder = "converted_files"
    with open(os.path.join(file_folder, tower_name, f"{tower_name}.json"), "r") as data_file:
        data = json.load(data_file)

    app_names = list(data.keys())

    return jsonify(app_names)

@app.route('/env_names', methods=['GET'])
def env_names():
    tower_name = request.args.get('tower_name')
    app_name = request.args.get('app_name')
    file_folder = "converted_files"
    with open(os.path.join(file_folder, tower_name, f"{tower_name}.json"), "r") as data_file:
        data = json.load(data_file)

    env_names = list(data[app_name].keys())

    return jsonify(env_names)

if __name__ == '__main__':
    app.run(debug=True)
