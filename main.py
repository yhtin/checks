from flask import Flask, request, render_template
import os
import json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/convert", methods=["POST"])
def convert():
    tower_name = request.form["tower_name"]
    application_name = request.form["application_name"]
    environment = request.form["environment"]
    file = request.files["file"]

    file_folder = "converted_files"
    os.makedirs(os.path.join(file_folder, tower_name), exist_ok=True)
    file.save(os.path.join(file_folder, tower_name, file.filename))

    with open(os.path.join(file_folder, tower_name, file.filename), "r") as fileinput:
        urls = fileinput.readlines()

    try:
        with open(os.path.join(file_folder, tower_name, f"{tower_name}.json"), "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        data = {}

    new_data = {
        application_name: {
            environment: {
                "urls": urls
            }
        }
    }

    if application_name in data:
        data[application_name][environment] = new_data[application_name][environment]
    else:
        data.update(new_data)

    with open(os.path.join(file_folder, tower_name, f"{tower_name}.json"), "w") as data_file:
        json.dump(data, data_file, indent=4)

    return render_template("sucessmsg.html", tower_name=tower_name, application_name=application_name)



if __name__ == "__main__":
    app.run(debug=True)



