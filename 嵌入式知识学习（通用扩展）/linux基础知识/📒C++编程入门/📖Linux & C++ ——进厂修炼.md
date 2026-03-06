# Linux

## Day 1

```bash
1 df -h 查看磁盘分区
bash1
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/068409e601cbffa2cc429610af1b7c33\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/068409e601cbffa2cc429610af1b7c33_MD5.png)

```bash
2 free -k/m/G  查看内存的使用情况
bash1
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/d2830356b1b4a9fb5ce4b5a360064afe\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/d2830356b1b4a9fb5ce4b5a360064afe_MD5.png)

```bash
3 head -n 查看一个文件的前n行，不指定n，n的默认为10
bash1
```
```bash
4 tail -n 查看一个文件的末n行
-F 查看一个文档的动态变化，修改文档的时候显示(例如火车站时间版）
bash12
```
```bash
5 less 查看文件，以较少的内容进行输出

less +数字   从第n行开始查看
less 空格   翻页
less +↑/↓  上下翻页 
bash12345
```
```bash
6 wc 统计文件内容信息
-l 以行的形式
-w 统计单词，空格区分
-c 统计字节
bash1234
```
```bash
7 date 操作时间、日期
bash1
```
```bash
（1）date
bash1
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/8369520256b31f7a93744ce5166aff5d\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/8369520256b31f7a93744ce5166aff5d_MD5.png)

```bash
（2）date +%F  或者 date "+%Y-%m-%d"
bash1
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/ccbd54ea7c535273eacb6702b2c87e2c\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/ccbd54ea7c535273eacb6702b2c87e2c_MD5.png)

```bash
（3） date "+%F %T"   或者 date "+%Y-%m-%d %H:%M:%S
bash1
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/9baeb521644de1f60b64b3eeeb073b2d\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/9baeb521644de1f60b64b3eeeb073b2d_MD5.png)

```bash
（4） 获取之前或者之后的某个时间(备份需要）
date -d "-1/+1 day" "%F %T"
bash12
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/a8152a32777662893fc6578968a382b7\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/a8152a32777662893fc6578968a382b7_MD5.png)

```bash
8 cal 操作日历 
cal  -1 当前日历
cal -3 上月+本月+下月日历
cal -y 年份 某一年日历
bash1234
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/8df4c7a2d422d27d89ca4de447210d70\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/8df4c7a2d422d27d89ca4de447210d70_MD5.png)

```bash
9 clear  或者  快捷键ctrl+l    清除页面
bash1
```
```bash
10 管道
管道符 |  作用：过滤、特殊、扩展处理      注意：不可单独使用
bash12
```
```bash
（1） 过滤、查询根目录下包含“y"字母的文档
ls / | grep y      
可以理解为：ls / 有一个输出
| 分界线
grep 过滤
y 有一个输入
bash123456
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/9db60ae1b657d02d4ed07c8cf78d7459\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/9db60ae1b657d02d4ed07c8cf78d7459_MD5.png)

```bash
（2）特殊：通过管道实现less等价效果
cat 文件名 | less = less 文件名       有点鸡肋
bash12
```

## Day 2

```bash
1 hostname 操作主机名
hostname -f 输出当前主机的FQDN，即域名
bash12
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/e2f830b2a77d6514d40ea7be6a1170af\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/e2f830b2a77d6514d40ea7be6a1170af_MD5.png)

```bash
2 id 指令  查看一个用户基本信息
id  默认当前id
id 用户名 指定用户基本信息
bash123
```
```bash
3 whoami 当前登录用户名
bash1
```
```bash
4 ps -ef 用于查看服务器进程
bash1
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/d87323dab22ae3edc53af7fb56d2faa2\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/d87323dab22ae3edc53af7fb56d2faa2_MD5.png)

```bash
ps中结果过滤出想要查看进程状态
ps -ef | grep 进程名称   结果至少包含2个进程
bash12
```
```bash
5 top 查看服务器进程占用的资源
快捷键： top运行的状态中
M：按照内存从高到底排序
P：按照CPU从高到底排序
bash1234
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/fec4127eaa06e41f04650ce3295a7c2f\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/fec4127eaa06e41f04650ce3295a7c2f_MD5.png)

## Day 3

```bash
1 du -sh 路径 查看目录真实大小
bash1
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/a07ee7ec65aceaf9130e62495128f584\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/a07ee7ec65aceaf9130e62495128f584_MD5.png)

```bash
2 find 查找   注意：隐藏的文件也可以找到
find 路径范围 -name 名称查找  选项的值
            -type 类型文档  f文件/d文件夹
bash123
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/e6552e6ecedfabf295420ac8139170b7\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/e6552e6ecedfabf295420ac8139170b7_MD5.png)

```bash
3 service 服务名    start/stop/restart
eg1:启动本机安装的Apache，服务名：httpd
service httpd start
bash123
```

## Day 4

```bash
1 kill 杀死进程
    kill PID 
    killall 进程名称
