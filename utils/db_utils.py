import sqlite3


def initialize_database():
    db_path = 'lark_utils.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建配置表
    # id: 整数类型，主键，自动递增。
    # key: 文本类型，不能为空，并且必须是唯一的。
    # value: 文本类型，不能为空。
    # description: 文本类型，可为空。
    # typez: #文本类型，不能为空，并且必须是 'string', 'integer', 'boolean', 'float' 之一。
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configurations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL,
            description TEXT,
            type TEXT NOT NULL CHECK(type IN ('string', 'integer', 'boolean', 'float'))
        )
        ''')

    # 创建文本历史表
    # id: 整数类型，主键，自动递增。
    # title: 标题
    # text_content: 文本类型，不能为空。
    # created_at: 日期时间类型，默认值为当前时间戳。
    # updated_at: 日期时间类型，默认值为当前时间戳，并且在每次更新记录时自动更新为当前时间戳。
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS text_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            text_content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

    # 创建触发器
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_timestamp
        AFTER UPDATE ON text_history
        FOR EACH ROW
        BEGIN
            UPDATE text_history SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
        END;
        ''')

    # 插入初始数据
    # initial_data = [
    #     ('Alice', 'alice@example.com', 30),
    #     ('Bob', 'bob@example.com', 25),
    #     ('Charlie', 'charlie@example.com', 35)
    # ]
    # cursor.executemany("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", initial_data)

    # 提交事务
    conn.commit()

    # 关闭连接
    cursor.close()
    conn.close()
