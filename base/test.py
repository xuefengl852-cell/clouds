import argparse
import os
import time


def simulate_volume_presses(count=500, interval=0.5, volume_up=True):
    """
    模拟按下音量键
    :param count: 按下次数
    :param interval: 按键间隔（秒）
    :param volume_up: True为音量上键，False为音量下键
    """
    keycode = "KEYCODE_VOLUME_UP" if volume_up else "KEYCODE_VOLUME_DOWN"
    direction = "上" if volume_up else "下"
    
    print(f"模拟按下音量{direction}键 {count} 次...")
    
    for i in range(1, count + 1):
        print(f"按下音量{direction}键 ({i}/{count})")
        os.system(f"adb shell input keyevent {keycode}")
        time.sleep(interval)
    
    print("模拟完成！")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='模拟按下音量键')
    parser.add_argument('-c', '--count', type=int, default=500, help='按下次数')
    parser.add_argument('-i', '--interval', type=float, default=1.0, help='按键间隔（秒）')
    
    # 修改为选择参数
    parser.add_argument('-d', '--direction', choices=['up', 'down'], default='down',
                        help='音量键方向: up(上键) 或 down(下键)')
    
    args = parser.parse_args()
    
    # 根据参数值确定方向
    volume_up = (args.direction == 'up')
    
    simulate_volume_presses(
        count=args.count,
        interval=args.interval,
        volume_up=volume_up
    )
