"""
File with all tests for the archivePreviewer project
"""

import io
import json
import os
import zipfile

import pytest
from flask import Flask

from app import create_app, db
from app.views import get_info_about_file


@pytest.fixture(name='app')
def testing_app() -> Flask:
    """
    Create test application with testing configuration and testing database.
    :return: Flask application object
    :rtype: Flask
    """
    app = create_app("app.config.TestingConfig")
    with app.app_context():
        db.drop_all()
        db.create_all()
    return app


def test_empty_db(app: Flask) -> None:
    """
    Function is testing get information from empty database
    :param app: Flask testing application
    :type app: Flask
    """
    client = app.test_client()
    res = client.get('/')
    assert res.status == '200 OK'
    assert {'status': 'SUCCESS', 'response': []} == json.loads(res.data.decode())


def test_add_zip_without_files(app: Flask) -> None:
    """
    Function is testing sending empty zip file
    :param app: Flask testing application
    :type app: Flask
    """
    client = app.test_client()
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    with open(os.path.join(current_directory, 'files\\empty.zip'), 'rb') as file:
        data = {'file': (io.BytesIO(file.read()), 'empty.zip')}
    res = client.post('/', content_type='multipart/form-data', data=data)
    assert res.status == '200 OK'
    assert {'response': {
                'content': [],
                'file': 'empty.zip'
            }, 'status': 'SUCCESS'} == json.loads(res.data.decode())


def test_add_zip_with_big_files(app: Flask) -> None:
    """
    Function is testing sending zip file with big size files inside.
    :param app: Flask testing application
    :type app: Flask
    """
    client = app.test_client()
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    with open(os.path.join(current_directory, 'files\\someBigFiles.zip'), 'rb') as file:
        data = {'file': (io.BytesIO(file.read()), 'someBigFiles.zip')}
    res = client.post('/', content_type='multipart/form-data', data=data)
    assert res.status == '200 OK'
    assert {'response': {'content': [{'path': 'bncache.dat', 'size': 1200514},
                                     {'path': 'game.dll', 'size': 12042240},
                                     {'path': 'War3Patch.mpq', 'size': 45620324},
                                     {'path': 'War3xLocal.mpq', 'size': 36615390}],
                         'file': 'someBigFiles.zip'},
            'status': 'SUCCESS'} == json.loads(res.data.decode())


def test_add_zip_with_folders(app: Flask) -> None:
    """
    Function is testing sending zip file with files and folders in that zip file
    :param app: Flask testing application
    :type app: Flask
    """
    client = app.test_client()
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    with open(os.path.join(current_directory, 'files\\zipWithFolders.zip'), 'rb') as file:
        data = {'file': (io.BytesIO(file.read()), 'zipWithFolders.zip')}
    res = client.post('/', content_type='multipart/form-data', data=data)
    assert res.status == '200 OK'
    assert {'response': {'content': [
            {'path': 'Nexus/folder1/flash-all.sh', 'size': 750},
            {'path': 'Nexus/folder1/flash-base.sh', 'size': 705},
            {'path': 'Nexus/folder2/flash-all.bat', 'size': 862},
            {'path': 'Nexus/folder2/folder3/bootloader-flounder-3.48.0.0135.img', 'size': 2968354}],
         'file': 'zipWithFolders.zip'}, 'status': 'SUCCESS'} == json.loads(res.data.decode())


def test_get_info_function() -> None:
    """
    Function is testing get_info_about_file function and check the result.
    """
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    with zipfile.ZipFile(os.path.join(current_directory, 'files\\oneFile.zip')) as zip_object:
        res = get_info_about_file(zip_object, 'dotnetfx.exe')
    assert res == {'path': 'dotnetfx.exe', 'size': 21823560}
