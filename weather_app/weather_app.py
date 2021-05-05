import requests 
import json
import pprint
from datetime import date

API_KEY = ''
dias = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']

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

def previsao_futura_json(codigo_local):
    future_conditions = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{codigo_local}?apikey={API_KEY}&language=pt-br&metric=True'
    r = requests.get(future_conditions)

    if r.status_code != 200:
        print('Não foi possível obter a previsão')

    future_conditions_response = json.loads(r.text)
    
    return future_conditions_response['DailyForecasts']

def previsao_futura(json_previsao):
    info_5_dias = []

    for dia in json_previsao:
        clima_dia = {}
        clima_dia['max'] = dia['Temperature']['Maximum']['Value']
        clima_dia['min'] = dia['Temperature']['Minimum']['Value']
        clima_dia['clima'] = dia['Day']['IconPhrase']
        dia_semana = int(date.fromtimestamp(dia['EpochDate']).strftime('%w'))
        clima_dia['dia'] = dias[dia_semana]

        info_5_dias.append(clima_dia)

    return info_5_dias 


if __name__ == '__main__':
    coordenadas = obter_coordenadas()
    local = obter_codigo_local(coordenadas['lat'], coordenadas['long'])

    clima_atual = obter_tempo_agora(local['codigo_local'], local['nome_local'])
    
    print('Clima atual em: {}'.format(clima_atual['nome_local']))
    print('{}'.format(clima_atual['texto_clima']))
    print('Temperatura: {} {}C\n'.format(str(clima_atual['temperatura']), '\xb0'))

    json_previsao = previsao_futura_json(local['codigo_local'])
    lista_dias = previsao_futura(json_previsao)

    print('Clima para hoje e para os próximos dias...\n')
    
    for dia in lista_dias:
        print(dia['dia'])
        print('Mínima: {} {}C'.format(str(dia['min']), '\xb0'))
        print('Máxima: {} {}C'.format(str(dia['max']), '\xb0'))
        print('Clima: {}'.format(str(dia['clima'])))
        print('--------------------------------------------------')