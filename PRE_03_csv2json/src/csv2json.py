import csv
import json

def convert_csv_2_json(input_file):

    output_file = input_file.replace(".csv", ".json")
    output_file = output_file.replace("/data/", "/temp/")

    data = []

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


convert_csv_2_json("PRE_03_csv2json/data/drivers.csv")

   
