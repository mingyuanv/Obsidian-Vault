---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：




# 一、shell基础知识

## shell的解析器（ sh ash bash）
### 1 、查看⾃⼰ linux 系统的默认解析器（echo $SHELL）
- 1 #!/bin/bash

### 2 、编写shell脚本（记得赋于文件可执行权限）
[[嵌入式知识学习（通用扩展）/linux基础知识/assets/🔨shell语言学习/file-20250810171436460.png|Open: Pasted image 20250710141623.png]]
![嵌入式知识学习（通用扩展）（未）/边开发边积累/assets/shell语言学习/file-20250810171436460.png](assets/🔨shell语言学习/file-20250810171436460.png)

### 3 、


### 4 、




## shell环境变量设置文件
### 1 、/etc/profile
- 1 开机⾃启动的程序，公共环境变量在这⾥设置

### 2 、~/.bashrc
- 1 登录时会⾃动调⽤，打开任意终端时也会⾃动调⽤
- 2 与个⼈⽤⼾有关的环境变量


### 3 、



# 二、shell的特殊功能符

## 赋值变量（等号两边不能有空格）

### 1 、=（廷迟赋值）
- 1 赋值脚本⾥⾯最后被指定的值
```bash
variable=11
variable=22
echo $variable

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
22
```

### 2、+=（追加赋值，中间无空格）
```bash
variable=11
variable+=22
echo $variable

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh

```


## 在`${ }`内才可以赋值的变量

### 1、:=（未设置，则默认）
- 1 如果变量未设置或为空，不仅会返回默认值，还会将变量设置为这个默认值。
```bash
echo ${variable:=default_value}

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
default_value
```

- 2 否则返回 variable 的实际值。

### 2 、:-（如果指定的变量未设置或为空，则输出默认值。）
- 1 并没有实际修改variable的值。
```bash
echo ${variable:-100}

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
100
```

### 3、:?（确保某个变量必须存在，未设置时给出错误消息，并终止程序）
```bash
echo ${variable:?error_message}

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
./test.sh: 行 24: variable: error_message

```





## 特殊单字符在shell中的规则作用
### 1 、`"` 双引号（部分引用）
- 1 **部分引用**：允许变量替换和命令替换，但阻止通配符（如 `*`）扩展。
```bash
name="World"
echo "Hello $name"  # 输出: Hello World
echo "Files: *.txt"  # 输出: Files: *.txt（不会匹配文件）

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
Hello World
Files: *.txt
```
- 2 双引号内仍需转义 `$`、`\``、`"`、`\` 等特殊字符。
- 2 不解析⼤部分特殊字符
### 2 、`'` 单引号（完全引用）
- 1 **完全引用**：禁止所有变量替换和通配符扩展，内容按字面处理。


### 3 、`\` 

####   行继续符（将多行内容连接成一行）
```bash
echo 第一行 11 \
 第二行\
 第三行\

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
第一行 11 第二行 第三行
```
- 2 最后一行的 `\` 是多余的
- 2  `\` 必须位于行末（无空格）。
#### **转义特殊字符**（取消特殊字符的含义（如 `$`, `"`, `'`, `*` 等）
```bash
echo "Price is \$5"  # 输出: Price is $5
echo "Hello \"World\""  # 输出: Hello "World"

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
Price is $5
Hello "World"
```

- 2 在单引号 `' '` 中，`\` 不会转义特殊字符（除单引号本身）。
```bash
echo "Price is \$5"  # 输出: Price is $5
echo 'Hello "World"'  # 输出: Hello "World"

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
Price is $5
Hello "World"
```


#### **表示特殊控制字符**（表示换行符 `\n`、制表符 `\t` 等）（要加-e 转义）
```bash
echo -e "Hello\nWorld"  # 输出两行：Hello 和 World
echo -e "Name:\tJohn"    # 输出：Name:    John（包含制表符）

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
Hello
World
Name:	John

```




### 4 、$  （解释后面内容为变量名或特殊参数，而不是普通字符串）
```bash
variable=11
variable+=22
echo variable

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
variable
```

####  `${}`（需要明确变量边界时非常有用）（功能同`$`）
```
(base) topeet@ubuntu:~/shell_test$ echo /home/user${USER}_data
/home/usertopeet_data

```

#### `$(command)`（执行命令并替换为结果）
```
(base) topeet@ubuntu:~/shell_test$ echo $(ls)
a1.c filelist.txt newdir system.log test.sh

