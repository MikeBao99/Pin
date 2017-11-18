from flask import * #TODO: actually look at imports
import boto3
import requests
import json
import urllib
from werkzeug import * #TODO: actually look at imports
import classify as watson

views = Blueprint('views', __name__)

extensions = set(['jpg'])

def file_allowed(file):
	return '.' in file and \
		   file.rsplit('.', 1)[1] in extensions

@views.route('/', methods=["GET", "POST"])
def homepage():
	if request.method == "POST":

		s3 = boto3.resource('s3')

		bucket = s3.Bucket('imagen50')
		bucket.upload_fileobj(request.files['input-b1'], request.files['input-b1'].filename, ExtraArgs={'ContentType': 'image/jpeg'})
	
		link = 'https://s3.us-east-2.amazonaws.com/imagen50/%s' % urllib.quote_plus(request.files['input-b1'].filename)
		
		classifications = watson.classify(link)
		
		classes = {}
		classif = []
		for classification in classifications['images'][0]['classifiers'][0]['classes']:
			classes[classification['class']] = classification['score']
			classif.append(classification['class'])
		#classif = sorted(classes, key=lambda x: -classes[x])
				
		content = '<table class="table table-hover table-bordered text-center thead-light"><thead><tr><th>Rank</th><th>Guess</th></tr></thead><tbody>'       
		return render_template('homepage.html', WordCount =  content + "<tr><td>1st Guess</td><td>" + classif[0] + "</td></tr><tr><td>2nd Guess</td><td>" + classif[1] + "</td></tr><tr><td>3rd Guess</td><td>" + classif[2] +  "</td></tr></tbody></table>")
	else:
		return render_template('homepage.html', WordCount = "")
  
@views.route('/about')
def about():
	return render_template('about.html')


# def ocr_space_file(filename, overlay=False, api_key='6960bb930988957', language='eng'):
#     """ OCR.space API request with local file.
#         Python3.5 - not tested on 2.7
#     :param filename: Your file path & name.
#     :param overlay: Is OCR.space overlay required in your response.
#                     Defaults to False.
#     :param api_key: OCR.space API key.
#                     Defaults to 'helloworld'.
#     :param language: Language code to be used in OCR.
#                     List of available language codes can be found on https://ocr.space/OCRAPI
#                     Defaults to 'en'.
#     :return: Result in JSON format.
#     """

#     payload = {'isOverlayRequired': overlay,
#                'apikey': api_key,
#                'language': language,
#                }
#     with open(filename, 'rb') as f:
#         r = requests.post('https://api.ocr.space/parse/image',
#                           files={filename: f},
#                           data=payload,
#                           )
#     return r.content.decode()


# def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
#     """ OCR.space API request with remote file.
#         Python3.5 - not tested on 2.7
#     :param url: Image url.
#     :param overlay: Is OCR.space overlay required in your response.
#                     Defaults to False.
#     :param api_key: OCR.space API key.
#                     Defaults to 'helloworld'.
#     :param language: Language code to be used in OCR.
#                     List of available language codes can be found on https://ocr.space/OCRAPI
#                     Defaults to 'en'.
#     :return: Result in JSON format.
#     """

#     payload = {'url': url,
#                'isOverlayRequired': overlay,
#                'apikey': api_key,
#                'language': language,
#                }
#     r = requests.post('https://api.ocr.space/parse/image',
#                       data=payload,
#                       )
#     return r.content.decode()


