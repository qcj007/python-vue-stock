#!/usr/bin/env python
"""Django的命令行工具，用于执行管理任务。"""

import os
import sys


def main():
    """
    执行管理任务。

    设置环境变量' DJANGO_SETTINGS_MODULE'为'stockMain.settings'，
    然后从命令行执行Django的管理命令。
    """
    # 设置Django的环境变量
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockMain.settings')
    try:
        # 尝试从django.core.management导入execute_from_command_line函数
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # 如果导入失败，抛出错误信息
        raise ImportError(
            "无法导入Django。您确定它已安装并在您的PYTHONPATH环境变量中可用吗？"
            "您忘记激活虚拟环境了吗？"
        ) from exc
    # 执行从命令行传入的命令
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # 如果脚本被直接运行，则调用main函数
    main()



# 打包
#1、pyi-makespec -D manage.py
#2、pyinstaller manage.spec
#3、进入dist/manage 目录输入manage.exe runserver