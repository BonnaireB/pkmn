import csv,json,requests


def read_csv():
    file_path = "ressources\\pokemon.csv"
    data=[]
    with open(file_path, mode='r', encoding='utf-8-sig') as infile:
        for line in csv.DictReader(infile):
            data.append(line)
    return data

def parse_data():
    d = read_csv()
    d = format(d)
    save_json(d)
    # Poke args are the search parameters availables, a dict with a formated 
    #lowerkey key whithout space, and a value as the original json key
    args = {}
    for a in d[0].keys():
        args[a.replace(" ","_").replace(".","").lower()]= a
    args.pop('#')
    args.pop('id')
    return d, args

def format(data):
    for i,d in enumerate(data,0):
        d["id"] = i
    return data

def save_json(data):
    output_file = "ressources\\pokemon.json"
    with open(output_file,"w", encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=4)