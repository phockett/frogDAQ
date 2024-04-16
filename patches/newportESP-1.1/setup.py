from distutils.core import setup

setup(
    name = 'newportESP',
    version = '1.1',
    description = """Python driver for Newport's ESP motion controllers""",
    long_description ="""
    A simple Python driver for Newport's ESP-compatible motion controllers.
    
    Arbitrary numbers of controllers and stages can be used simultaneously
    (within your hardware's capabilities). The whole command set is available,
    although only the most common ones are defined as class methods.
    The driver currently uses only RS232, but adding support from USB and GPIB should be simple.
    
    Usage:
    
    >>> esp = NewportESP('/dev/ttyUSB0') # open communication with controller
    >>> stage = esp.axis(1)   # open axis no 1
    >>> stage.move_to(1.2)    # move to position 1.2 mm
    >>> stage.wait()          # wait until motion is finished.
    """,
    author = 'Guillaume Lepert',
    author_email = 'guillaume.lepert07@imperial.ac.uk',
    py_modules = ['newportESP']
)
