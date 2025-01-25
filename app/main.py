import mysql.connector
import subprocess
import logging
from typing import Any, Dict, Optional

class UserService:
    def __init__(self, db_connection: mysql.connector.MySQLConnection):
        self.db = db_connection
        self.cursor = db_connection.cursor()

    def get_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        获取用户数据的方法 - 存在 SQL 注入漏洞
        """
        try:
            # 危险: 直接字符串拼接构建 SQL 查询
            query = f"SELECT * FROM users WHERE id = '{user_id}'"

            # 执行不安全的查询
            self.cursor.execute(query)
            result = self.cursor.fetchone()

            if result:
                return {
                    "id": result[0],
                    "username": result[1],
                    "email": result[2]
                }
            return None

        except Exception as e:
            # 危险: 直接暴露错误详情
            logging.error(f"Database error: {str(e)}")
            raise

    def execute_command(self, command: str) -> str:
        """
        执行系统命令的方法 - 存在命令注入漏洞
        """
        try:
            # 危险: 直接执行用户提供的命令
            result = subprocess.check_output(
                command,
                shell=True,  # 特别危险: 启用 shell=True
                text=True
            )
            return result
        except subprocess.SubprocessError as e:
            logging.error(f"Command execution failed: {str(e)}")
            raise

    def save_user_data(self, user_data: dict) -> None:
        """
        保存用户数据的方法 - 存在路径穿越漏洞
        """
        try:
            # 危险: 不安全的文件操作
            filename = f"user_data_{user_data['username']}.txt"

            # 危险: 没有验证文件路径，可能导致路径穿越
            with open(filename, 'w') as f:
                f.write(str(user_data))

        except IOError as e:
            logging.error(f"File operation failed: {str(e)}")
            raise

def main():
    # 示例数据库连接（实际使用时需要替换为真实的连接信息）
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "password",  # 危险: 硬编码的凭据
        "database": "test_db"
    }

    try:
        # 创建数据库连接
        connection = mysql.connector.connect(**db_config)
        user_service = UserService(connection)

        # 演示 SQL 注入漏洞
        result = user_service.get_user_data("1' OR '1'='1")
        print(f"SQL Injection Result: {result}")

        # 演示命令注入漏洞
        output = user_service.execute_command("ls -la; cat /etc/passwd")
        print(f"Command Injection Result: {output}")

        # 演示路径穿越漏洞
        malicious_data = {
            "username": "../../../etc/passwd",
            "data": "malicious content"
        }
        user_service.save_user_data(malicious_data)

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    main()
