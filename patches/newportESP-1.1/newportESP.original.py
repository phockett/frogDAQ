"""Driver for Newport's ESP (and compatible) motion controllers over a serial port (RS232). 

Refer to the controller's manual for detailed operational instructions: http://assets.newport.com/webDocuments-EN/images/ESP300_User_Manual.pdf

:Usage:

>>> from newportESP import ESP
>>> esp = ESP('/dev/ttyUSB0')  # open communication with controller
>>> stage = esp.axis(1)        # open axis no 1
>>> stage.id                   # print stage ID
>>> stage.move_to(1.2)         # Move to position 1.2 mm

**Revision history:**

  - v. 0.3 (27 August 2015): update all methods/properties names to lowercase.
    Capitalised versions are still available for backward compatibility.

  - v. 0.4 (28 September 2015): added a threading.Lock() to the query() method.
    This should make the module thread-safe.

  - v. 1.0 (16 February 2016) clean up Sphinx documentation.
    Remove all capitalised names.
    Upload to PyPi.
    
----------------------------------------   
"""

import serial
from time import sleep
import signal
import threading
#import logging
#from  matplotlib.cbook import Stack


class NewportError(Exception):
  """Represents errors raised by the ESP controller."""
  # Error are in the form of 'code, timestamp, MESSAGE', eg: '0, 451322, NO ERROR DETECTED'
  def __init__(self, string):
    self._string = string
    split_string = string.split(',')
    code = split_string[0]
    if len(code) == 3:
      self.axis = code[0]
      self.code = code[1:]
    else:
      self.axis = None
      self.code = code
    self.code = split_string[0]
    self.timestamp = split_string[1][1:]
    self.message = split_string[2][1:]

  def __str__(self):
    if self.axis is not None:
      if_axis_specific = ' on axis ' + self.axis
    else:
      if_axis_specific = ''
    return self.message + if_axis_specific

def catch_error(func):
  """A decorator to read error messages after calling ESP functions."""
  def inner(*args, **kwargs):
    self = args[0]
    func(*args, **kwargs)
    self.write('TB?', axis="")
    error_string = self.read_error()
    if error_string[0] is not '0':
      self.abort()
      raise NewportError(error_string)
  return inner

def check_previous_motion_is_done(func):
  def checked_previous_motion_is_done(*args, **kwargs):
    self = args[0]
    if self.moving:
      raise RuntimeError('Previous motion is not done! Aborting.')
    else:
      func(*args, **kwargs)
  return checked_previous_motion_is_done

class ESP(object):
  """ Driver for Newport's ESP (100/300) motion controller.

  :Usage:
  
  >>> esp = NewportESP.ESP('/dev/ttyUSB0') # open communication with controller
  >>> stage = esp.axis(1)   # open axis no 1
  """
  def __init__(self, port):
    """:param port: Serial port connected to the controller."""
    self.lock = threading.Lock()
    self.ser = serial.Serial(port=port,
                             baudrate=19200,
                             bytesize=8,
                             timeout=1,
                             parity='N',
                             rtscts=1)
    #print("Found controller: " + self.version)
    self.Abort = self.abort

  def __del__(self):
    self.ser.close()

  def read(self):
    """ Serial read with EOL character removed."""
    with DelayedKeyboardInterrupt():
      # stuff here will not be interrupted by SIGINT
      str = self.ser.readline()
    return str[0:-2]

  def write(self, string, axis=None):
    """ Serial write.
    
    The EOL character is automatically appended
    
    :param string: the string to write to the port
    :param axis: index of the destination axis. If unspecified, the destination is the controller."""
    self.ser.write((str(axis) if axis is not None else "") + string + "\r")

  def query(self, string, axis=None, check_error=False):
    """write a command and read the reply.
    
    :param string: string to write to the port
    :param axis: index of the destination axis. If unspecified, the destination is the controller.
    :param check_error: if True, query the controller for any error, both before writing and before reading.
    :type check_error: bool
    :return: the reply string
    :rtype: string
    """    
    with self.lock:
      if check_error:
        self.raise_error()
      self.write(string+'?', axis=axis)
      if check_error:
        self.raise_error()
      return self.read()

  @property
  def version(self):
    """The controller firmware version number."""
    return self.query('VE')

  def abort(self):
    """Send an 'Abort motion' command to the controller."""
    self.write('AB')

  def read_error(self):
    """Return the last error as a string."""
    return self.query('TB')
    
  def raise_error(self):
    """Check the last error message and raise a NewportError."""
    err = self.read_error()
    if err[0] != "0":
      raise NewportError(err)
  
  def axis(self, axis_index=1):
    """create an Axis object.
    
    :param axis_index: the axis index
    :type axis_index: int
    :rtype: :class:`Axis`
    """
    return Axis(self, axis=axis_index)

