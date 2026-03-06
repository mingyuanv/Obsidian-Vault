# Day 1

## 运行模式

```c
运行级别：
 0：表示关机级别（默认不设置）
 1：单用户模式
 2：多用户模式，不带NFS
 3：完全的多用户模式（命令行界面，不带桌面）                                              
 4：被保留模式
 5：完整的图形界面模式（默认）
 6：表示重启（默认不设置） 
c12345678
```

**注意： ==init== 指令需要超级管理员权限，普通用户无法执行**

```c
临时操作：
init 0 关机
init 3 命令行界面
init 5 图形界面
init 6 重启
c12345
```
```c
查看当前运行级别：
systemctl get-default
级别3：multi-user.target
级别5：graphical.target 
c1234
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/d85a5c36d90e03bdaba6c2a5708fb132\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/d85a5c36d90e03bdaba6c2a5708fb132_MD5.png)

# Day 2

## 用户与用户组管理

```c
1. /etc/passwd     存储用户的关键信息    查看用户主组
 2. /etc/group        存储用户组关键信息    查看用户的附加组
 3. /etc/shadow        存储用户密码
c123
```

### 用户管理

（1）添加用户

```c
useradd + - g     可以是id,也可以是组名，指定用户的用户组                       +               用户名
         - G    指定用户的用户组附加组                                            
         - u    用户的id(用户标识符)系统默认从500之后顺序分配Uid，不系统分配，使用此项自定义
         - c    添加注释
c1234
```

**eg:创建一个用户：useradd zs**

```c
[root@localhost wcjax]# useradd -u 504 zhangs
c1
```

验证是否创建成功：

1. 查看/etc/passwd的最后一行
2. 是否存在家目录（创建完之后会产生一个同名的家目录）

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/e556c5638b67aee584e235c5bbef7a08\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/e556c5638b67aee584e235c5bbef7a08_MD5.png)

- zhangs：用户名称
- x：密码，表示密码占位
- 504：用户ID，用户的标识符
- 1002： 用户组ID，用户所属的主组ID
- /home/zhangs: 家目录，用户登录进入系统默认位置
- /bin/bash：解释器shell

（2）修改用户

```c
usermod +选项 用户名
        - g :主组
        - G    :附加组
        - u    :UID 
        - l    :修改用户名
c12345
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/e057a87b498c43409d004b122ae12fdc\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/e057a87b498c43409d004b122ae12fdc_MD5.png)  
**eg:修改用户组ID 附加组id**

```c
usermod -g 1000 -G 10001
c1
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/97e948cb2ee5bdb7f479b1616063bea3\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/97e948cb2ee5bdb7f479b1616063bea3_MD5.png)

**eg:修改用户名称**

```c
usermod -l (新）zhs (旧)zhangs
c1
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/33f02895c689441ff6d76a4bbf89bd84\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/33f02895c689441ff6d76a4bbf89bd84_MD5.png)  
（3）设置密码：

```c
passwd zhs  输入密码            非root用户也可以执行
c1
```

（4）删除用户

```c
userder 用户名
-r :表示删除用户的同时，删除其家目录
c12
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/93b29133106b540637dc21d5e4df88eb\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/93b29133106b540637dc21d5e4df88eb_MD5.png)  
**注意：若是已经登录的用户删除会删除失败，需要 ==kill+进程ID== ，杀死对应的进程**

# Day 3

## 用户组管理

每个用户都有一个用户组， Linux 下的用户属于与它同名的用户组。

### 用户组添加

```c
groupadd -g 用户组名
-g 设置自定义的用户组ID，不设置默认500之后默认顺序分配
c12
```

### 用户组编辑

```c
groupmod -g  用户组名
         -n  新名 旧名
