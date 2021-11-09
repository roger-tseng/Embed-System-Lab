from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

scanner = Scanner()
print("Scanning for 5 seconds...")
devices = list(scanner.scan(5.0))

for i,dev in enumerate(devices):
    print("#%d: %s (%s), RSSI=%d dB" % (i, dev.addr, dev.addrType, dev.rssi))
    for (adtype, desc, value) in dev.getScanData():
        if desc=="Complete Local Name":
            print( "  %s = %s" % (desc, value))

print()
number = int(input('Enter your device number: '))
print(f'Connecting to #{number}: {devices[number].addr}')

dev = Peripheral(devices[number].addr, devices[number].addrType)

print()
print("Available Services:")
for svc in dev.services:
    print("Service", str(svc))
    
try:
    target_svc = int("0x"+str(input("Which service to connect? ")), 16)
    testService= dev.getServiceByUUID(UUID(target_svc))
    print()
    print("Available Characteristics:")
    for ch in testService.getCharacteristics():
        print(str(ch))
    target_char = int("0x"+str(input("Which characteristic to connect? ")), 16)
    ch = dev.getCharacteristics(uuid=UUID(target_char))[0]
    
    print()
    if target_svc == 0xa000:
        while True:
            if (ch.supportsRead()):
                print("Data in channel:", ch.read())
                time.sleep(0.5)
    elif target_svc == 0xa002:
        if (ch.supportsRead()):
            print("Data in channel:", ch.read())
        while True:
            message = input("To Write:")
            ch.write(message.encode('utf-8'))
            print(message.encode('utf-8'))

finally:
    dev.disconnect()
