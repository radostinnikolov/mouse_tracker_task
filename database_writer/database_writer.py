import sqlite3
import aiosqlite


class DatabaseWriter:
    def __init__(self):
        self.con = sqlite3.connect("./data.db")
        self.cursor = self.con.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS info")
        self.cursor.execute(""" CREATE TABLE info(
                        id int,
                        x int,
                        y int,
                        image_path text)""")
        self.cursor.execute(""" INSERT INTO info(id, x, y, image_path)
                                        VALUES(1,0,0,'')""")
        self.con.commit()
        self.con.close()

    async def save_data(self, type, *args):
        if type == 'coordinates':
            info = [int(x) for x in args]
            async with aiosqlite.connect("./data.db") as db:
                update_stmt = 'UPDATE info SET x=?, y=? WHERE id = ?'
                await db.execute(update_stmt, (info[0], info[1], 1))
                await db.commit()
                await db.close()

        elif type == 'image':
            info = args[0]
            async with aiosqlite.connect("./data.db") as db:
                update_stmt = 'UPDATE info SET image_path=? WHERE id = ?'
                await db.execute(update_stmt, (info, 1))
                await db.commit()
                await db.close()


# conn.close()