c12
```

### 用户组删除

若删除的是一个组，但是该组是用户的主组，删除时删除不了，只有把组内所有的用户移除(==修改用户的组ID）== ，才能删除该组

```c
groupdel 用户组名
c1
```

# Day 4

## 网络设置

文件的位置：

```c
/etc/sysconfig/network-scripts
c1
```

重启网卡

```c
/etc/init.d/network restart
c1
```
```c
创建一个快捷方式（也即是==软链接==）方便找更深层次的文件
ln -s  某文件的路径  快捷方式路径
c12
```
```c
停止网卡： ifdown 网卡名
开启网卡： ifup 网卡名
c12
```

设置主机名

```c
hostname 主机名  临时的
修改主机名的配置文件：/etc/hostname    永久设置
c12
```

## chkconfig 提供开机启动项管理服务

chkconfig命令主要用来更新（启动或停止）和查询系统服务的运行级信息。  
![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/9c1ee090b21db1c25d357c242cdb32d1\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/9c1ee090b21db1c25d357c242cdb32d1_MD5.png)

```c
显示所有运行级系统服务的运行状态信息（on或off）。如果指定了name，那么只显示指定的服务在不同运行级的状态。
chkconfig --list 
c12
```
```c
除所指定的系统服务，不再由chkconfig指令管理，并同时在系统启动的叙述文件内删除相关数据。
删：chkconfig --del 服务名
c12
```
```c
chkconfig确保每个运行级有一项启动(S)或者杀死(K)入口。如有缺少，则会从缺省的init脚本自动建立。
添加：chkconfig --add 服务名
c12
```
```c
设置某服务在某级别下启动或者不启动
chkconfig --level  级别数字(多个连在一起） 服务名 on/off

 1. 等级0表示：表示关机
 2. 等级1表示：单用户模式
 3. 等级2表示：无网络连接的多用户命令行模式
 4. 等级3表示：有网络连接的多用户命令行模式
 5. 等级4表示：不可用
 6. 等级5表示：带图形界面的多用户模式
 7. 等级6表示：重新启动
```

## ntp 服务 时间同步管理操作

```c
一次性同步时间
ntpdate 时间服务器域名或者ip
c12
```
```c
设置同步服务器
服务名：ntpd
启动：service ntpd statt
c123
```

# Day 5

## 防火墙服务

防范一些网络攻击，有软硬防火墙，有选择的让某些请求通过。

### 版本7：

```c
查看状态：
firewall-cmd --state
c12
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/fb65df82b5527dbb2ff61e12f75601bb\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/fb65df82b5527dbb2ff61e12f75601bb_MD5.png)

```c
查看防火墙的具体配置信息,会显示出当前防火墙的所有配置信息，包括已启用的服务、端口、协议等，通过分析这些信息，你可以了解到防火墙的实际配置情况，从而判断是否需要进行调整。
firewall-cmd --list-all
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/a48f82148286692b74bb615466ffd1bb\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/a48f82148286692b74bb615466ffd1bb_MD5.png)

```c
启动：
systemctl     start         firewall
            restart
            stop
```
```c
设置开机启动或者开机禁用
systemctl        enable            firewalled
                disable
c123
```

### 版本6

```c
启动/关闭防火墙 ：
service IP tables  start/stop
c12
```
```c
设置开机启动/禁用
chkconfig iptables on/off
c12
```

## rpm

类似于软件管家，对 [Linux服务器](https://so.csdn.net/so/search?q=Linux%E6%9C%8D%E5%8A%A1%E5%99%A8&spm=1001.2101.3001.7020) 上的软件包进行对应管理操作：查询 / 卸载/ 安装  
（1）查询：查询某软件的安装情况

```c
rpm -qa | grep 关键词
c1
```

（2）卸载

```c
rpm -e 软件名
c1
```

有些软件卸载会有依赖 关系，无法卸载

```c
rpm -e 软件名 --nodeps
c1
```

（3）安装

```c
rpm -ivh 软件包完整名称
    -i install 安装
    -v 显示安装进度
    -h 以#显示进度条
