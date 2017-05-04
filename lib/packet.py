class Packet(object):
  'Class to create correct packet format'

  t = None  # Temperature   6b
  s = None  # Speed         5b
  d = None  # Direction     6b
  
  def zfill(self, string, num):
    """
    Generic zfill.
    """
    
    string = str(string)
    
    # Find position of decimal point
    try:
      pos = string.index('.')
    except Exception as e:
      pos = 0
    
    missing = num - pos
    if missing > 0:
      string = ('0' * missing) + string
    
    return string
    
  def reset(self):
    self.t = None
    self.s = None
    self.d = None
    
  def clean(self):
    self.t = '' if self.t is None else self.t
    self.s = '' if self.s is None else self.s
    self.d = '' if self.d is None else self.d

  def set_t(self, t):
    """
    Temperature, 6 bytes
    E.g. -10.22
         -04.01
         005.22
    """
    tx = '%.2f' % t
    
    if t >= 0:
      self.t = self.zfill(tx, 3)
    else:
      pos = tx * (-1)
      self.t = '-' + self.zfill(pos, 2)

  def set_s(self, s):
    """
    Wind speed, 5 bytes
    E.g. 04.50
         15.00
    """
    s = '%.2f' % s

    # 1. Convert s to a string with 2 decimals.
    # 2. Pad the string to match a total of 2 characters
    #    with zfill().
    self.s = self.zfill(s, 2)

  def set_d(self, d):
    """
    Wind direction, 6 bytes
    E.g. 145.87
         003.00
    """
    d = '%.2f' % d
    self.d = self.zfill(d, 3)

  def get(self):
    t = '1' if self.t is not None else '0'
    s = '1' if self.s is not None else '0'
    d = '1' if self.d is not None else '0'
    
    # Convert binary string to decimal.
    # E.g. 101 => 5, wind speed excluded.
    f = str(int(t + s + d, 2))
    
    # Clean values (None > xxx.xx)
    self.clean()

    # Store packet and reset
    packet = f + self.t + self.s + self.d
    self.reset()

    return packet
