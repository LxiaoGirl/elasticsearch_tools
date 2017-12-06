#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: xiaoL-pkav l@pker.in
@version: 2015/5/20 15:09
"""

from config.database import DB_USER, DB_HOST, DB_LIB, DB_PORT, DB_PWD, DB_TYPE
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# 构建sqlalchemy的session
def init_db(db_name = ''):
    connect = "%s+%s://%s:%s@%s:%s/%s?charset=utf8" % (DB_TYPE, DB_LIB, DB_USER, DB_PWD, DB_HOST, DB_PORT, db_name)
    engine = create_engine(connect, connect_args={'connect_timeout': 999999999})
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return engine, session