c1234
```

## 挂载

将外部设备或者远程系统文件添加到 现有的 文件系统 树中，使外部存储设备或者远程系统的文件系统能够被系统访问到 。

```c
查看快装信息：
Name ： 名称
Size : 大小
Type : 类型
MountPoint : 挂载点
c12345
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/75b1ffaae0b084661883dce3a2bee7bd\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/75b1ffaae0b084661883dce3a2bee7bd_MD5.png)  
光盘的挂载与解挂：  
解挂：

```c
umount 路径            相当于window弹出U盘
c1
```

挂载：

```c
mount 设备原始地址    路径
设备原始地址： /dev :    根据大小确定具体的 name值，拼凑在一起组成原始地址  ：
/dev/sr0

挂载地址放在：    /dev/mnt
c12345
```

## cron计划任务

操作系统不可能24小时有人值班 ，又是想要指定时间点执行任务

```c
crontab -l :列出指定用户的计划任务列表
        -e :编辑指定用户计划列表
        -u :指定用户，不指定当前用户
        -r ：删除指定用户的计划任务列表
c1234
```

（1）编辑计划列表

```c
以行为单位，一行一个计划
格式：
分 时 日 月 周 需要执行的指令

 - 分：0~59
 - 时：0~23
 - 日：1~31
 - 月：1~12
 - 周：0~7 0，7都表示周日
 - *：表示取值范围的每一个数字
 - -：区间表达式
 - /：表示每多少个  
     每2天1次：*/2
     每10分钟1次： */10
 - ，：多取值：1点，6点，9点执行  ： 1，6，9

c12345678910111213141516
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/87ef5eba1c473eaea54634730ba322af\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux服务及用户设置——进厂修炼/87ef5eba1c473eaea54634730ba322af_MD5.png)  
权限问题:  
超级管理员通过配置某些用户不允许设置计划任务

```c
配置文件： /etc/cron.deny
里面写用户名即可
c12
```

# Day 6

## 权限

```c
身份类别的权限：
    ower:所有者
    group: 用户组
    other: 其他人
    root ：超级管理员
操作权限：：
    read 
    write
    execate
c123456789
```

查看文件权限

```c
ls -l 路径  =  ll

d rwx  r-x  ---  

 1. d:文件夹  还有：-：文件 / l: 软链接 / s:套接字
 2. rwx:文件所有者所有权限都有
 3. r-x:用户组权限可读可执行
 4. 其他权限：无权限
c12345678
```

## 权限设置

```c
chmod -R(文件：递归设置权限） 权限模式 文件
c1
```

（1）字母形式

```c
给谁设置：
 1. u：所有者身份：ower
 2. g:所有者同组用户设置
 3. o:其他用户设置
 4. a:所有用户设置权限（默认不指定）（root用户设置）
c12345
```
```c
权限字符：

 1. r:读
 2. w:写
 3. x:执行

c123456
```
```c
权限分配：

 1. +： 增加
 2. -： 删除
 3. = ：将权限设置具体值
c12345
```

eg:给一个文件(-rw-------)设置权限，所有者所有权限，同组用户读和执行，其他用户读

```c
chmod u+x ,g+rx,o+r 文件
chmod u=rwx,g=rx,o=r 文件
c12
```

（2）数字形式

```c
1. 读:r->4
 2. 写:w->2
 3. 执行：x->1
 4. 无权限：-->0

c123456
```

**注意：在Linux中，如果其他用户要删除一个文件，不是看文件有没有对应的权限，而是看 ==文件所在的目录== 是否有权限。**

## 属主与属组设置

（1）更改文档的所属用户

```c
chown -R username 文件路径
c1
```

eg: ==root== 创建oo目录，修改为 ==aiy== 用户

```c
chown -R test /oo
c1
```

（2）更改文档的所属用户组

```c
chgrp -R groupname 文档路径
c1
```

（3）将上述两则 合并

```c
chown -R username:groupname 文档路径
c1
```

