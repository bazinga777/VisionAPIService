from image2tokens import extractTokens, extractLines
from ocr import Ocr
import json
from google.cloud import storage
import os

def changeFileExtension(path, newExtension):
    res = ''.join(path.split(".")[:-1]) + '.' + newExtension  #join to merge sequence of strings
    print("res:",res)
    return res


def convertImageToText(imagePath):

    # Create OCR
    ocr = Ocr()

    # Run OCR over image. It generates a JSON with the text and the coordinates of each word
    jsonFile = ocr.processFile(imagePath, './')

    # Read JSON
    # jsonFile = changeFileExtension(imagePath.split("/")[-1], "json")
    # with open(jsonFile, 'r') as f:
    #     image = json.load(f)

    # Extract tokens (Each word, its width, height and its coordinates)
    #tokens = extractTokens(image)
    tokens = extractTokens(jsonFile)

    # Sort the tokens into lines
    lines = extractLines(tokens)

    txt = ""
    response = {}
    linesList = []
    for line in lines:
        print(json.dumps(line))

        linesList.append(line)

        line = list(filter(lambda x: x != "–", line))
        try:
            txt += "{:>40}{:>40}{:>40}{:>40}\n".format(line[0], line[1], line[2], line[3])
        except:
            try:
                txt += "{:>40}{:>40}\n".format(line[0], line[1])
            except:
                pass

    # with open(changeFileExtension(imagePath.split("/")[-1], "txt"), 'w') as f:
    #     f.write(txt)

    response["0"] = linesList
    return json.dumps(response, indent=4)

def getPathToGCPBucket(fileName):
    cwd = os.getcwd()
    print(cwd)
    #client = storage.Client.from_service_account_json(os.path.join(cwd , "src/credential.json"))
    client = storage.Client.from_service_account_json(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    bucket = client.get_bucket("vision_demo_2020")
    blob = bucket.blob(fileName)
    # with open(os.path.join(cwd,"sample/"+ fileName), "wb") as file_obj:
    #     blob.download_to_file(file_obj)
    with open(os.path.join(cwd, "/tmp/" + fileName), "wb") as file_obj:
        blob.download_to_file(file_obj)
    return ''
# imagePath = sys.argv[1]
# print('RUNNING ON ' + imagePath)
# convertImageToText(imagePath)
