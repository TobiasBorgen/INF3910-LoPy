import binascii
import socket
from network import LoRa
from wrapper import LED

class LORA(object):
    'Wrapper class for LoRa'
    
    # LoRa and socket instances
    lora = None
    s = None
    
    def connect(self, dev_eui, app_eui, app_key):
        """
        Connect device to LoRa.
        Set the socket and lora instances.
        """
        
        dev_eui = binascii.unhexlify(dev_eui)
        app_eui = binascii.unhexlify(app_eui)
        app_key = binascii.unhexlify(app_key)
        
        # Disable blue blinking and turn LED off
        LED.heartbeat(False)
        LED.off()

        # Initialize LoRa in LORAWAN mode
        self.lora = LoRa(mode = LoRa.LORAWAN)

        # Join a network using OTAA (Over the Air Activation)
        self.lora.join(activation = LoRa.OTAA, auth = (dev_eui, app_eui, app_key), timeout = 0)

        # Wait until the module has joined the network
        count = 0
        while not self.lora.has_joined():
            LED.blink(1, 2.5, 0xff0000)
            # print("Trying to join: " ,  count)
            count = count + 1

        # Create a LoRa socket
        LED.blink(2, 0.1)
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # Set the LoRaWAN data rate
        self.s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

        # Make the socket non-blocking
        self.s.setblocking(False)

        # print ("Joined! ",  count)
        # print("Create LoRaWAN socket")

        # Create a raw LoRa socket
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.s.setblocking(False)
        
    def send(self, data):
        """
        Send data over the network.
        """
        
        try:
            self.s.send(data)
            LED.blink(2, 0.1, 0x00ff00)
            print("Sending data:")
            print(data)
        except OSError as e:
            if e.errno == 11:
                print("Caught exception while sending")
                print("errno: ", e.errno)
        
        LED.off()
        data = self.s.recv(64)
        print("Received data:", data)

        return data
