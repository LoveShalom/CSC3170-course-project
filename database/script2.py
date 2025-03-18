import sqlite3

# 连接到数据库
conn = sqlite3.connect('csc3170.db')
c = conn.cursor()

# 添加新列
status = "Making"
c.execute("UPDATE orders SET status = (?) WHERE id = (?)", (status, 7))

# 提交事务
conn.commit()

# 关闭连接
conn.close()
