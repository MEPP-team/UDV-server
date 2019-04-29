#!/usr/bin/env python3
# coding: utf8

import unicodedata

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from util.db_config import Base
from util.encryption import encrypt
from util.encryption import *
from util.serialize import serialize

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)


    def update(self, new_values):
        for attKey, attVal in new_values.items():
            if hasattr(self, attKey):
                if(attVal):
                    setattr(self, attKey, attVal)
                else:
                    setattr(self, attKey, None)
        if 'password' in new_values:
            self.password = encrypt(new_values['password'])
        return self

    @classmethod
    def get_attr(cls, attr_name):
        if hasattr(cls, attr_name):
            return getattr(cls, attr_name)
        return None

    def get_all_attr(self):
        return {i for i in dir(self)
                if not (i.startswith('_')
                        or callable(getattr(self, i))
                        or i == "metadata")}

    def serialize(self):
        serialized_object = {}
        for attr in self.get_all_attr():
            serialized_object[attr] = serialize(getattr(self, attr))
        return serialized_object