```


### 5、**`*` 星号**（通配符）
- 1 **通配符**：匹配任意字符序列（包括空字符）。

### 6、**`|` 管道符**
- 1 **管道**：将前一个命令的输出作为后一个命令的输入。


### 7、`()` 子 Shell运行
- 1 **子 Shell 执行**：在子 Shell 中运行命令。

```bash
(cd /tmp; pwd)  # 进入 /tmp 并输出路径，但当前 Shell 路径不变

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
/tmp
```

- 2 ⼦进程的变量和更改不会影响当前进程

####  `(( ))`（进⾏整数的逻辑判断）（c语言化）
- 1 shell中的⼀个内置命令

```bash
if (( 3 > 2 )) ;then 
    echo "3 > 2" 
fi

(base) topeet@ubuntu:~/shell_test$ ./test.sh
3 > 2

```


#### `<(command)`（进程替换）
```bash
cat <(ls)

(base) topeet@ubuntu:~/shell_test$ ./test.sh
a1.c
a2.c
filelist.txt
mysql-bin.001880
newdir
system.log
test.sh
```

- 2 将⼩括号⾥⾯命令的输出存储到⼀ 个⽂件描述符（通常是⼀个命名管道或临时⽂件）中，然后其他命令可以像读取普通⽂件⼀样读取命令的输出。

#### 





### 8、`[]`（匹配范围内的单个字符）（通配符）

```c
(base) topeet@ubuntu:~/shell_test$ touch a1.c
(base) topeet@ubuntu:~/shell_test$ ls *[0-9]*
a1.c

```

- 1 使用 `[^...]` 或 `![...]` 来排除特定字符。
```c
(base) topeet@ubuntu:~/shell_test$ touch a2.c
(base) topeet@ubuntu:~/shell_test$ ls a[^1].c
a2.c
(base) topeet@ubuntu:~/shell_test$ ls a[^2].c
a1.c

```
#### `test` 命令的一个别名（输出真假（1/0））（同逻辑符用）
```
[ expression ] == test expression
```
- 1 `[]`内左右必须有一个空格。
```c
(base) topeet@ubuntu:~/shell_test$ if [ "string1" = "string1" ]; then echo "Strings are equal"; fi

Strings are equal
```


#### 用作test时的常用用法
> [!PDF|yellow] [[嵌入式知识学习（通用扩展）/linux基础知识/assets/🔨shell语言学习/file-20250810171436705.pdf#page=17&selection=219,0,233,1&color=yellow|shell脚本语言（未整理）, p.17]]
> > 2.字符串⽐较 - 字符串操作符

> [!PDF|yellow] [[嵌入式知识学习（通用扩展）/linux基础知识/assets/🔨shell语言学习/file-20250810171436705.pdf#page=18&selection=246,0,261,1&color=yellow|shell脚本语言（未整理）, p.18]]
> > ⽂件状态 - 测试选项及其含义：
> 
> 

> [!PDF|yellow] [[嵌入式知识学习（通用扩展）/linux基础知识/assets/🔨shell语言学习/file-20250810171436705.pdf#page=20&selection=119,0,132,1&color=yellow|shell脚本语言（未整理）, p.20]]
> > 数值⽐较 - 数值⽐较操作符

#### 判断“存在”（包括普通文件、目录、链接等任何类型）

```
if [ -e "$file" ]; then
  echo "文件存在"
  # 或者 exit 0
else
  echo "文件不存在"
  # 或者 exit 1
fi

```

####  `[[]]`（替代 test 命令中的 -a 和 -o和!）（“与”逻辑、“或”逻辑、逻辑⾮）
- 1 test 命令中的 -a       <span style="background:#b1ffff">“与”逻辑</span>，即两个条件都必须为真。
- 2 test -r file -a -x file

```bash
[[ -r file && -x file ]]
```


- 1 test 命令中的 -o     <span style="background:#b1ffff">“或”逻辑</span>，即任意⼀个条件为真即可。
- 2 test -r file -o -x file

```bash
[[ -r file || -x file ]]
```

- 1 条件为假时返回真。
- 2 test ! -x file

```bash
[[ ! -x file ]]
```


### 9、 `{}`（`{}`由当前的shell执⾏，会影响当前变量）

#### `{ command1; command2; }`（依次执⾏）
- 1 括号两边必须有空格
- 1 每个指令都需要以分号 ; 结尾

```bash
(base) topeet@ubuntu:~/shell_test$ { ls;cd ..; }
a1.c  filelist.txt  newdir  system.log  test.sh
(base) topeet@ubuntu:~$ 