bash123
```
```bash
2 ifconfig  网卡信息
bash1
```
```bash
3 reboot 重启
    reboot -w  模拟重启，不操作（一般测试使用）
bash12
```
```bash
4 shutdown 关机
    shutdown -h now "关机提示"   立即关机
    shutdown -h  时间  "关机提示"  指定时间关机   ctrl + c 取消  或者  shutdown -c
其他关机命令：
    init 0
    halt
    poweroff
bash1234567
```
```bash
5 uptime  计算机在线持续时间（开机到现在）
bash1
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/15164d4eadf9e4e9c5c443ca9d423c39\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/15164d4eadf9e4e9c5c443ca9d423c39_MD5.png)

```bash
6 uname 获取系统相关信息
    uname
    uname -a  
    类型   主机名  内核版本  发布时间  开源计划
bash1234
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/ad7d07856d62dabe4524c6e3ef9c4135\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/ad7d07856d62dabe4524c6e3ef9c4135_MD5.png)

```bash
7 netstat -tnlp 查看网络连接状态
            -t 查看tcp协议连接
            -n 将地址字母转换成ip地址，协议变成端口号
            -l 只显示"stat"状态为LISTEN监听连接
            -p 显示发起连接进程pid和进程名称
bash12345
```
```bash
8 man linux全部命令手册
man 查询命令
bash12
```

## Day 5

```bash
在这里插入代码片
bash1
```
```bash
1 vim 编译器
bash1
```
```bash
（1） 三种模式

 1. 命令模式：不能对文件直接编译，快捷键操作（粘贴、删除、移动光标）
 2. 编辑模式：可以对文件进行编译
 3. 末行操作：对末行输入命令对文件操作（搜索、替换、保存、退出、撤销、高亮）

bash123456
```
```bash
（2）打开文件的方式

 1. vim 文件路径
 2. vim +数字 文件路径  打开指定文件，光标移动到指定行
 3. vim /关键词 文件路径  （高亮关键词）
 4. vim 路径1 路径2 （同时打开多个文件）

bash1234567
```
```bash
（3）光标移动

 1. 行首 shift + 6    行尾：shift + 4 
 2. 首行 gg            尾行：G
 3. 上移动 n : n+↑
 4. 下移动 n : n+↓
 5. 左移动 n : n+←
 6. 右移动 n : n+→
 7. 向上翻屏： ctrl + b         向下翻屏：ctrl + f
 8. 复制光标所在行：    yy      粘贴 ：    p
 9. 以光标所在行，向下复制 n 行：数字+yy
 10.剪切/删除所在行    ：     dd
 11. 以光标所在行，向下剪切 n 行：数字+dd
 12. 撤销    ： u    undo    快捷键： ctrl r
bash1234567891011121314
```

## Day 6

```bash
1 模式之间切换
bash1
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/8b2aeb32f8c41509e1a9da7a2a1e3a6e\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/8b2aeb32f8c41509e1a9da7a2a1e3a6e_MD5.png)

