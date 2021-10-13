from app import db


class ZipFileInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)


class AnalyzeInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zip_file_id = db.Column(db.Integer, db.ForeignKey('zip_file_info.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
