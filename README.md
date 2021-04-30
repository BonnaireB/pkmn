# pkmn
A simple api 
## Version
* v1 
* 2021.04.30

REQUIREMENTS
------------

This api requires the following modules:

 * Python 3 (https://www.python.org/downloads/)
 
 INSTALLATION
------------

 * Once you have python downloaded, please run the following commands in a command prompt within your project directory
 * To install pip :
  

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
Then run the following : 
* For windows
```
py get-pip.py
```
* For Mac OS
```
python get-pip.py
```
Once you have pip installed, you need to install Flask and pytest to be able to run the API:
```
pip install flask
pip install pytest
```

 RUNNING THE PROGRAM
------------

To run the program, enter in the terminal :
* Windows
```
py api.py
```
* Mac Os
```
python api.py
```
 API ENDPOINTS
------------

The base url of the api is http://127.0.0.1:50000 but to access the Pokemon ressources you have to add these different endpoint to the URL + argument:
* Get a Pokemon with the ID
```
/api/v1/resources/pokemon/<PokemonId>
```
* Get pokemon(s) with different search parameters : 
```
/api/v1/resources/pokemon?name=<name>&hp=<hp>&type_1=<Type1>
```
* Get all pokemons:
```
/api/v1/resources/pokemon/all
```
* Get all pokemons with pagination :
```
/api/v1/resources/pokemon/page?start=<start>&limit=<limit>
```

## Creator
Benjamin Bonnaire 
