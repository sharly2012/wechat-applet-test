#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author: sharly

import pymysql
from utils.baseutil import BaseUtil
from utils.logger import Logger

logger = Logger(logger="MysqlDB").get_log()
db_host = BaseUtil().get_config_value("MySql", "host")
port = BaseUtil().get_config_value("MySql", "port")
username = BaseUtil().get_config_value("MySql", "username")
password = BaseUtil().get_config_value("MySql", "password")
db_name = BaseUtil().get_config_value("MySql", "db_name")
charset = BaseUtil().get_config_value("MySql", "charset")


class MySql(object):
    def __init__(self):
        try:
            self.connection = pymysql.connect(host=db_host,
                                              port=int(port),
                                              user=username,
                                              password=password,
                                              database=db_name,
                                              charset=charset)
        except pymysql.err.OperationalError as e:
            logger.info("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def create_db(self, sql_query):
        con = self.connection
        cursor = con.cursor()
        try:
            cursor.execute(sql_query)
            con.close()
        except pymysql.err.ProgrammingError as e:
            logger.info("Create DB fail, %d: %s" % (e.args[0], e.args[1]))

    def select_query(self, sql_query):
        con = self.connection
        cursor = con.cursor()
        try:
            cursor.execute(sql_query)
            query_result = cursor.fetchall()
            con.close()
        except pymysql.err.ProgrammingError as e:
            logger.info("Select Error %d: %s" % (e.args[0], e.args[1]))
        return query_result

    def insert_query(self, sql_query):
        con = self.connection
        cursor = con.cursor()
        try:
            cursor.execute(sql_query)
            con.commit()
            con.close()
        except pymysql.err.ProgrammingError as e:
            con.rollback()
            logger.info("Insert Fail, %d: %s" % (e.args[0], e.args[1]))

    def update_query(self, sql_query):
        con = self.connection
        cursor = con.cursor()
        try:
            cursor.execute(sql_query)
            con.commit()
            con.close()
        except pymysql.err.ProgrammingError as e:
            con.rollback()
            logger.info("Update Fail, %d: %s" % (e.args[0], e.args[1]))

    def delete_query(self, sql_query):
        con = self.connection
        cursor = con.cursor()
        try:
            cursor.execute(sql_query)
            con.commit()
            con.close()
        except pymysql.err.ProgrammingError as e:
            con.rollback()
            logger.info("Delete Fail, %d: %s" % (e.args[0], e.args[1]))


if __name__ == '__main__':
    query = "select * from tfb_template where mongodb_id = '5be11060f44fd07527ae9513';"
    result = MySql().select_query(query)
    print(result)
