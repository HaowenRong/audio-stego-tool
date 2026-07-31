from cryptography.fernet import Fernet

def generateKey():
  return Fernet.generate_key()

def encryptText(text, key):
  fernet = Fernet(key)
  encryptedText = fernet.encrypt(text.encode())

  return encryptedText.decode()

def decryptText(encryptedText, key):
  fernet = Fernet(key)
  decryptedText = fernet.decrypt(encryptedText.encode())

  return decryptedText.decode()