```

#### `{ str1,str2,str3 }`（扩展为多个独⽴的字符串）
```c
(base) topeet@ubuntu:~/shell_test$ echo {a,b,c,d,e}.txt
a.txt b.txt c.txt d.txt e.txt

```


#### `{ start..end }`（⽣成从起始值到结束值的序列）
```c
(base) topeet@ubuntu:~/shell_test$ touch mysql-bin.001837
(base) topeet@ubuntu:~/shell_test$ touch mysql-bin.001880
(base) topeet@ubuntu:~/shell_test$ sudo rm -f mysql-bin.0018{37..79}
(base) topeet@ubuntu:~/shell_test$ ls
a1.c  filelist.txt  mysql-bin.001880  newdir  system.log  test.sh
```


#### `${command}`（同上）




### 10、` _ `（​占位符）（临时存储）
```bash
read -r field1 _ field3 <<< "value1 value2 value3"
echo "需要的字段: $field1 和 $field3"

while read -r name _ age; do
    echo "姓名: $name, 年龄: $age"
done <<EOF
Alice 女 25
Bob 男 30
EOF

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
需要的字段: value1 和 value3
姓名: Alice, 年龄: 25
姓名: Bob, 年龄: 30
```
- 1 忽略不需要的输入字段
- 1 遍历文件时跳过某些列：

- 2  `_` 纯粹是编程约定，不直接影响脚本逻辑, 避免滥用

### 11、？（匹配单个任意字符）
```bash
(base) topeet@ubuntu:~/shell_test$ touch aa.c
(base) topeet@ubuntu:~/shell_test$ ls ?a.c
aa.c

```

### 12、`>`（输出重定向，并覆盖文件）
```shell
(base) topeet@ubuntu:~/shell_test$ ls > filelist.txt
(base) topeet@ubuntu:~/shell_test$ cat filelist.txt 
a1.c
aa.c
filelist.txt
test.sh

```


### 13、`>>`（输出重定向，内容追加到⽂件尾部。）
```bash
(base) topeet@ubuntu:~/shell_test$ echo "System rebooted at $(date)" >> system.log
(base) topeet@ubuntu:~/shell_test$ cat system.log 
System rebooted at 2025年 07月 10日 星期四 05:45:51 PDT
System rebooted at 2025年 07月 10日 星期四 05:46:15 PDT

```

### 14、`;`（分隔多个命令，让多个命令顺序执⾏）
```bash
(base) topeet@ubuntu:~/shell_test$ ls; pwd
a1.c  aa.c  filelist.txt  system.log  test.sh
/home/topeet/shell_test

```

### 15、`&`（命令后台执⾏）


### 16、`&&`（前⾯的命令执⾏成功后再执⾏后⾯的命令。）
> (base) topeet@ubuntu:~/shell_test$ `mkdir newdir && cd newdir`
> (base) topeet@ubuntu:~/shell_test/newdir$ 


### 17、`||`（前⾯的命令执⾏失败时再执⾏后⾯的命令）
> (base) topeet@ubuntu:~/shell_test/newdir$ `rm file.txt || echo "Failed to delete the file."
rm: 无法删除 'file.txt': 没有那个文件或目录
Failed to delete the file.

> (base) topeet@ubuntu:~/shell_test$ rm aa.c || echo "Failed to delete the file."
> (base) topeet@ubuntu:~/shell_test$ 

### 18、`~`（代表⽤⼾家⽬录路径。）
```
cd ~
```

### 19、数字键1左⾯的反引号（命令执⾏）
- 1 反引号中的内容作为系统命令,并执⾏其内容
```bash
echo `date`     # 反引号
echo $(date)    # $()

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
2025年 07月 10日 星期四 01:35:20 PDT
2025年 07月 10日 星期四 01:35:20 PDT

```



### 20、


### 21、



