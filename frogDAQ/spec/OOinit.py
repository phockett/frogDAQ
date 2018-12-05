

# Import seabreeze for Ocean Optics spectrometer interfacing
try:
    from frogDAQ.spec import OOfunc as OO
    import seabreeze.spectrometers as sb
except ImportError as e:
    if e.msg != "No module named 'seabreeze.spectrometers'":
        raise
    print('* Seabreeze not found, Ocean Optics Spectrometers not available. ')

def OOinit():
    # Init & test spectrometer(s)

    # Find spectrometers & print list
    devices = sb.list_devices()
    print(devices)

    # Test spectrometers in the list, 15 frames each
    [OO.run(devices,devID=n,frames=15) for n in range(len(devices))]

    return devices
