import fileinput
import zipfile

from flask import request

from app import app


@app.route('/', methods=['GET'])
def getCheckedFiles():
    return 'HELLO!'
    pass


def getInfoAboutFile(file):
    sended_zip_file = zipfile.ZipFile(file)
    result = {'status': 'SUCCESS', 'response': {'file': file.filename, 'content': []}}
    for filename in sended_zip_file.namelist():
        file_info = sended_zip_file.getinfo(filename)
        result['response']['content'].append({'path': filename, 'size': int(file_info.file_size)})
    return result


@app.route('/', methods=['POST'])
def postZIP():
    if 'file' not in request.files:
        return {'status': 'ERROR', 'description': 'No file'}
    file = request.files['file']
    if file.filename.rsplit('.', 1)[1] != 'zip':
        return {'status': 'ERROR', 'description': "It's not a .ZIP file"}
    result = getInfoAboutFile(file)
    return result
