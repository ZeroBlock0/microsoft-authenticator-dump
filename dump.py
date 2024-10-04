import sqlite3
import uuid
import json
from urllib.parse import quote
import os
import logging
import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_otpauth_url(name, username, secret_key):
    """
    生成 otpauth URL，用于 TOTP（基于时间的一次性密码）。
    
    参数:
        name (str): 用户的姓名。
        username (str): 用户名。
        secret_key (str): OTP 秘钥。
        
    返回:
        str: 生成的 otpauth URL。
    """
    label = quote(f"{name}:{username}")
    issuer = quote(name)
    return f"otpauth://totp/{label}?secret={secret_key}&issuer={issuer}"

def fetch_accounts(database, account_type=0):
    """
    从 SQLite 数据库中获取指定 account_type 的账户信息。

    参数:
        database (str): SQLite 数据库文件路径。
        account_type (int): 账户类型，用于过滤查询。为1的是微软本身的账户，为0的是手动添加的第三方账户。

    返回:
        list: 包含账户信息的列表，每个元素为字典。
    """
    result = []
    try:
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, username, oath_secret_key 
                FROM accounts 
                WHERE account_type = ?
            """, (account_type,))

            for row in cursor:
                name, username, secret_key = row
                uuid_str = str(uuid.uuid4())
                otpauthstr = generate_otpauth_url(name, username, secret_key)
                result.append({
                    "uuid": uuid_str,
                    "name": name,  # 包含中文名
                    "otpauthstr": otpauthstr
                })
    except sqlite3.Error as e:
        logging.error(f"数据库错误: {e}")
    except Exception as ex:
        logging.error(f"发生未知错误: {ex}")
    return result

def save_json_to_file(data, filename):
    """
    将数据保存为 JSON 文件。
    
    参数:
        data (list): 要保存的数据。
        filename (str): 输出文件名。
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"JSON 数据已成功保存到 '{filename}' 文件。")
    except IOError as e:
        logging.error(f"文件写入错误: {e}")

def main():
    """
    主函数，执行数据库查询并将结果保存为 JSON 文件。
    """
    database = 'PhoneFactor'  # 确保数据库文件名正确，建议添加扩展名
    if not os.path.isfile(database):
        logging.error(f"数据库文件不存在: {database}")
        return
    
    accounts = fetch_accounts(database)
    
    if accounts:
        # 生成带有时间戳的输出文件名，避免覆盖旧文件
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output_{date_str}.json"
        save_json_to_file(accounts, output_file)
    else:
        logging.info("未找到符合条件的账户数据。")

if __name__ == "__main__":
    main()
