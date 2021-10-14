# -*- coding: utf-8 -*-
"""File models.py contains the descriptions of all tables in the SQLite database"""

from app import db


class ZipFileInfo(db.Model):  # pylint: disable=too-few-public-methods
    """
    Table zip_file_info with information about each checked zip file
    Fields:
        id: primary key of each zip file
        filename: name of zip file
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)


class AnalyzeInfo(db.Model):  # pylint: disable=too-few-public-methods
    """
    Table analyze_info with information about each checked file in zip file
    Fields:
        id: primary key of each zip file.
        zip_file_id: foreign key with zip_file_info.
            Connection zip file and file inside that zip file.
        filename: name of file
        file_size: size of file
    """
    id = db.Column(db.Integer, primary_key=True)
    zip_file_id = db.Column(db.Integer, db.ForeignKey('zip_file_info.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
