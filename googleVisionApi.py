import io
import os

from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson


class GoogleVisionApi:
    def __init__(self):
        # Instantiates a client
        self.client = vision.ImageAnnotatorClient()
        # Service that performs Google Cloud Vision API detection tasks over client images, such as face, landmark, logo, label, and text detection.
        # The ImageAnnotator service returns detected entities from the images.
        self.requestsCache = {}

    def request(self, imagePath):
        # Loads the image into memory
        with io.open(imagePath, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        # Performs label detection on the image file
        self.requestsCache[imagePath] = self.client.document_text_detection(
            image=image)  # document_text_detection performs doc text detection

        response = self.requestsCache[imagePath]
        # print("response", response)
        jsonText = MessageToJson(response)

        return jsonText

    def clear(self, requestName):
        if requestName in self.requestsCache:
            del self.requestsCache[requestName]

    def clearAll(self):
        self.requestsCache = {}