## `$类`变量
```bash
# $# 是一个特殊变量，它表示传递给脚本或函数的参数个数。
echo "传递给脚本的参数的个数=$#"

# $* 是一个特殊变量，它表示所有传递给脚本或函数的参数的内容。
echo "所有传递给脚本的参数的内容=$*"

# $1 表示第一个传递给脚本或函数的参数。
echo "第一个参数: $1"

# 下面是一个简单的示例，输出第三个参数（注意这里的索引从1开始）。
echo "第三个参数: $3"

# readonly 声明一个只读变量 data，并赋值为 10。
readonly data=10

# 尝试修改只读变量 data 的值为 250。
data=250

# $? 捕获上一条命令的退出状态。由于试图修改只读变量，这将返回非零值表示失败。
echo "尝试修改只读变量的结果: $?"

# $$ 是当前shell进程的ID。
echo "进程名: $0"
echo "进程号: $$"

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh a b c
传递给脚本的参数的个数=3
所有传递给脚本的参数的内容=a b c
第一个参数: a
第三个参数: c
./test.sh: 行 51: data：只读变量
尝试修改只读变量的结果: 1
进程名: ./test.sh
进程号: 7778

```


## 环境变量
### 1 、 环境变量的定义
- 1 环境变量是定义在当前环境（进程）中、并可以被当前进程及其所有⼦进程访问和继承的特殊变量。
[[嵌入式知识学习（通用扩展）/linux基础知识/assets/🔨shell语言学习/file-20250810171436725.png|Open: Pasted image 20250710222928.png]]
![嵌入式知识学习（通用扩展）（未）/边开发边积累/assets/shell语言学习/file-20250810171436725.png](assets/🔨shell语言学习/file-20250810171436725.png)

### 2 、EDITOR（指定文本编辑器）
- 1 将默认文本编辑器设置为`nano`
```bash
export EDITOR=nano
```

### 3 、SHELL（shell路径）
```c
(base) topeet@ubuntu:~/shell_test$ echo $SHELL
/bin/bash
```

### 4 、USER（当前登录的⽤⼾名）


### 5、HOME（家⽬录路径）


### 6、PATH（控制命令搜索路径）
- 1 PATH 是⼀个⽤冒号（ : ）分隔的⽬录列表，系统在执⾏命令时，会按照这些⽬录的顺序依次查找可执⾏⽂件。

```bash
echo $PATH
```

#### 临时修改 PATH 环境变量（仅当前终端会话⽣效）
- 1 export PATH=$PATH:/new/directory

- 1 若需优先搜索新⽬录，可将新路径放在前⾯： 
- 2 export PATH=/new/directory:$PATH


#### 永久修改PATH 环境变量（当前⽤⼾⽣效）（`~/.bashrc`）（记得source保存）
- 1 修改 `~/.bashrc` 或 `~/.bash_profile`或`~/.profile`
```bash
    # 打开文件（如使用 vi 或 nano）
    vi ~/.bashrc
    # 在文件末尾添加：
    export PATH=$PATH:/home/ming/ming/linux-v3.1.x/linux/prebuilts/gcc/linux-x86/aarch64/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/bin/
    # 保存后执行以下命令使修改生效：
    source ~/.bashrc
```

#### 永久修改（系统全局⽣效）（`/etc/profile`）

```bash
    # 需 root 权限
    sudo vi /etc/profile
    # 添加：
    export PATH=$PATH:/new/directory
    # 保存后执行：
    source /etc/profile
    # 或重启系统
```

#### 注意
- 1 必须使⽤绝对路径
- 1 避免空格：路径中若有空格，需⽤引号包裹（如 "/path with space" ）。

- 1 若需全局访问某个可执⾏⽂件，可创建软链接到 /usr/local/bin ：
- 2 sudo ln -s /path/to/your_program /usr/local/bin/



### 7、LANG（指定系统使⽤的语⾔环境）
- 1 中⽂环境： zh_CN.UTF-8 ，英⽂环境： en_US.UTF-8 。
```c
(base) topeet@ubuntu:~/shell_test$ echo $LANG
zh_CN.UTF-8

```

### 8、IFS（定义Shell在进⾏分词或字段拆分时使⽤的字符）
- 1 当shell在处理命令或变量展开时，会依据 IFS 中的字符来确定如何将⼀个字符串拆分为多个字段。IFS 默认指定的分隔符是空格、制表符（tab）和换⾏ 符的组合。

```c
(base) topeet@ubuntu:~/shell_test$ printf "%q\n" "$IFS"
$' \t\n'

```

### 9、CROSS_COMPILE（指定用于目标平台的编译器前缀）
> 通常与构建系统（如 **Makefile）配合使用**，以便**自动选择正确的编译工具链**。





## 命令变量
### 1 、`test condition`（测试输出布尔值）（看`[]`就可）
- 1 检查文件类型、比较字符串、数值比较等。其主要功能是根据给定的条件返回布尔值（真或假）

