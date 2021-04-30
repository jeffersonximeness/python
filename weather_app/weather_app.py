import requests 
import json
import pprint

API_KEY = ''


def obter_coordenadas():
    r = requests.get('http://www.geoplugin.net/json.gp')

    if r.status_code != 200:
        print('Não foi possível obter a localização')

    localizacao = json.loads(r.text)
    coordenadas = {}
    coordenadas['lat'] = localizacao['geoplugin_latitude']
    coordenadas['long'] = localizacao['geoplugin_longitude']

    return coordenadas

def obter_codigo_local(lat, long):
    LOCATION_API_URL = f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={API_KEY}&q={lat}%2C%20{long}&language=pt-br'
    r = requests.get(LOCATION_API_URL)

    if r.status_code != 200:
        print('Não foi possível obter a localização')

    location_response = json.loads(r.text)
    info_local = {}
    info_local['nome_local'] = location_response['LocalizedName'] + ", " + location_response['AdministrativeArea']['LocalizedName'] + ". " + location_response['Country']['LocalizedName']
    info_local['codigo_local'] = location_response['Key']

    return info_local

def obter_tempo_agora(codigo_local, nome_local):
    current_conditions_url = f'http://dataservice.accuweather.com/currentconditions/v1/{codigo_local}?apikey={API_KEY}&language=pt-br'
    r = requests.get(current_conditions_url)

    if r.status_code != 200:
        print('Não foi possível obter o código do local')

    current_conditions_response = json.loads(r.text)
    info_clima = {}
    info_clima['texto_clima'] = current_conditions_response[0]['WeatherText']
    info_clima['temperatura'] = current_conditions_response[0]['Temperature']['Metric']['Value']
    info_clima['nome_local'] = nome_local

    return info_clima


if __name__ == '__main__':
    coordenadas = obter_coordenadas()
    local = obter_codigo_local(coordenadas['lat'], coordenadas['long'])
    clima_atual = obter_tempo_agora(local['codigo_local'], local['nome_local'])
    
    print('Clima atual em: {}'.format(clima_atual['nome_local']))
    print('{}'.format(clima_atual['texto_clima']))
    print('Temperatura: {} {}C'.format(str(clima_atual['temperatura']), '\xb0'))
