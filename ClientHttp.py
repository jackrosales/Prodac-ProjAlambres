import requests
import sys

func = str(sys.argv[1])
idFMC = int(sys.argv[2])
par1 = int(sys.argv[3])
par2 = int(sys.argv[4]) 
par3 = int(sys.argv[5])
par4 = int(sys.argv[6])

# URL del servidor donde está alojado el API para controlar el movimiento
server_url = 'http://localhost:5000/' + func

# Datos que se enviarán en la solicitud POST (en este caso, un JSON con el comando de movimiento)
data = {
        'Id': idFMC,
        'Par1': par1,
        'par2': par2,
        'par3': par3,
        'par4': par4,
    }

try:
    # Realizar la solicitud POST al servidor
    response = requests.post(server_url, json=data)


    # Verificar el código de estado de la respuesta
    if response.status_code == 200:
        print('Comando de movimiento enviado con éxito.')
    else:
        print('Error al enviar el comando de movimiento. Código de estado:', response.status_code)

except requests.exceptions.RequestException as e:
        print('Error de conexión:', e)

