from DB.dbconnection import connection_db
from mysql.connector import OperationalError

class db_interaction:
    def __init__(self):
        self.db_conf = connection_db()
        self.db_conf.db_connect()
        self.db_operate = self.db_conf.db_cnx()

    async def comment_info_data(self, comment, filename):
        dt_info = False

        cursor = self.db_operate.cursor()
        create_comment = """INSERT INTO `comment_info` (comment, image_name)
                            VALUES (%s, %s);"""
        create_data = (comment, filename)

        cursor.execute(create_comment, create_data)
        if cursor.rowcount == 1:
            self.db_operate.commit()
            dt_info = True
        else:
            self.db_operate.rollback()

        if cursor is not None:
            cursor.close()

        return dt_info
        

    async def create_comment_info(self, commnet, filename):
        _result = False
        try:
            _result = await self.comment_info_data(commnet, filename)
            return _result
        except OperationalError:
            self.db_conf.restart_connect()

            try:
                _result = await self.comment_info_data(commnet, filename)
                return _result
            except Exception:
                return False
        except Exception as e:
            print("create error,"+str(e))
            return False    

    async def get_comment(self):
        dt_info = False

        cursor = self.db_operate.cursor()
        cursor.execute("""SELECT comment AS comm, image_name AS imgName FROM `comment_info`;""")
        findAll = cursor.fetchall()

        if findAll != []:
            dt_info = findAll

        if cursor is not None:
            cursor.close()

        return dt_info

    async def get_comment_to_update_frontend(self):
        dt_info = False

        cursor = self.db_operate.cursor()
        cursor.execute("""SELECT comment, image_name FROM `comment_info` 
                        ORDER BY id DESC LIMIT 1;""")
        findOne = cursor.fetchone()

        if findOne != None:
            dt_info = findOne

        if cursor is not None:
            cursor.close()

        return dt_info

    async def query_comment_info(self, times):
        _result = False
        try:
            if times == 1:
                _result = await self.get_comment()
            elif times == 2:
                _result = await self.get_comment_to_update_frontend()
            return _result
        except OperationalError:
            self.db_conf.restart_connect()
            try:
                if times == 1:
                    _result = await self.get_comment()
                elif times == 2:
                    _result = await self.get_comment_to_update_frontend()
                return _result
            except Exception:
                return False
        except Exception as e:
            print("query error,"+str(e))
            return False