```bash
1. w 保存
 2.  w 路径  另存
 3. 查找： /关键词
 4. 查找关键词上下移动： n/N
 5. 取消高亮：nohl
 6. 替换
     :s/搜索关键词/新内容    光标所在行的第一处替换
     :s/搜索关键词/新内容/g    光标所在行的全部
     :%s/搜索关键词/新内容    替换整个文档的每一行第一处
     :%s/搜索关键词/新内容/g 替换整个文档
 7. 显示行号： set nu    取消：set nonu
bash123456789101112
```
```c
2 vim 打开多个文件
默认第一个界面在第一个文件夹，查看打开的文件：files(末行输入）
%a 正在打开的文件
# 上一个文件

(1) 切换文件： open  文件
(2) bn:下一个文件        bp:上一个文件
c1234567
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/883881aceafe95b0678e50161568a08e\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/883881aceafe95b0678e50161568a08e_MD5.png)

```c
3 vim 配置
末行位置配置：    临时的
个人配置文件： ~/.vimc    没有可自行创建    若是与全局配置冲突，则个人配置==为主== 
全局配置文件：/etc/vimc
c1234
```
```c
4 异常退出
编译文件时，没有正常wq退出，遇到关闭终端或者断电。
下次vim进入的时候，会有一个交换文件的提示
解决：
ls -a  把文件显示(包含隐藏文件）
- 会发现.pawsswd.swp 这个文件
rm -f .pawsswd.swp   移除即可
c1234567
```
```c
5 别名机制：创建属于自己自定义的命令别名
依靠在一个别名映射文件：~/.bashrc

重启 或者    source ~/.bashrc
c1234
```

# C++

## 1 区别struct class

```c
struct 默认权限：public
class 默认权限： private
```

## 2 setName()/getName()

```c
setName() getName()  对某些属性进行 可读可写/只读/只写 控制
c1
```

## 3 拷贝函数的调用过程

```c
Person(const Person &p){
}
 1. 使用一个已经创建完毕的对象初始化新对象
 2. 值传递的方式给函数返回参数值
 3. 以值方式返回局部对象
Person p
Person p1(p)
```

## 4 构造函数调用规则

创建一个类，每个类至少添加3个函数

1. 默认构造 ：若是有参构成已有，则不提供默认构造
2. 析构函数
3. 拷贝构造 ：若提供拷贝构造。不提供有参、无参

## 5 深拷贝、浅拷贝（💌）

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖Linux & C++ ——进厂修炼/d11e3be97f81564869d9f1e62f9c8015\_MD5.jpg](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖Linux%20&%20C++%20——进厂修炼/d11e3be97f81564869d9f1e62f9c8015_MD5.jpg)

## 6 类对象作为类成员

当其他类对象作为本 [类成员](https://so.csdn.net/so/search?q=%E7%B1%BB%E6%88%90%E5%91%98&spm=1001.2101.3001.7020) ，构造时先构造类对象，再构造自身。析构的顺序相反。

## 7 静态成员

特点：

- 共享一份数据
- 编译阶段分配内存
- 类内声明。类外初始化
```c
static int m_age;
int Person::m_age=10;
c12
```

[静态成员函数](https://so.csdn.net/so/search?q=%E9%9D%99%E6%80%81%E6%88%90%E5%91%98%E5%87%BD%E6%95%B0&spm=1001.2101.3001.7020) ：  
特点：

- 共享一个函数
- 只有静态成员变量可以访问静态成员函数

**都有访问权限**

## 8 成员变量和成员函数是分开存储的

```c
创建1个空对象（1个类）占用空间：    1  区分空对象占用内存的位置

 1. 非静态成员变量    属于类对象    4
 2. 静态成员变量        不属于类对象    1
 3. 非静态成员函数    不属于类对象    1
 4. 静态成员函数        不属于类对象    1
```

## 9 this指针（💌）

> 在 C++ 中，对于一个类的 非静态成员函数，编译器会隐式传递一个指向该成员函数所属于对象的指针。这个指针就是 this。 
> 
> 它的类型在成员函数中一般是 ClassName* const（或在 const 成员函数中是 const ClassName* const）——即指向该对象的指针，且不能被重新赋值。 
> 教程要点
> 
> 使**用 this->member 或 (* this).member 是访问当前对象成员的方式**。其实在成员函数内部，你一般可以直接写 member 而不写 this->，因为编译器会隐式理解。但**当有名称冲突（例如成员变量和形参重名）时，使用 this-> 来区分成员变量是推荐做法。** 
> 
> **静态成员函数是属于类而非对象，因此没有 this 指针。** 


### （1）解决名称冲突（类属性与形参一致问题）

- 1 这里，`this->age` 指的是当前对象的成员变量 `age`，而右侧的 `age` 是形参。这样就解决了名称冲突。
```c
class Person {
public:
    int age;
    void setAge(int age) {
        this->age = age;  // 使用 this-> 来区分成员变量 age 与形参 age
    }
};

```

### （2）返回对象本体，用引用的方式
```c
# 用引用方式返回
Person & PersonAdd(Person &p)
{
    return *this
}
# 以值的形式返回
Person PersonAdd(Person &p)
{
    return *this
}
```

> 如果用 引用方式返回` *this` （即 Person & PersonAdd(...) { `return *this; `}），那么你返回的是当前对象自身的引用。**外部通过这个引用可以直接操作这个对象。**
> 
> 如果用 值方式返回 `*this` （即 Person PersonAdd(...) {` return *this; `}），那么你**返回的是当前对象的一个拷贝（因为值返回会触发拷贝构造或移动构造）。所以外部得到的是一个新的对象，与原对象分离。**







## 10 空指针访问成员函数

若是成员函数中有属性，默认为：this->m\_age,但是this 被调用的不能为 ==空==

```c
解决：
在成员函数中加：
if(this==NULL)
{
    return ;
}
```

## const 修饰成员函数

```c
void show() const  常函数
const Person p    常对象
c12
```

this 的本质：指针常量，指针指向不能修改

```c
Perosn * const this;
c1
```

在成员函数加 const ，这样指针指向的值也不能修改

```c
const Person * const this
c1
```

若是常函数内想访问属性：  
在属性前加： ==mutable==

**常对象可以访问常函数，不可以访问普通函数**

```c
public:
    int m_A;
    mutable int m_B; //可修改 可变的

const Person person; //常量对象  
cout << person.m_A << endl;
//person.mA = 100; //常对象不能修改成员变量的值,但是可以访问
person.m_B = 100; //但是常对象可以修改mutable修饰成员变量
//常对象访问成员函数
person.MyFunc(); //常对象不能调用const的函数
c1234567891011
```
