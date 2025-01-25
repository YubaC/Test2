import os


class UserService:

    def __init__(self):
        self.users = {"admin": "password123"}  # 硬编码的凭据，存在安全问题

    def get_user(self, username: str) -> str:
        """
        通过用户名获取用户的密码 - 存在信息泄露风险
        """
        return self.users.get(username, "User not found")

    def dangerous_command(self, command: str) -> str:
        """
        执行危险的系统命令 - 存在命令注入漏洞
        """
        # 直接执行用户输入的命令，没有进行任何验证
        return os.popen(command).read()


def main():
    service = UserService()

    # 获取用户信息，存在信息泄露风险
    print(service.get_user("admin"))

    # 执行危险命令
    print(service.dangerous_command("echo Hello, World!"))

    # 演示命令注入漏洞
    print(service.dangerous_command("ls; cat /etc/passwd"))


if __name__ == "__main__":
    main()
