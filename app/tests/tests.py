import io
import json
import os
import zipfile

import pytest

from app import create_app, db
from app.views import getInfoAboutFile


@pytest.fixture
def app():
    app = create_app("app.config.TestingConfig")
    with app.app_context():
        db.drop_all()
        db.create_all()
    return app


def test_empty_db(app):
    client = app.test_client()
    res = client.get('/')
    assert '200 OK' == res.status
    assert {'status': 'SUCCESS', 'response': []} == json.loads(res.data.decode())


def test_add_zip_without_files(app):
    client = app.test_client()
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    with open(os.path.join(current_directory, 'files\\empty.zip'), 'rb') as f:
        data = {'file': (io.BytesIO(f.read()), 'empty.zip')}
    res = client.post('/', content_type='multipart/form-data', data=data)
    assert '200 OK' == res.status
    assert {'response': {'content': [], 'file': 'empty.zip'}, 'status': 'SUCCESS'} == json.loads(res.data.decode())


def test_add_zip_with_big_files(app):
    client = app.test_client()
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    with open(os.path.join(current_directory, 'files\\someBigFiles.zip'), 'rb') as f:
        data = {'file': (io.BytesIO(f.read()), 'someBigFiles.zip')}
    res = client.post('/', content_type='multipart/form-data', data=data)
    assert '200 OK' == res.status
    assert {'response': {'content': [{'path': 'bncache.dat', 'size': 1200514},
                                     {'path': 'game.dll', 'size': 12042240},
                                     {'path': 'War3Patch.mpq', 'size': 45620324},
                                     {'path': 'War3xLocal.mpq', 'size': 36615390}],
                         'file': 'someBigFiles.zip'}, 'status': 'SUCCESS'} == json.loads(res.data.decode())


def test_add_zip_with_folders(app):
    client = app.test_client()
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    with open(os.path.join(current_directory, 'files\\zipWithFolders.zip'), 'rb') as f:
        data = {'file': (io.BytesIO(f.read()), 'zipWithFolders.zip')}
    res = client.post('/', content_type='multipart/form-data', data=data)
    assert '200 OK' == res.status
    assert {'response': {'content': [{'path': 'Nexus/folder1/flash-all.sh', 'size': 750},
                                     {'path': 'Nexus/folder1/flash-base.sh', 'size': 705},
                                     {'path': 'Nexus/folder2/flash-all.bat', 'size': 862},
                                     {'path': 'Nexus/folder2/folder3/bootloader-flounder-3.48.0.0135.img',
                                      'size': 2968354}],
                         'file': 'zipWithFolders.zip'}, 'status': 'SUCCESS'} == json.loads(res.data.decode())


def test_get_info_function():
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    with open(os.path.join(current_directory, 'files\\oneFile.zip'), 'rb') as f:
        zip = zipfile.ZipFile(io.BytesIO(f.read()))
        res = getInfoAboutFile(zip, 'dotnetfx.exe')
        assert res == {'path': 'dotnetfx.exe', 'size': 21823560}
