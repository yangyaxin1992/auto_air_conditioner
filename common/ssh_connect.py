# ！/usr/bin/env python
# -*- coding:utf8 -*-
# author:yangyaxin time::14:17
import datetime
import time
from subprocess import Popen,PIPE
import os
import paramiko
from scp import SCPClient


class SshConnect:
    """
    ping设备ip,ssh连接设备，重启设备，获取指定的日志
    """
    def ping_ip(self,host):
        # 判断设备ip是否可以ping通
        # nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.p = Popen(
            args = "ping "+ host,
            stdin = None,
            stdout = PIPE,
            stderr = PIPE,
            cwd = os.getcwd(),
            shell = True
            )
        self.outinfo, self.errinfo = self.p.communicate()
        time.sleep(5)
        out = self.outinfo.decode('gbk')
        print("输出：",out)
        return out

    def juage_ping_ip(self,host):
        # 判断是否ping通，循环count次
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        count = 5
        i = 0
        while i < count :
            out = self.ping_ip(host)
            if "无法访问目标主机" in out :
                print(nowTime,host,"ping fail")
                print("*" * 88)
                i += 1
                continue
                # return self.ping_ip(host)
            elif "无法访问目标主机" not in out and "丢失 = 0 (0% 丢失)" not in out :
                print(nowTime, host, "丢包率大于0%，重试")
                print("*" * 88)
                i += 1
                continue

            else :
                print(nowTime,host,"ping success")
                print("*"*88)
                break
        return i


        # print("错误：",self.errinfo.decode('gbk'))
        # return out

    def connect_server(self,ip,pid,username,password):
        # ssh连接设备
        # self.transport = paramiko.Transport(("192.168.18.177", 22))
        flag = 0
        try :
            self.transport = paramiko.Transport((ip, pid))
            self.transport.connect(username=username, password=password)
            flag += 1
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.ssh._transport = self.transport
            # 创建scp对象，上传、下载文件
            self.scp = SCPClient(self.ssh.get_transport(), socket_timeout=30.0)
            print("*" * 66 + "ssh连接成功" + "*" * 66)
            # self.transport.connect(username="root", password="rockchip")
        except (Exception, paramiko.ssh_exception.SSHException) as e:
            print("由于目标计算机积极拒绝，无法连接，可能处于离线")
            flag += 0
            time.sleep(2)
        return flag



    def send_cmd(self,cmd):
        #发送命令，返回输出结果
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        # self.stdin.write(
        #     '''cd /zihome/plugins/zgateway/
        #      ls''')
        # self.channel.send("cd /zihome/plugins/zgateway/"+"\n")
        result = stdout.read().decode("utf8","ignore")
        print(result)
        time.sleep(1)
        return result

    def get_log(self,cmd,mac):
        # 获取最新log，copy到本地
        print("*" * 88)
        # 获取最新log文件名称
        # 依次循环遍历文件夹的文件，依次拷贝到本地目录下
        current_date = datetime.datetime.now().strftime('%m-%d')
        print(current_date)
        # local_path = r'D:\Work(勿删）\04 _自动化项目\auto_testplat\z_touch\log\ztouch_log'
        local_path = os.getcwd()
        # 多层文件夹，需一层层获取
        module_log = ['zdaemon','zgui','zigbee','zpanel','zvoice','zwifi']
        # module_log = ['zpanel']
        for file_log in module_log :
            # stdin, stdout, stderr = self.ssh.exec_command(f'find /userdata/zihome/log/{file_log}')
            # 判断module_log列表是否为空，非空，则path需增加，空，则直接cmd path
            if len(module_log) != 0 :
                new_cmd = os.path.join(cmd,file_log)
            else :
                new_cmd = cmd
            stdin, stdout, stderr = self.ssh.exec_command(new_cmd)
            # stdin, stdout, stderr = self.ssh.exec_command(f'cd /userdata/zihome/log/{file_log}/ && ls -l')
            result = stdout.read().decode("utf8", "ignore")
            print(f'{file_log}的日志：',result)
            # 遍历远端服务器上的所有文件夹，若在本地服务器不存在，则scp过来
            files = result.split('\n')[1:-1]
            print("files:",files)
            # 本地保存log路径
            new_local_path = os.path.join(local_path ,"..","log","new_log",mac ,current_date,file_log)
            print(new_local_path)
            # remove_path = f'/userdata/zihome/log/{log_name}'
            for file in files :
                # self.scp.get(f'{file}', local_path)
                if os.path.exists(new_local_path):
                    print('sub dir %s  already exists. update it' % file_log)
                    self.scp.get(f'{file}', new_local_path)
                else:
                    print('start to copy %s...' % file_log)
                    os.makedirs(new_local_path)
                    self.scp.get(f'{file}', new_local_path)
        # time.sleep(1)
        # self.scp.close()
        # time.sleep(1)
        # self.ssh.close()
        return current_date

    def closed_ssh(self):
        # 关闭ssh、scp
        time.sleep(1)
        self.scp.close()
        time.sleep(1)
        self.ssh.close()

# print(os.path.abspath(os.path.join(os.getcwd(), "../config/")))
if __name__ == '__main__':
    pass
    # ztouch = ZTouch()
    # ztouch.ping_ip(host="192.168.18.177")
    # time.sleep(2)
    # ztouch.connect_server("192.168.18.177",22,"root","rockchip")
    # time.sleep(2)
    # ztouch.reboot_ztouch("reboot")
    # cmd = "cd /zihome/plugins/zgateway/ && ./run.sh start"
    # zgateway.root_gateway(cmd)
    # time.sleep(10)


