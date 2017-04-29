class Packet(object):
  'Class to create correct packet format'

  t = None  # Temperature   6b
  s = None  # Speed         5b
  d = None  # Direction     6b
    
  def reset(self):
    self.t = None
    self.s = None
    self.d = None

  def set_t(self, t):
    """
    Temperature, 6 bytes
    E.g. -10.22
         -04.01
         005.22
    """
    # TODO
    self.t = t

  def set_s(self, s):
    """
    Wind speed, 5 bytes
    E.g. 04.50
         15.00
    """

    # 1. Convert s to a string with 2 decimals.
    # 2. Pad the string to match a total of 4 characters
    #    with zfill().
    self.s = '%.2f'.zfill(4) % s

  def set_d(self, d):
    """
    Wind direction, 6 bytes
    E.g. 145.87
         003.00
    """
    self.d = '%.2f'.zfill(5) % d

  def get(self):
    t = '1' if self.t is not None else '0'
    s = '1' if self.s is not None else '0'
    d = '1' if self.d is not None else '0'

    # Convert binary string to decimal.
    # E.g. 101 => 5, wind speed excluded.
    f = str(int(t + s + d, 2))

    # Store packet and reset
    packet = self.f + self.t + self.s + self.d
    self.reset()

    return packet
