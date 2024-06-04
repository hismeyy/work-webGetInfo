import os
import winreg as reg


def set_auto_start(enable):
    # 设置注册表项的路径
    registry_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    # 程序名称（随便你想要的名称）
    program_name = "getInfo"
    # 程序路径（替换为你的程序路径）
    program_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "\\main.exe"
    print(program_path)

    try:
        # 打开注册表项
        with reg.OpenKey(reg.HKEY_CURRENT_USER, registry_key, 0, reg.KEY_SET_VALUE) as key:
            if enable == "True":
                # 设置自动启动
                reg.SetValueEx(key, program_name, 0, reg.REG_SZ, program_path)
                print(f"{program_name} 已设置为开机自动启动。")
            else:
                # 取消自动启动
                reg.DeleteValue(key, program_name)
                print(f"{program_name} 的开机自动启动已取消。")
    except FileNotFoundError:
        # 捕捉键不存在的错误
        if not enable:
            print(f"{program_name} 未设置为开机自动启动。")
        else:
            print(f"错误: 无法设置 {program_name} 为开机自动启动。")
    except PermissionError:
        print("错误: 权限被拒绝。请以管理员身份运行此脚本。")
