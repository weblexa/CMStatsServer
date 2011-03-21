from cmstats.database import Base, DBSession
from cmstats.utils.string import parse_modversion
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.expression import func


class Device(Base):
    __tablename__ = "devices"

    id = Column('id', Integer, primary_key=True)
    hash = Column('hash', String(32), unique=True)
    name = Column('name', String(50), index=True)
    version = Column('version', String(50), index=True)
    country = Column('country', String(50), index=True)
    carrier_id = Column('carrier_id', String(50), index=True)
    kang = Column('kang', Integer, index=True)
    date_added = Column('date_added', DateTime)
    date_updated = Column('date_updated', DateTime)


    @classmethod
    def count(cls):
        session = DBSession()

        q = session.query(cls).count()
        return q

    @classmethod
    def device_count(cls):
        session = DBSession()

        q = session.query(func.count(cls.name), cls.name) \
            .group_by(cls.name).all()

        q = sorted(q, key=lambda x: x[0], reverse=True)

        return q

    @classmethod
    def add(cls, **kwargs):
        # Clean up the version.
        version = parse_modversion(kwargs['version'])

        # Grab a session
        session = DBSession()

        # Grab device record, if it already exists.
        try:
            obj = session.query(cls).filter(cls.hash == kwargs['hash']).one()
        except:
            obj = cls()
            obj.date_added = func.now()

        # Flag this as a KANG if necessary.
        if version == None:
            version = kwargs['version']
            obj.kang = 1
        else:
            obj.kang = 0

        # Populate the rest of the records.
        obj.hash = kwargs['hash']
        obj.name = kwargs['name']
        obj.version = version
        obj.country = kwargs['country']
        obj.carrier_id = kwargs['carrier_id']
        obj.date_updated = func.now()

        session.add(obj)
        session.commit()
