"""
File consists API routes and functions.
"""


import collections
import io
import zipfile
from typing import Union

from flask import request, Blueprint

from app import db
from app.models import ZipFileInfo, AnalyzeInfo

app = Blueprint('archivePreviewer', __name__)


@app.route('/', methods=['GET'])
def get_checked_files() -> Union[collections.defaultdict, dict, list]:
    """
    API GET /. Get all previous checked files.
    :return: JSON with fields:
        {
            'response':
            {
                'content' - list of files with their paths and sizes
                'file' - name of checked zip file
            },
            'status' - status of query (SUCCESS or ERROR)
        }
    :rtype: Union[collections.defaultdict, dict, list]
    """
    results = db.session.query(AnalyzeInfo, ZipFileInfo).join(ZipFileInfo).all()
    answer = {'status': 'SUCCESS', 'response': []}
    files = {}
    for file_info, zip_file_info in results:
        if zip_file_info.id not in files:
            files[zip_file_info.id] = {'file': zip_file_info.filename,
                                       'content': [{'path': file_info.filename,
                                                    'size': file_info.file_size}]}
        else:
            files[zip_file_info.id]['content'].append({'path': file_info.filename,
                                                       'size': file_info.file_size})

    for key, value in files.items():
        answer['response'].append({**{'id': key}, **value})
    return answer


def get_info_about_file(zip_file: zipfile, filename: str) -> Union[collections.defaultdict, dict]:
    """
    Function get opened zip file and filename from that file, and return dict of relative path in
    zip file and size of file
    :param zip_file: zipfile library object
    :type zip_file: zipFile Object
    :param filename: name of file in that zipFile
    :type filename:  str
    :return: dictionary with filename and size of that file
    :rtype: Union[collections.defaultdict, dict]
    """
    file_info = zip_file.getinfo(filename)
    return {'path': filename, 'size': int(file_info.file_size)}


@app.route('/', methods=['POST'])
def post_zip() -> Union[collections.defaultdict, dict, list]:
    """
    API POST /. Post zip file for analyzing files inside
    :return: JSON with information about each file in zip archive
    :rtype: Union[collections.defaultdict, dict, list]
    """
    if 'file' not in request.files:
        return {'status': 'ERROR', 'description': 'No file'}
    file = request.files['file']
    if file.filename.rsplit('.', 1)[1] != 'zip':
        return {'status': 'ERROR', 'description': "It's not a .ZIP file"}
    zip_file = ZipFileInfo(filename=file.filename)
    db.session.add(zip_file)
    db.session.flush()
    db.session.refresh(zip_file)
    answer = {'status': 'SUCCESS', 'response': {'file': file.filename, 'content': []}}
    with zipfile.ZipFile(io.BytesIO(file.read())) as sended_zip_file:
        for filename in [x for x in sended_zip_file.namelist() if not x.endswith('/')]:
            result = get_info_about_file(sended_zip_file, filename)
            info_file = AnalyzeInfo(zip_file_id=zip_file.id,
                                    filename=result['path'],
                                    file_size=result['size'])
            db.session.add(info_file)
            answer['response']['content'].append(result)
    db.session.commit()
    return answer
