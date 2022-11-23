from datetime import datetime

from log import logger
from main import db


# Job is template Model

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(255), unique=True, nullable=False)
    server_type = db.Column(db.String(255), nullable=False)
    status  = db.Column(db.String(255), nullable=False)
    submit_time = db.Column(db.DateTime, nullable=True)
    update_time = db.Column(db.DateTime, default=datetime.now(),onupdate=datetime.now(), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    sim_range = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Job %r>' % self.decode().job_id

    def json(self):
        self = self.decode()
        return {'job_id': self.job_id, 'server_type': self.server_type,'status':self.status,
                'update_time':str(self.update_time), 'submit_time':str(self.submit_time),'create_time':str(self.create_time),'sim_range': self.sim_range}

    # todo
    # complete curd

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        self.decode()

    @classmethod
    def query_by_job_id(cls, job_id):
        obj = cls.query.filter_by(job_id=job_id).first()
        if obj:
            obj = obj.decode()
        return obj

    @classmethod
    def query_all(cls):
        logger.info('Start to retrieve all object from DB')
        return [item.decode() for item in cls.query.all()]

    @classmethod
    def create_job(cls, job_id, status, server_type, sim_range):
        obj = cls(job_id=job_id, status=status, server_type=server_type, sim_range=sim_range).decode()
        obj.create_time = datetime.now()
        db.session.add(obj)
        db.session.commit()
        return obj

    def decode(self):
        if self:

            if type(self.job_id) is bytes:
                self.job_id = self.job_id.decode('utf-8')

            if type(self.status) is bytes:
                self.status = self.status.decode('utf-8')

            if type(self.server_type) is bytes:
                self.server_type = self.server_type.decode('utf-8')

            if type(self.sim_range) is bytes:
                self.sim_range = self.sim_range.decode('utf-8')

        return self
