import requests
import pandas as pd
import json

if __name__ == "__main__":
    url = "https://www.spiceography.com/list-of-herbs-and-spices/"
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    df = df.drop("Image", axis=1)
    df = df.set_index("Name")

    result = df.to_json(orient="index")
    parsed = json.loads(result)


    for spice_name in parsed:
        parsed[spice_name]["Flavor"] = parsed[spice_name]["Flavor"].split(",")
        if (parsed[spice_name]["Origin"]):
            parsed[spice_name]["Origin"] = parsed[spice_name]["Origin"].split(",")


    with open('data/spices.json', 'w') as outfile:
        json.dump(parsed, outfile)