class Axis(object):
  """ Represents a Newport actuator or motorised stage attached to the ESP controller.
  
  :Usage:
  
  >>> esp = NewportESP.ESP('/dev/ttyUSB0') # open communication with controller
  >>> stage = NewportESP.Axis(esp, axis = 1)   # open axis no 1
  """
  def __init__(self, controller, axis=1):
    """
    :param controller: The axis' Newport ESP controller
    :type controller: :class:`ESP`
    :param axis: the axis index
    :type axis: int
    """
    self.axis = axis
    self.esp = controller
    self.read = self.esp.read
    self.step_size_list = (1, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001)
    self.step_size = 6  # default increment for gotoRel (index in step_size_list)
    self.polling_time = 0.02

    self.abort = self.esp.abort    
    self.read_error = self.esp.read_error
  
  def __del__(self):
    self.off()
  
  def write(self, string, axis=None):
    """ Send a command string to the axis.
     
    Can be used to send commands that are not covered by class methods.
    
    :param string: the command string. The axis index and EOL characters are automatically appended.
    :param axis: if unspecified, the command is directed to the current axis. However, by setting ``axis`` to an empty string, the command will be directed to the controller instead. 
    """
    if axis is None:
      axis = self.axis
    # optional argument allows none-axis-specific commands
    # (most of which should be in the controller class, but a few are useful here.)
    self.esp.write(string, axis=axis)
  
  def query(self, string, check_error=False):
    """write a command and read the reply.
    
    :param string: string to write to the port
    :param check_error: if True, query the controller for any error, both before writing and before reading.
    :type check_error: bool
    :return: the reply string
    :rtype: string
    """
    return self.esp.query(string, self.axis, check_error)
  
  @property
  def id(self):
    """The axis model and serial number."""
    return self.query('ID')
  
  def on(self):
    """Power on the axis."""
    self.write("MO")
    
  def off(self):
    """Power on the axis."""
    self.write("MF")

  def home_search(self, mode=None):
    """Search for home.

    This command executes a Home search routine on the axis.
    
    If ``mode`` is missing, the axes will search for home using the mode specified using OM command.
    The possible values for ``mode`` are:    
      
      - 0, search for zero position count.
      - 1, search for combined Home and Index signal transitions.
      - 2, search for Home signal transition only.
      - 3, search for positive limit signal transition.
      - 4, search for negative limit signal transition.
      - 5, search for positive limit and index signal transition.
      - 6, search for negative limit and index signal transition.
    
    At the end of a home search routine, the position of axes is reset to the value specified using SH command.
    
    The home search motion status can be monitored with the Motion Done (MD) 
    status command. If a fault condition such as E-stop occurs while home search is 
    in progress or if this command is issued to an axis before enabling it, the
    controller returns error xx20, 'HOMING ABORTED'.
    For a detailed description of the home search routine see the Home - The Axis
    Origin chapter in the Motion Control Tutorial section.
    """
    if mode is None:
      mode = ""
    self.write('OR'+str(mode))
  
  @property
  def home(self):
    """Define home.
    
    This command is used to define current position, HOME position. This means
    that the current position will be preset to the value defined by parameter 'nn'.
    """
    return self.query('DH')
  @home.setter
  def home(self, nn):
    self.write('DH'+str(nn))
  
  @property
  def moving(self):
    """Return True is motion is finished.
    
    :rtype: bool
    """
    return False if self.query('MD') == "1" else True
      
  def wait(self):
    """This method will block until current motion is finished."""
    while self.moving:
      sleep(self.polling_time)
  
  #catch_error
  def move_to(self, pos, wait=False): 
    """Go to absolute position.
    
    :param pos: the final position (in mm)
    :type pos: float
    :param wait: whether to block until the motion is finished
    :type wait: bool
    """
    self.write("PA" + str(pos))
    if wait:
      self.wait()

  #catch_error
  def move_by(self, pos, wait=False):
    """Go to relative position.
    
    :param pos: the requested step (in mm)
    :type pos: float
    :param wait: whether to block until the motion is finished
    :type wait: bool
    """
    self.write("PR" + str(pos))
    if wait:
      self.wait()  
    
  @property
  def position(self):
    """The current position, in mm."""
    return float(self.query('TP'))
    
  def move_to_hardware_limit(self, direction):
    """Move to hardware limit.
    
    :param direction: negative or position, indicate which direction to move towards.
    :type direction: float
    """
    self.write('MT'+str(direction))
  
  @check_previous_motion_is_done
  def move_up(self):
    """Move continuously upwards (negative direction).
    
    Call :func:`stop` to stop the motion.
    """
    if not self.moving:
      self.write('MV-')
    else:
      print("Previous motion is not done!")
  
  @check_previous_motion_is_done 
  def move_down(self):
    """Move continuously downwards (positive direction).
    
    Call :func:`stop` to stop the motion.
    """
    if not self.moving:
      self.write('MV+')
    else:
      print("Previous motion is not done!")
      
  @check_previous_motion_is_done 
  def move_(self, direction):
    if not self.moving:
      self.write('MV+')
    else:
      print("Previous motion is not done!")
      
  def stop(self):
    """Stop the current motion."""
    self.write('ST')
  
  @property
  def backlash(self):
    """set backlash compensation (in mm).
    
    This command initiates a backlash compensation algorithm when motion
    direction is reversed. The controller keeps track of the motion sequence and for
    each direction change it adds the specified nn correction. Setting nn to zero
    disables the backlash compensation.
    
    NOTE: The command is affective only after a home search (OR) or define
    home (DH) is performed on the specified axis.
    """

    return float(self.query('BA'))
  
  @backlash.setter
  def backlash(self, value):
    self.write('BA'+str(value))
  
  @property  
  def resolution(self):
    """Return the encoder resolution, in mm."""
    return float(self.query('SU'))
    
  @property
  def unit(self):
    """Return the encoder unit."""
    return UNIT[int(self.query('SN'))]
  
  def travel_limits(self, left=None, right=None):
    """Set or query the axis travel limits.
    
    :param float left:  left (negative) travel limit 
    :param float right: right (positive) travel limit
     
     If both limits are unspecified, returns the current settings as a dictionary.
    """
    if left is None and right is None:
      left_lim = float(self.query('SL'))
      right_lim = float(self.query('SR'))
      return {'left': left_lim, 'right': right_lim}
    if left is not None:
      self.write('SL'+str(left))
    if right is not None:
      self.write('SR'+str(right))
  
  #def setVelocity(self, vel):

UNIT = {0: 'encoder count', 1: 'motor step', 2: 'millimiter', 3: 'micrometer',
4: 'inches', 5: 'milli-inches', 6: 'micro-inches', 7: 'degree', 8: 'gradient',
9: 'radian', 10: 'milliradian', 11: 'microradian'}


class DelayedKeyboardInterrupt(object):
    """Context manager that capture a KeyboardInterrupt Event 
    and ignores it for the duration of the context, triggering the
    interrupt when exiting. If called in a thread, does nothing.
    """
    def __enter__(self):
      try:
        self.signal_received = False
        self.old_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.handler)
        self.threaded = False
      except ValueError:
        self.threaded = True

    def handler(self, signal, frame):
        self.signal_received = (signal, frame)
        #logging.debug('SIGINT received. Delaying KeyboardInterrupt.')

    def __exit__(self, type, value, traceback):
      if not self.threaded:
        signal.signal(signal.SIGINT, self.old_handler)
        if self.signal_received:
            self.old_handler(*self.signal_received)
      else:
        pass
