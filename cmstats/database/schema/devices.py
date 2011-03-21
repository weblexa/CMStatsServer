from cmstats.database import Base, DBSession
from cmstats.utils.string import parse_modversion
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.expression import func


class Device(Base):
    __tablename__ = "devices"

    id = Column('id', Integer, primary_key=True)
    hash = Column('hash', String, unique=True)
    name = Column('name', String, index=True)
    version = Column('version', String)
    country = Column('country', String)
    carrier_id = Column('carrier_id', String)
    kang = Column('kang', Integer, index=True)
    date_added = Column('date_added', DateTime)
    date_updated = Column('date_updated', DateTime)

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

        # Populate the rest of the records.
        obj.hash = kwargs['hash']
        obj.name = kwargs['name']
        obj.version = version
        obj.country = kwargs['country']
        obj.carrier_id = kwargs['carrier_id']
        obj.date_updated = func.now()

        session.add(obj)
        session.commit()
