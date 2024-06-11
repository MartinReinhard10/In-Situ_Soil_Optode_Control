import adafruit_dht
import board

#Intialize Temperature Sensor
dhtDevice = adafruit_dht.DHT22(board.D8)

       
def update_temp_values(label_t, label_h):
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        label_t.config(text="Temperature {:.1f} C".format(temperature_c))
        label_h.config(text="Humidity {}%".format(humidity))
    except RuntimeError as error:
        pass

    # Update every 2 seconds
    label_t.after(2000, update_temp_values, label_t, label_h)
