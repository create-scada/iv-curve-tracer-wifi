import network

def setup_wifi_ap(ssid, password):

    ap = network.WLAN(network.AP_IF)

    ap.config(essid=ssid, password=password) 
    ap.active(True)

    while ap.active() == False:
      pass

    print("Access point active")
    print(ap.ifconfig())

    return True
