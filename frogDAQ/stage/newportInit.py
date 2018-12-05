
"""
newportInitComms(port,stageID)

Basic function to init & test Newport ESP stage(s).
Serial comms, using newportESP python wrapper, from https://pypi.org/project/NewportESP/

Inputs:
    - port = serial port to use.
    - stageID = stage number (corresponds to number on ESP controller).

Outputs:
    - esp controller object.
    - stage (axis) object.
"""
# Import seabreeze for Ocean Optics spectrometer interfacing
try:
    import newportESP
except ImportError as e:
    if e.msg != "No module named 'newportESP'":
        raise
    print('* NewportESP not found, Newport ESP stage control not available. ')
    
def newportInitComms(port,stageID):
    # Init comms
    esp = newportESP.ESP(port)
    stage = esp.axis(stageID)

    # Test
    stage.id
    stage.position

    # Check specs
    stage.travel_limits

    # OTHER SETTINGS?  May want to set move speed etc. here?

    # Find home
    # stage.on()
    # stage.home_search

    return esp, stage
