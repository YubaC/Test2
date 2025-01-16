import logging

# DEBUG = os.environ.get('DEBUG', 'False') == 'True'
DEBUG = False

# 配置日志
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)


def main():
    logging.debug("程序开始运行。")
    result = 2 + 2
    logging.debug(f"计算结果: {result}")
    if result == 4:
        logging.debug("结果正确。")
    else:
        logging.debug("结果有误！")
    logging.debug("程序结束。")


if __name__ == "__main__":
    main()
