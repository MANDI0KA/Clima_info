import requests
from django.shortcuts import render

API_KEY = 'EcSBedrXbyFhMScag8G0Zwj8p36qbF4M' 
REALTIME_URL = f"https://api.tomorrow.io/v4/weather/realtime?location={{city}}&units=metric&apikey={API_KEY}"

CLIMA_MAP = {
    1000: 'Despejado', 1001: 'Nublado', 1100: 'Mayormente despejado',
    1101: 'Parcialmente nublado', 1102: 'Mayormente nublado', 2000: 'Llovizna',
    2100: 'Lluvia ligera', 4000: 'Llovizna', 4001: 'Lluvia', 4200: 'Lluvia ligera',
    4201: 'Lluvia intensa', 5000: 'Nieve', 5001: 'Nieve ligera', 5100: 'Nieve', 
    6000: 'Llovizna helada', 6001: 'Lluvia helada', 6200: 'Lluvia helada ligera',
    7000: 'Hielo', 7100: 'Hielo ligero', 8000: 'Aguacero', 
    3000: 'Nieve/Lluvia', 3001: 'Nieve/Lluvia', 3002: 'Nieve/Lluvia'
}

def clima_vista(request):
    context = {} 

    if request.method == 'POST':
        ciudad = request.POST.get('city')
        
        if not ciudad:
            context['error_message'] = "Por favor, ingresa una ciudad."
            return render(request, 'clima_app/climafront.html', context)
        
        url = REALTIME_URL.format(city=ciudad)

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and 'data' in data and 'values' in data['data']:
                
                clima_valores = data['data']['values']
                
                weather_code = clima_valores.get('weatherCode', 1000)
                descripcion = CLIMA_MAP.get(weather_code, 'Condición Desconocida')
                
                clima_data = {
                    'ciudad': ciudad.capitalize(),
                    'temperatura': f"{clima_valores.get('temperature', 0.0):.1f}", 
                    'humedad': f"{clima_valores.get('humidity', 0)}",
                    'viento': f"{clima_valores.get('windSpeed', 0.0):.1f}",
                    'descripcion': descripcion,
                }
                
                context['clima_data'] = clima_data

            else:
                error_msg = data.get('message', f"Error {response.status_code}: Ciudad no encontrada o clave API incorrecta.")
                context['error_message'] = error_msg
                
        except requests.exceptions.RequestException:
            context['error_message'] = "Error de conexión: No se pudo contactar con el servicio de clima. ¿Está el servidor de Tomorrow.io disponible?"
            
        except Exception as e:
            context['error_message'] = f"Error al procesar los datos: {e}"
            
    return render(request, 'clima_app/climafront.html', context)