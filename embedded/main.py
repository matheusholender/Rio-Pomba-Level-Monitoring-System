import _thread
import time
import sensor
import webserver

text = (
    "----------------------------------------------------------------\n"
    "Sistema de Medição Ultrassônico de Nivel do Rio Pomba\n"
    "Desenvolvido por Matheus V. Holender em parceria com a Eneltec\n"
    "----------------------------------------------------------------\n"
)
print(text)

def measurement_thread():
    while True:
        value = float(sensor.run() / 10)
        #webserver.update_value(value)
        time.sleep(5)

#webserver.start_ap()
measurement_thread()
#webserver.start_web_server()
