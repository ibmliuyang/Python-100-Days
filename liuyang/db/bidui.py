import mysql.connector
import pandas as pd

# 数据库连接配置
db_config = {
    'host': '183.60.103.150',
    'user': 'root',
    'password': 'RooT@Tw123456',
    'port': 3306,
}


def get_table_columns(db_name):
    """获取指定数据库的所有表及其字段信息"""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = %s;
    """

    cursor.execute(query, (db_name,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return pd.DataFrame(result)


def compare_databases(db1_name, db2_name):
    """比较两个数据库的表结构"""
    df1 = get_table_columns(db1_name)
    df2 = get_table_columns(db2_name)

    # 添加来源标识
    df1['source'] = db1_name
    df2['source'] = db2_name

    # 合并两个DataFrame以找出不同之处
    diff = pd.concat([df1, df2]).drop_duplicates(subset=['TABLE_NAME', 'COLUMN_NAME', 'DATA_TYPE', 'IS_NULLABLE'],
                                                 keep=False)

    return diff


if __name__ == "__main__":
    # 比较两个数据库
    differences = compare_databases('a', 'aa')

    if not differences.empty:
        print("Differences found:")
        print(differences)
    else:
        print("No differences found.")