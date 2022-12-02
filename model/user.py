from helper import sql
from context import app, db
from log import logger

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    user_name = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(10), nullable=False)
    mail = db.Column(db.String(55), nullable=True)
    phone = db.Column(db.String(20), nullable=False)
    major = db.Column(db.String(55), nullable=False)
    campus = db.Column(db.String(55), nullable=False)
    institution = db.Column(db.String(55), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.decode().user_name

    def json(self):
        self = self.decode()
        return {'user_name': self.user_name, 'password': self.password, 'gender': self.gender,
                'mail': self.mail, 'phone': self.phone, 'major': self.major,
                'campus': self.campus, 'institution': self.institution}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        self.decode()

    @classmethod
    def query_all(cls):
        logger.info('Start to retrieve all object from DB')
        return [item.decode() for item in cls.query.all()]

    @classmethod
    def create_user(cls, user_name, password, mail):
        obj = cls(user_name=user_name, password=password, mail=mail)
        with sql.Db_connection('127.70.14.86', 'root',
                               'Buaa2022', 'tttt') as [db, cursor]:
            sql.insert(cursor, 'user', ['user_name', 'password', 'mail'], [
                obj.user_name, obj.password, obj.mail])
            db.commit()
        return obj

    @classmethod
    def query_by_username_and_email(cls, user_name, email):
        with sql.Db_connection('127.70.14.86', 'root',
                               'Buaa2022', 'tttt') as [db, cursor]:
            obj = sql.select(cursor, ['*'], 'user',
                             'where user_name = %s and mail = %s' % (user_name, email))
        if obj:
            obj = cls(user_name=obj['user_name'],
                      password=obj['password'], mail=obj['mail'])
        return obj.decode()

    @classmethod
    def query_by_username(cls, user_name):
        with sql.Db_connection('127.70.14.86', 'root',
                               'Buaa2022', 'tttt') as [db, cursor]:
            obj = sql.select(cursor, ['*'], 'user',
                             'where user_name = %s' % user_name)
        if obj:
            obj = cls(user_name=obj['user_name'],
                      password=obj['password'], mail=obj['mail'])
        return obj.decode()

    @classmethod
    def update_password(self, password):
        self.password = password
        with sql.Db_connection('127.70.14.86', 'root',
                               'Buaa2022', 'tttt', 3306) as [db, cursor]:
            obj = sql.update(cursor, ['password'], 'user', [password],
                             'where user_name = %s' % self.user_name)
            db.commit()
        return self

    def decode(self):
        if self:

            if type(self.user_name) is bytes:
                self.user_name = self.user_name.decode('utf-8')

            if type(self.password) is bytes:
                self.password = self.password.decode('utf-8')

            if type(self.gender) is bytes:
                self.gender = self.gender.decode('utf-8')

            if type(self.mail) is bytes:
                self.mail = self.mail.decode('utf-8')

            if type(self.phone) is bytes:
                self.phone = self.phone.decode('utf-8')

            if type(self.major) is bytes:
                self.major = self.major.decode('utf-8')

            if type(self.campus) is bytes:
                self.campus = self.campus.decode('utf-8')

            if type(self.institution) is bytes:
                self.institution = self.institution.decode('utf-8')

        return self


if __name__ == "__main__":
    # NOTE: add `with app.app_context():` to test locally

    with app.app_context():
        User.query_all()