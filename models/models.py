from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Date, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(120), unique=True, nullable=False)
    position = Column(String(100))
    slack_id = Column(String(11), unique=True, nullable=False)

    user = relationship("UsersRolesRelation")

    def __repr__(self):
        return '<User {}>'.format(self.full_name, self.position)


class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    role_name = Column(String(100), nullable=False)


class UsersRolesRelation(Base):
    __tablename__ = "users_roles_relation"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    role_id = Column(Integer, ForeignKey('roles.id', ondelete="CASCADE"))

    user = relationship("User", back_populates="user_roles_relation")
    roles = relationship("Roles", back_populates="user_roles_relation")


class Bonus(Base):
    __tablename__ = "type_bonus"
    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False)
    description = Column(Text)

    def __repr__(self):
        return '<Bonus {}>'.format(self.type, self.description)


class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    creator = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"))
    status = Column(String(100), nullable=False)
    reviewer = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"))
    type_bonus = Column(Integer, ForeignKey('type_bonus.id', ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    payment_date = Column(Date)
    payment_amount = Column(Integer, default=1)
    description = Column(Text)

    creator_user = relationship("User", back_populates="requests")
    user_reviewer = relationship("User", back_populates="requests")
    bonus_type = relationship("Bonus", back_populates="requests")
    request_history = relationship("RequestHistory")

    def __repr__(self):
        return '<Request {}>'.format(self.creator, self.status, self.payment_date)


class RequestHistory(Base):
    __tablename__ = "requests_history"
    id = Column(Integer, primary_key=True)
    status = Column(String(100), nullable=False, default='created')
    timestamp = Column(DateTime, server_default=func.now())
    request_id = Column(Integer, ForeignKey('requests.id'))
