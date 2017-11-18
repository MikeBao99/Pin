from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3('2016-05-20', api_key='4a5dce0273f76cfc7fdebaec7d43f6828a512194')

def classify(url):
  return visual_recognition.classify(images_url=url)
