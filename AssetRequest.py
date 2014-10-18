from ProtocolBuffer import ProtocolBuffer

class AssetRequest:
  def __init__( self, package_name, auth_token, device_id, operator, device_name, sdk_version):
    self.encode_table       = [0, [16], 2, [24], 4, [34], 6, [42], 8, [50], 10, [58], 12, [66], 14, [74], 16, [82], 18, [90], 20, [19, 82], 22, [10], 24, [20]]
    self.pad                = [ 10 ]
    self.buffer             = ProtocolBuffer()

    self.auth_token         = auth_token
    self.is_secure          = True
    self.sdk_version        = 2009011
    self.device_id          = device_id
    self.device_name        = device_name
    self.sdk_version        = sdk_version
    self.locale             = "en"
    self.country            = "us"
    self.operator_alpha     = operator.name
    self.sim_operator_alpha = operator.name
    self.operator_code      = operator.code
    self.sim_operator_code  = operator.code
    self.package_name       = package_name

  def encode( self ):
    self.buffer.reset()

    header_len = 0

    for encoder in self.encode_table:
      enc_type = type(encoder).__name__

      if enc_type == "list":
        self.buffer.buffer += encoder

      elif enc_type == "int":
        if encoder ==  0:
          self.buffer.update( self.auth_token )

        elif encoder ==  2:
          self.buffer.update( self.is_secure )

        elif encoder ==  4:
          self.buffer.update( self.sdk_version )

        elif encoder ==  6:
          self.buffer.update( self.device_id )

        elif encoder ==  8:
          self.buffer.update( '%s:%d' % (self.device_name, self.sdk_version) )

        elif encoder ==  10:
          self.buffer.update( self.locale )

        elif encoder ==  12:
          self.buffer.update( self.country )

        elif encoder ==  14:
          self.buffer.update( self.operator_alpha )

        elif encoder ==  16:
          self.buffer.update( self.sim_operator_alpha )

        elif encoder ==  18:
          self.buffer.update( self.operator_code )

        elif encoder ==  20:
          self.buffer.update( self.sim_operator_code )
          header_len = len( self.buffer.buffer ) + 1

        elif encoder ==  22:
          self.buffer.update( len( self.package_name ) + 2 )

        elif encoder ==  24:
          self.buffer.update( self.package_name )

    self.buffer.buffer = self.pad + ProtocolBuffer().update( header_len ) + self.pad + self.buffer.buffer

    return self.buffer.finalize()


