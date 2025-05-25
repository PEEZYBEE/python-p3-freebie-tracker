from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship("Freebie", back_populates="company")

    @property
    def devs(self):
        # Return unique devs who got freebies from this company
        return list({freebie.dev for freebie in self.freebies})

    def give_freebie(self, dev, item_name, value):
        # Create a new Freebie linked to this company and given dev
        new_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        return new_freebie

    @classmethod
    def oldest_company(cls, session):
        # Return company with earliest founding year
        return session.query(cls).order_by(cls.founding_year.asc()).first()


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship("Freebie", back_populates="dev")

    @property
    def companies(self):
        # Unique companies this dev has freebies from
        return list({freebie.company for freebie in self.freebies})

    def received_one(self, item_name):
        # Return True if dev has any freebie matching item_name
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, new_dev, freebie):
        # Only give away freebie if it belongs to this dev
        if freebie in self.freebies:
            freebie.dev = new_dev
            return freebie
        else:
            return None


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    dev = relationship("Dev", back_populates="freebies")
    company = relationship("Company", back_populates="freebies")

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