[shell语言学习 \> 8、\`\[\]\`（匹配范围内的单个字符）（通配符）](#8、`[]`（匹配范围内的单个字符）（通配符）)


### 2 、`read` --从键盘获取值保存到变量
- 1 在一行上显示和添加提示 需要加上-p

```bash
read -p "请输入你的名字: " name
echo "你好，$name！"

(base) topeet@ubuntu:~/shell_test$ ./test.sh
请输入你的名字: ming
你好，ming！
```
### 3 、`readonly`--只读变量
```bash
readonly num=10
num=20  # 尝试修改只读变量，将会失败

(base) topeet@ubuntu:~/shell_test$ ./test.sh
./test.sh: 行 135: num：只读变量
```

### 4 、`env`  、`export`--查看当前终端环境
```bash
(base) topeet@ubuntu:~/shell_test$ env
SHELL=/bin/bash
SESSION_MANAGER=local/ubuntu:@/tmp/.ICE-unix/2343,unix/ubuntu:/tmp/.ICE-unix/2343
QT_ACCESSIBILITY=1
COLORTERM=truecolor
XDG_CONFIG_DIRS=/etc/xdg/xdg-ubuntu:/etc/xdg
XDG_MENU_PREFIX=gnome-
GNOME_DESKTOP_SESSION_ID=this-is-deprecated

```

### 5、`source`--导出环境变量
<span style="background:#b1ffff"> 作用：（让其他shell脚本识别该变量，设为全局变量）</span>
<span style="background:#affad1">只对当前终端生效。</span>

### 6、 `echo` --打印
#### echo工作原理（`echo $filename`）
> 1<span style="background:#d3f8b6">. 先将变量展开，替换为具体的变量值</span>，因为ls命令的输出是多行内容，所以原始值中包含换行符。
> 2.<span style="background:#d3f8b6"> shell会根据 IFS（空格、换行符、Tab） 将展开后的变量分隔为为多个单词</span>
> 3.shell 会<span style="background:#d3f8b6">将分隔后的单词作为参数传给 echo，echo命令再逐个以空格间隔打印这些单词</span>

### 7、unset（删除变量）
- 1 交互式 Shell 中⼿动定义的变量会⼀直存在，此时就需要⼿动销毁。
```bash
name=tom
unset name

echo ${name}_aaa

(base) topeet@ubuntu:~/shell_test$ ./test.sh
_aaa
```

- 1 脚本执⾏完毕后，变量都会⾃动释放，不会再保留在系统中。
### 8、local （在函数内部声明局部变量 ）
- 1 通过 `local` 关键字声明的变量只在其所在的函数以及由该函数调用的子函数中有效
```bash
# 定义一个全局变量
global_var="I am global"

function show_local() {
    # 在函数内部声明一个局部变量
    local func_local="I am local to func_show"
    
    echo "Inside function: $func_local"
    echo "Inside function (global): $global_var"
}

# 调用函数
show_local

# 尝试访问函数内的局部变量
echo "Outside function: $func_local" # 这里会输出空值或者原始环境中的值，因为func_local是局部变量

echo "Outside function (global): $global_var"

(base) topeet@ubuntu:~/shell_test$ ./test.sh
Inside function: I am local to func_show
Inside function (global): I am global
Outside function: 
Outside function (global): I am global
```




# 三、shell语法

## 对变量的限制
### 1 、定义变量规则
- 1 变量名由数字、字⺟和下划线组成，且不允许使⽤数字开头
- 1 等号两边不能有空格。
- 1 

```bash
 #有空格，不合法 
 AGE = 18 
 # 存在非数字、字母和下划线字符，不合法 
 chunk-name=fdfasfas.js 
 # 数字开头，不合法 
 8Name=tom 

```

- 1 如果变量值存在空格或其他特殊字符， 需要使⽤引号保护，表⽰是⼀个整体。
- 1 双引号：可以解析变量的值   ，单引号：不能解析变量的值
```bash
# 存在空格，需要使用引号让其成为整体 
NAME="John Wilson" 
# 存在特殊字符，需要转义或用单引号 
PRICE='$18' 
```


### 2 、三种变量类型(普通变量、全局变量、局部变量)（作用域）
```bash
# 普通变量，当前 Shell 或脚本有效 
age=18 

# 全局变量，，能被当前Shell创建的子进程继承。 
export age=18 

# 局部变量，函数内生效 
get_name() 
{ 
	local name=tom 
} 
1213444
```
- 1 普通变量，当前 Shell 或脚本有效 
- 1 全局变量，，能被当前Shell创建的子进程继承。
- 1 局部变量，函数内生效 



### 3 、

### 4 、



##  `${str:3:6}`（字符串操作语法）
```bash
# 定义一个字符串变量
str="hehe:haha:xixi:lala"

# 测量字符串的长度
echo "str的长度为: ${#str}"  # 输出 str的长度为: 23

# 从下标3的位置开始提取子串
echo "${str:3}"  # 输出 he:haha:xixi:lala

# 从下标为3的位置开始提取长度为6字节的子串
echo "${str:3:6}"  # 输出 he:hah

"# 使用新字符替换str中出现的第一个旧字符（例如：用#替换第一个:）"
echo "${str/:/#}"  # 输出 hehe#haha:xixi:lala

 "使用新字符替换str中所有的旧字符（例如：用#替换所有:）"
echo "${str//:/#}"  # 输出 hehe#haha#xixi#lala

(base) topeet@ubuntu:~/shell_test$ sudo ./test.sh
str的长度为: 19
e:haha:xixi:lala
e:haha
hehe#haha:xixi:lala
hehe#haha#xixi#lala
```

- 2 从下标为3的位置开始提取长度为6字节的子串
- 2 


## 控制语句
### 1.if控制语句
- 1 不用在意空格格式

#### 1.1 `if[]; then  --else  --fi
```
if [条件1]; then
    执行第一段程序
else
    执行第二段程序
fi

```


#### 1.2 `if[]; then  --elif[]; then  --else  --fi
```
if [条件1]; then
    执行第一段程序
elif [条件2]；then
执行第二段程序
else
    执行第三段程序
fi

```



### 2. case 结构   `case $变量 in  --esac`
**格式** ：
```bash
# 定义变量a，并赋值为1
a=1

# 使用case语句根据变量a的值执行相应的操作
case $a in  
    1)
        # 当变量a等于1时执行的代码块
        echo "匹配到模式1"
        ;;
    2)
        # 当变量a等于2时执行的代码块
        # 注意：原代码中的echo没有提供输出内容，这里假设可能是遗漏了或者有特定目的。
        echo "匹配到模式2"
        ;;
    *)
        # 如果以上情况都不满足（即默认情况），则执行这里的代码
        echo "没有匹配到任何模式"
        ;;
esac

(base) topeet@ubuntu:~/shell_test$ ./test.sh
匹配到模式1

```

### 3. for 循环

#### 3.1 `for 变量 in 输入列表;do  --done`（依次把列表中的值赋给变量）

```bash
# 使用for循环遍历给定的名字列表
for name in tom bob alice; do
    # 对于列表中的每个名字，执行以下操作：
    # 输出当前迭代的名字到控制台
    echo $name
done

(base) topeet@ubuntu:~/shell_test$ ./test.sh
tom
bob
alice
```


#### 3.2 `for ((   )) ;do  --done`（同c语言的用法）

```bash
# 初始化表达式; 条件表达式; 迭代表达式
for ((i=0; i<5; i++)); do
    # 在每次循环中执行的命令
    echo "1111"
done

(base) topeet@ubuntu:~/shell_test$ ./test.sh
1111
1111
1111
1111
1111
```



### 4.while 循环

#### 4.1`while 条件;do  --done`(基于某个条件来动态控制循环次数)

```bash
# 初始化计数器变量i为1
i=1
# 当i小于5时，持续循环
while [ $i -lt 5 ]; do
    # 打印当前i的值
    echo "当前数字: $i"
    
    # i自增1，避免造成无限循环
    i=$((i+1))
done

(base) topeet@ubuntu:~/shell_test$ ./test.sh
当前数字: 1
当前数字: 2
当前数字: 3
当前数字: 4
```




### 5.select 循环
通过 select 可以在shell中用于生成简单交互式菜单的命令，<span style="background:#d3f8b6">让用户通过输入选项编号来选择其中之一</span>。select 一般结合 PS3变量使用，通过PS3变量可以指定 select 命令的提示符，让用户知道该输入选项编号。

#### 5.1 `select 变量 in 列表 ;do  --done`（根据用户的选择把列表中对应值赋给变量）

- 1 **举例** ：实现一个选择菜单
```bash
# 设置提示信息，这将在用户被要求输入时显示
PS3="请选择指定序号: "

# 使用select结构创建一个菜单，供用户从"MySQL", "Redis", "Mqtt1884", "Mqtt1883"中选择一个
# 选择的结果将会存储在变量opt中
select opt in "MySQL" "Redis" "Mqtt1884" "Mqtt1883"; do
    # 根据用户的选择执行不同的操作
    case $opt in
        # 如果用户选择了"MySQL"
        "MySQL")
            echo "MySQL"
            # 使用break语句退出select循环
            break
            ;;
        # 如果用户选择了"Redis"
        "Redis")
            # 调用函数set_redis()来设置Redis服务
            set_redis
            # 使用break语句退出select循环
            break
            ;;
        # 如果用户选择了"Mqtt1884"
        "Mqtt1884")
            # 调用函数set_mqtt1884()来设置MQTT服务端口1884
            set_mqtt1884
            # 使用break语句退出select循环
            break
            ;;
        # 如果用户选择了"Mqtt1883"
        "Mqtt1883")
            # 调用函数set_mqtt1883()来设置MQTT服务端口1883
            set_mqtt1883
            # 使用break语句退出select循环
            break
            ;;
        # 默认情况：如果用户输入的不是一个有效的选项
        *)
            # 提示用户输入无效，并请他们重试
            echo "无效的选择，请重试"
            ;;
    esac
# 结束select循环
done

(base) topeet@ubuntu:~/shell_test$ ./test.sh
1) MySQL
2) Redis
3) Mqtt1884
4) Mqtt1883
请选择指定序号: 1
MySQL

```
- 2 `PS3`是一个特殊的环境变量，它定义了`select`循环中的提示字符串。作为提示用户输入的选择菜单的前缀。
- 2 如果未设置`PS3`，默认情况下它的值为`#?`


### 6. break 和 continule（同c语言）

- **break 命令** ：<span style="background:#b1ffff">终止整个循环</span>。当执行到 `break` 命令时，循环立即结束，程序控制流<span style="background:#d3f8b6">跳出循环体</span>，继续执行循环后面的代码。
- **continue 命令** ：<span style="background:#d3f8b6">跳过当前循环中余下的命令，立即进入下一次循环迭代</span>。当执行到 `continue` 命令时，当前迭代剩下的命令不会执行，循环直接进入下一次迭代的判断。

# 四、函数
## 1.定义函数
**完整格式** ：
```bash
function fun_name()
{
    command;
}
```

**简写格式** ：
```bash
# 省略小括号：
function fun_name
{
    command;
    command;
}

# 省略function 关键字：
fun_name() 
{
    command;
    command;
}

```


## 2.调用函数

> **说明** ：shell 脚本是从上到下依次执行的，如果在调用函数之前没有定义，shell 会提示“未找到命令”或类似的错误。所以需要<span style="background:#b1ffff">先定义函数才能调用函数。</span>

- 无参调用：直接通过函数名即可调用函数
- 传参调用：<span style="background:#affad1">函数名后面跟参数，参数一般使用空格分隔。函数内通过 `$1` 、 `$2` 等来引用这些参数</span>

```bash
# 定义一个名为 fun_name 的函数
function fun_name()
{
    # 函数体内的命令或一系列命令，这里以 'command;' 作为占位符表示具体执行的命令
    # 注意：在实际应用中，'command;' 应替换为需要执行的具体命令或者一系列命令
    ls;
    echo $1;
}


fun_name 1111

(base) topeet@ubuntu:~/shell_test$ ./test.sh
a1.c  a2.c  filelist.txt  mysql-bin.001880  newdir  system.log	test.sh
1111

```


## 3.函数返回值
调用函数后，<span style="background:#d3f8b6">命令状态退出码（$?） 就是函数的返回值</span>，<span style="background:#d3f8b6">默认情况下函数的返回值就是最后一条命令执行状态的退出码</span>，也可以退出return 命令来指定函数的退出状态码。

### 3.1 return 命令（指定函数的退出状态码）（退出函数执行）
- 1 退出函数执行：如果在函数的其他位置使用，则当函数执行到 `return` 时，会立即退出函数并返回控制权给调用者，函数后续的指令不会被执行。


```bash
# 示例函数定义，演示如何使用return命令指定函数退出状态码
function example_function() {
    # 函数体内的命令
    local result=0  # 初始化一个局部变量result，假设它用于存储操作结果

    # 假设这里有一系列操作，根据操作的结果设置result变量
    # 如果操作成功，则设置result为0（通常表示成功）
    # 如果操作失败，则设置result为非0值（通常表示错误）

    # 使用return命令来指定函数的退出状态码
    # 这里我们直接使用result变量作为退出状态码
    return $result
}

# 调用example_function函数
example_function

# 获取并打印函数的退出状态码。$?是上一条命令执行后的退出状态码
# 在这个例子中，它就是example_function函数的返回值
echo "Function exit status: $?"

# 注意：在实际应用中，可以根据需要修改函数体内的逻辑以及return语句的参数。

(base) topeet@ubuntu:~/shell_test$ ./test.sh
Function exit status: 0
```





# 五、

## 特殊用法讲解
### 1 、单引号和双引号嵌套
```bash
AME=TOM 
# My Name is 'TOM' 
echo "My Name is '${NAME}'"
```

> 说明 ：上⾯说了单引号中的任何内容都会原样输出，但是这⾥的<span style="background:#affad1">单引号在双引号内，双引号内的单引号就是⼀个普通字符，双引号内的$会被shell解释，所以能展开变量</span>。


### 2 、shell脚本不一定以.sh结尾

> xgrids@lixel:/usr/bin$ `file ./bt-attach `
./bt-attach: Bourne-Again `shell script`, ASCII text executable



### 3 、脚本所在目录与上一级目录（💌）
```c
#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 获取上一级目录
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

echo "脚本所在目录: $SCRIPT_DIR"
echo "上一级目录: $PARENT_DIR"
```


### 4 、

### 5、


### 6、


### 7、


### 8、



## test condition和 []条件测试详解
### 1 、 Shell `test` / `[ ]` 条件测试速查表

|**类别**|**语法**|**含义**|**示例**|
|---|---|---|---|
|**文件测试**|`-e file`|文件是否存在|`[ -e /tmp/log.txt ]`|
||`-f file`|是否为普通文件|`[ -f script.sh ]`|
||`-d dir`|是否为目录|`[ -d /home/user ]`|
||`-s file`|文件存在且**非空**|`[ -s data.csv ]`|
||`-r file`|当前用户对文件有**读权限**|`[ -r config.ini ]`|
||`-w file`|当前用户对文件有**写权限**|`[ -w output.log ]`|
||`-x file`|当前用户对文件有**执行权限**|`[ -x backup.sh ]`|
||`-L file`|是否为符号链接（软链接）|`[ -L /usr/bin/python ]`|
|**字符串测试**|`-z str`|字符串**为空**（zero length）|`[ -z "$input" ]`|
||`-n str` 或 `str`|字符串**非空**（non-zero）|`[ -n "$name" ]` 或 `[ "$name" ]`|
||`str1 = str2`|两个字符串**相等**|`[ "$a" = "$b" ]`|
||`str1 != str2`|两个字符串**不相等**|`[ "$user" != "root" ]`|
|**数值比较**|`num1 -eq num2`|相等（equal）|`[ $age -eq 18 ]`|
||`num1 -ne num2`|不相等（not equal）|`[ $code -ne 0 ]`|
||`num1 -gt num2`|大于（greater than）|`[ $score -gt 90 ]`|
||`num1 -ge num2`|大于等于（greater or equal）|`[ $count -ge 10 ]`|
||`num1 -lt num2`|小于（less than）|`[ $i -lt 5 ]`|
||`num1 -le num2`|小于等于（less or equal）|`[ $retry -le 3 ]`|
|**逻辑组合**|`cond1 -a cond2`|逻辑 **与**（and，POSIX 兼容）|`[ -f file.txt -a -r file.txt ]`|
||`cond1 -o cond2`|逻辑 **或**（or，POSIX 兼容）|`[ -z "$a" -o -z "$b" ]`|
||`! cond`|逻辑 **非**|`[ ! -e missing.txt ]`|
||`cmd1 && cmd2`|命令级 **与**（推荐现代脚本使用）|`[ -f log ] && echo "Exists"`|
||`cmd1 \| cmd2`|命令级 **或**|`[ -w data ] \| echo "No write"`|
```bash
[ -b FILE ]
	判断 FILE 是否存在 且是一个块设备文件（block special file）




```





### 2 、方括号 [ ] 两边必须有空格


### 3 、变量建议加双引号：防止空值或含空格时报错，如 [ -z "$var" ]


### 4 、


### 5、


### 6、


### 7、


### 8、



## 
### 1 、


### 2 、


### 3 、

### 4 、

### 5、


### 6、


### 7、


### 8、

