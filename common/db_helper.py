import pymysql


class DBHelper:

    @staticmethod
    def clear_cart(user_id=8):
        """直接从数据库清空购物车"""
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123456",
            database="tpshop3.0",
            charset="utf8"
        )
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM tp_cart WHERE user_id = {user_id}")
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_cart_count(user_id=8):
        """查询购物车商品数量"""
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123456",
            database="tpshop3.0",
            charset="utf8"
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM tp_cart WHERE user_id = {user_id}")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count