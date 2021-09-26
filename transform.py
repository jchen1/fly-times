import csv
from datetime import date

fieldnames = [
    "Date",
    "Rep",
    "Whoop Recovery",
    "Whoop Sleep",
    "Whoop Sleep %",
    "Workout time",
    "Weather (F)",
    "Weight (lbs)"
]

fieldnames_no_rep = [field for field in fieldnames if field != "Rep"]

def parse_date(datestr):
    split = datestr.split("/")
    month = int(split[0])
    day = int(split[1])
    year = int(split[2] if len(split) == 3 else "2021")
    return date(year, month, day)

def transform_row(row):
    rows = []

    date_level = { k: (parse_date(row[k]) if k == "Date" else row[k]) for k in fieldnames_no_rep }

    for rep in range(9):
        key = "Rep " + str(rep)
        if key in row and row[key] != '':
            newrow = date_level.copy()
            newrow["Rep"] = row[key]
            rows.append(newrow)

    return rows
        

def parse_csv(filename):
    with open(filename) as file:
        reader = csv.DictReader(file)

        return [tr for row in reader for tr in transform_row(row)]
    

def spit_data(filename, data):
    with open(filename, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    rows = parse_csv("by_date.csv")
    spit_data("by_rep.csv", rows)