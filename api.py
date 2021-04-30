import flask,json
from flask import jsonify,request, abort
import parse_data as p

app = flask.Flask(__name__)
app.config["DEBUG"] = True
#Retrieves the list of pokemons and the research parameters which are the different caracteristics of a pokemon
pokemons,parameters = p.parse_data() 

with open("ressources\\pokemon.json", "r", encoding="utf-8-sig")as j:
    pokemons = json.load(j)


@app.route('/', methods=['GET'])
def home():
    return "<h1>POKEMON LIBRARY</h1><p>This site is a prototype API for accessing data about Pokemons.</p>"

@app.route('/api/v1/resources/pokemon/all', methods=['GET'])
def api_all_pokemon():
    return jsonify(pokemons)

@app.route('/api/v1/resources/pokemon/<int:pokemon_id>', methods=['GET'])    
def api_id(pokemon_id):
    pokes = [poke for poke in pokemons if str(poke['#']) == str(pokemon_id)]
    if len(pokes) == 0:
        abort(404)
    return jsonify(pokes[0])

@app.route('/api/v1/resources/pokemon', methods=['GET'])
def api_pokemon():
    results=[]
    error = False
    error_msg = "Impossible top find resource: \n"
    print(request.args)
    if not request.args:
        return "Invalid research arguments"
    for a in request.args:
    #Look for each request parameters to see if they match available query parameters
        if a in parameters.keys():
    #If parameter is available, returns all the pokemon that matches the values
            z=[poke for poke in pokemons if str(poke[parameters[a]]) == str(request.args[a])]
            results += z

        else :
            # If the argument is not available, error message is also returned
            error = True 
            abort(404)
            error_msg += "Invalid research argument "+ a+", available arguments are "+ str(list(parameters.keys()))+"\n"
    if len(results) == 0:
        abort(404)
    r = list({v['#']:v for v in results}.values())
    return error_msg if error else jsonify(r)

@app.route('/api/v1/resources/pokemon', methods=['POST'])
def add_pokemon():
    poke = {
        '#': str(int(pokemons[-1]['#']) + 1),
        'id': str(int(pokemons[-1]['id']) + 1)
    }
    for a in parameters.keys():
        b = parameters[a]
        # If a parameter is missing in the list of parameters, then an error is raised
        if b in request.json and type(pokemons[-1][b]) == type(request.json[b]):
            poke[b] = request.json[b]
        else : 
            print(b)
            abort(400)
    check_duplicates(poke)
    pokemons.append(poke)
    return jsonify({'Pokemon': poke}), 201

@app.route('/api/v1/resources/pokemon/<int:pokemon_id>', methods=['PUT'])
def update_task(pokemon_id):
    pokes = [poke for poke in pokemons if str(poke['#']) == str(pokemon_id)]
    if len(pokes) == 0:
        abort(404)
    if not request.json:
        abort(400)
    for a in request.json:
        if a in pokemons[0].keys() and type(request.json[a]) == type(pokemons[0][a]):
            pokes[0][a] = request.json[a]
        else : abort(400)
    return jsonify({'Pokemon': pokes[0]}),200

@app.route('/api/v1/resources/pokemon/<int:pokemon_id>', methods=['DELETE'])
def delete_task(pokemon_id):
    pokes = [poke for poke in pokemons if str(poke['#']) == str(pokemon_id)]
    if len(pokes) == 0:
        print("failed")
        abort(404)
    pokemons.remove(pokes[0])
    return jsonify({'result': True}),204

@app.route('/api/v1/resources/pokemon/page')
def pagination():
    url = "/api/v1/resources/pokemon/page"
    start = int(request.args.get("start",1))
    limit = int(request.args.get("limit",10))
    data = get_pagination_list(url,start,limit)
    return jsonify(data)

def get_pagination_list(url,start,limit):
    total = len(pokemons)
    if start > total:
        abort(404)
    data = {
        "start":start,
        "limit":limit,
        "count":total
    }

    if start==1:
        data["previous"] = ''
    else:
        start_previous = max(1, start-limit)
        data['previous'] = url +'?start='+str(start_previous)+'&limit='+str(limit)
    
    if start+limit > total:
        data['next'] = ''
    else:
        start_next = start+limit
        data['next'] = url + '?start='+str(start_next)+'&limit='+str(limit)
    data['results']= pokemons[(start-1):(start-1+ limit)]
    print(data)
    return data


def check_duplicates(pokemon):
    for p in pokemons:
        if p["Name"] == pokemon["Name"]: abort(400)

app.run()