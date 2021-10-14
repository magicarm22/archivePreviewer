import fileinput
import io
import zipfile

from flask import request, Blueprint

from app import db
from app.models import ZipFileInfo, AnalyzeInfo


app = Blueprint('archivePreviewer', __name__)

@app.route('/', methods=['GET'])
def getCheckedFiles():
    results = db.session.query(AnalyzeInfo, ZipFileInfo).join(ZipFileInfo).all()
    answer = {'status': 'SUCCESS', 'response': []}
    files = {}
    for file_info, zip_file_info in results:
        if zip_file_info.id not in files:
            files[zip_file_info.id] = {'file': zip_file_info.filename, 'content': [{'path': file_info.filename, 'size': file_info.file_size}]}
        else:
            files[zip_file_info.id]['content'].append({'path': file_info.filename, 'size': file_info.file_size})

    for key, value in files.items():
        answer['response'].append({**{'id': key}, **value})
    return answer


def getInfoAboutFile(zip_file, filename):
    file_info = zip_file.getinfo(filename)
    return {'path': filename, 'size': int(file_info.file_size)}


@app.route('/', methods=['POST'])
def postZIP():
    if 'file' not in request.files:
        return {'status': 'ERROR', 'description': 'No file'}
    file = request.files['file']
    if file.filename.rsplit('.', 1)[1] != 'zip':
        return {'status': 'ERROR', 'description': "It's not a .ZIP file"}
    zip_file = ZipFileInfo(filename=file.filename)
    db.session.add(zip_file)
    db.session.flush()
    db.session.refresh(zip_file)
    sended_zip_file = zipfile.ZipFile(io.BytesIO(file.read()))
    answer = {'status': 'SUCCESS', 'response': {'file': file.filename, 'content': []}}
    for filename in [x for x in sended_zip_file.namelist() if not x.endswith('/')]:
        result = getInfoAboutFile(sended_zip_file, filename)
        info_file = AnalyzeInfo(zip_file_id=zip_file.id, filename=result['path'], file_size=result['size'])
        db.session.add(info_file)
        answer['response']['content'].append(result)
    db.session.commit()
    return answer
