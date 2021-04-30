import requests
import json


def test_post_headers_body_json():
    url = 'http://127.0.0.1:5000/api/v1/resources/pokemon'
    
    # Additional headers.
    headers = {'Content-Type': 'application/json' } 

    # Body
    new_pokemon_positive = {
        "Name": "Decodex",
        "Type 1": "Grass",
        "Type 2": "Poison",
        "Total": "318",
        "HP": "45",
        "Attack": "49",
        "Defense": "49",
        "Sp. Atk": "65",
        "Sp. Def": "65",
        "Speed": "45",
        "Generation": "1",
        "Legendary": "False"
    }
    new_pokemon_duplicate={
        "Name": "Bulbasaur",
        "Type 1": "Grass",
        "Type 2": "Poison",
        "Total": "318",
        "HP": "45",
        "Attack": "49",
        "Defense": "49",
        "Sp. Atk": "65",
        "Sp. Def": "65",
        "Speed": "45",
        "Generation": "1",
        "Legendary": "False"
    }
    new_pokemon_negative = {
        "Name": "Bazm",
        "Type 1": "Grass",
        "Type 2": "Poison",
        "Total": "318",
        "Attack": "49",
        "Defense": "49",
        "Sp. Atk": 4,
        "Sp. Def": "65",
        "Speed": "45",
        "Legendary": "False"
    }
    # Performing the POST operations 
    resp_pos = requests.post(url, headers=headers, data=json.dumps(new_pokemon_positive,indent=4))       
    resp_dupl = requests.post(url, headers=headers, data=json.dumps(new_pokemon_duplicate,indent=4))       
    resp_neg = requests.post(url, headers=headers, data=json.dumps(new_pokemon_negative,indent=4))       
    
    # Validate response headers and body contents, e.g. status code.
    assert resp_pos.status_code == 201
    resp_body = resp_pos.json()
    assert resp_body['Pokemon']["Name"] == new_pokemon_positive['Name']

    assert resp_dupl.status_code == 400
    assert len(requests.get(url,params={"name":"Bulbasaur"}).json()) == 1 

    assert resp_neg.status_code == 400

    # print response full body as text
    print(resp_pos.text,resp_neg.text)

def test_get():
    url = 'http://127.0.0.1:5000/api/v1/resources/pokemon'

    #Should return one record with the name Bulbasaur
    positive_args = url+ "?name=Bulbasaur"
    #Should return more than one pokemon
    positive_multiple_args = url+ "?name=Bulbasaur&hp=60"
    # Should return only one
    duplicate_args = url+ "?name=Bulbasaur&name=Bulbasaur"
    #Strength is an invalid argument
    invalid_args = url+ "?strength=45"

    # Performing the api calls
    resp_pos= requests.get(positive_args)
    resp_pos_multiple= requests.get(positive_multiple_args)
    resp_duplicate = requests.get(duplicate_args)
    resp_invalid = requests.get(invalid_args)

    assert resp_pos.status_code == 200
    resp_body_pos = resp_pos.json()
    assert resp_body_pos[0]["Name"] == "Bulbasaur"

    assert resp_pos_multiple.status_code == 200
    resp_pos_multiple = resp_pos_multiple.json()
    print(resp_pos_multiple)
    assert len(resp_pos_multiple) > 1 


    assert resp_duplicate.status_code == 200
    resp_body_dupl = resp_duplicate.json()
    assert resp_body_dupl[0]["Name"] == "Bulbasaur"
    assert len(resp_body_dupl) == 1 

    assert resp_invalid.status_code == 404

def test_put():
    
    url = 'http://127.0.0.1:5000/api/v1/resources/pokemon/1'
    # Additional headers.
    headers = {'Content-Type': 'application/json' } 

    #Should update the hp to 125 for pokemon 1
    positive = {"HP":"125"}

    #Strength is an invalid argument
    negative= {"Strength":"145"}

    # Performing the api calls
    resp_pos = requests.put(url,headers=headers, data=json.dumps(positive))
    resp_neg = requests.put(url, headers=headers, data=json.dumps(negative))

    assert resp_pos.status_code ==  200
    assert resp_pos.json()["Pokemon"]["HP"] == positive["HP"]

    assert resp_neg.status_code ==  400

def test_delete():

    url = 'http://127.0.0.1:5000/api/v1/resources/pokemon/1'

    resp_pos = requests.delete(url)
    resp_neg = requests.delete(url)

    assert resp_pos.status_code == 204
    assert requests.get(url).status_code == 404

    assert resp_neg.status_code == 404

def test_pagination():
    extension = "/api/v1/resources/pokemon/page"
    url = "http://127.0.0.1:5000"+extension

    positive = url+"?limit=10"

    resp_pos = requests.get(positive)
    resp_body_pos = resp_pos.json()

    assert resp_pos.status_code == 200
    assert resp_body_pos['next'] == extension+"?start=11&limit=10"
    assert resp_body_pos['previous'] == ""
    count = resp_body_pos['count']
    assert resp_body_pos['limit'] == 10
    assert len(resp_body_pos['results']) == 10

    negative = url+ '?start='+str(count+2)+'&limit=20'
    resp_neg = requests.get(negative)

    assert resp_neg.status_code == 404



if __name__ == '__main__': 
    test_get()