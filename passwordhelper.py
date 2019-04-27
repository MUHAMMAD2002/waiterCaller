import hashlib, os, base64

class PasswordHelper:
 
  def get_hash(self, plain): # plain = 123456
    plain_encode = plain.encode("utf-8")
    return hashlib.sha512(plain_encode).hexdigest() # This makes a hash 
    # 'ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413'

  def get_salt(self):
    salt = base64.b64encode(os.urandom(20)) # This first makes random number then 
    return salt.decode("utf-8")
  
  def validate_password(self, plain, salt, expected):
    return self.get_hash(plain + salt) == expected # return True or False
