from cryptography.fernet import Fernet
import base64, hashlib

# sets used to help validate user input
valid_blood_types = {'A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'}
valid_all_types = {'Immunophenotype', 'French-American-British (FAB)', 'ALL Cytogenetic Risk Group'}
valid_gender_types = {'Male', 'Female'}

# helper function to display the oncologist's name in the ToolBar
def getLastNameFromFullName(full_name):
    split = full_name.split()
    return split[-1].capitalize()

# helper function to delete all elements in a layout recursively
def clearLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clearLayout(item.layout())

# helper function used only by encryption/decryption methods
def generateFernetKey(passcode:bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('utf-8'))

# takes a plain text and the key in String format, returns encryptedText in String format
def encryptData(plainText, keyString):
    key = generateFernetKey(keyString.encode('utf-8'))
    fernet = Fernet(key)
    return fernet.encrypt(plainText.encode('utf-8')).decode("utf-8") 

# takes encrypted text and the key in String format, returns plain text in String format
def decryptData(encryptedText, keyString):
    key = generateFernetKey(keyString.encode('utf-8'))
    fernet = Fernet(key)
    return fernet.decrypt(encryptedText.encode('utf-8')).decode('utf-8')