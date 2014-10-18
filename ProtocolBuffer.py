import base64
import binascii

class ProtocolBuffer:
  def __init__( self ):
    self.buffer = []

  def __encode_int( self, number ):
    while number:
      mod    = number % 128
      number >>= 7
      if number:
        mod += 128

      self.buffer.append( mod )

  def reset( self ):
    self.buffer = []

  def update( self, data, raw = False ):

    if raw is True:
      self.buffer.append( data )

    else:
      data_type = type(data).__name__

      if data_type == "bool":
        self.buffer.append( 1 if data is True else 0 )

      elif data_type == "int":
        self.__encode_int( data )

      elif data_type == "str":
        self.__encode_int( len(data) )
        for c in data:
          self.buffer.append( ord(c) )

      else:
        raise Exception( "Unhandled data type : " + data_type )

    return self.buffer

  def finalize( self, b64 = True ):
    if not b64:
        stream = ""
        for data in self.buffer:
            stream += chr( data )
        return stream
    else:
        stream_hex = ""
        for data in self.buffer:
            stream_hex += ('%02x' % data)
        return base64.b64encode(binascii.a2b_hex(stream_hex))

