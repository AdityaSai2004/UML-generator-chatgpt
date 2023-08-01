import os
import base64
import openai
import plantuml
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
            max_tokens=2048,
            top_p=1,
        )
        result = response.choices[0].text
        image_data = generate_img(result)
        image_data_base64 = base64.b64encode(image_data).decode("utf-8")
        return render_template("index.html", result=result, image_data=image_data_base64)

    result = request.args.get("result")
    return render_template("index.html", result=result)

def generate_prompt(animal):
    return "Generate the plant uml code for the given specification." + animal

def generate_img(result):
    url = "http://www.plantuml.com/plantuml/img/"
    image = plantuml.PlantUML(url).processes(result)
    with open('diagram.png', 'wb') as f:
        f.write(image)
    return image