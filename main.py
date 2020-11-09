import base64

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from passporteye import read_mrz

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/process', methods=['POST', 'OPTIONS'])
@cross_origin()
def process():
    if (request.method=='POST'):
        content = request.json

        if 'image' in content:
            image = base64.b64decode(content['image'])
            mrz = read_mrz(image, extra_cmdline_params='--oem 0 --tessdata-dir data --l OCRB-3')
            if mrz != None:
                res = mrz.to_dict()
                if res['valid_score'] < 50:
                     return jsonify({'error': 'Not parsed'})
                else:
                    for k in res:
                        try:
                            res[k] = res[k].replace('<', '')
                        except:
                            pass
                    return jsonify(res)
            else:
                return jsonify({'error': 'Not parsed'})
        else:
            return jsonify({'error': 'No image provided'})
    else:
        return jsonify({})

if __name__ == '__main__':
    #mrz = read_mrz('raw1.jpg', extra_cmdline_params='--oem 0 --tessdata-dir data -l OCRB-3')
    #print(mrz.__dict__)
    app.run(host= '0.0.0.0', port='3002', debug=True)
