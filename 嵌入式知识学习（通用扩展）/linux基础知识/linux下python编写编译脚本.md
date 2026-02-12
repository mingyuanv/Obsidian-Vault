---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：




# 一、通过 Python 来调用 Shell 脚本的三种常用方式

```cardlink
url: https://blog.csdn.net/u013019701/article/details/121205743?ops_request_misc=%257B%2522request%255Fid%2522%253A%25226a8097819434e8f2b390a19230948b8d%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=6a8097819434e8f2b390a19230948b8d&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-1-121205743-null-null.142^v102^pc_search_result_base4&utm_term=%E9%80%9A%E8%BF%87%20Python%20%E6%9D%A5%E8%B0%83%E7%94%A8%20Shell%20%E8%84%9A%E6%9C%AC&spm=1018.2226.3001.4187
title: "通过 Python 来调用 Shell 脚本的三种常用方式_python调用xshell-CSDN博客"
description: "文章浏览阅读2.2w次，点赞7次，收藏48次。如何 通过 Python 来调用 Shell 脚本本文介绍三种写法使用os.system 来运行使用subprocess.run 来运行使用 subprocess.Popen 来运行三种方式的优缺点os.systemsubprocess.runsubprocess.Popen是否需要解析参数noyesyes同步执行（等待Shell执行结果）yesyesno能够获得 shell 的输入和输出noyesyesShell 执行结果返回值_python调用xshell"
host: blog.csdn.net
```

- 1 三种方式的优缺点

|                   | os.system    | subprocess.run | subprocess.Popen |
| ----------------- | ------------ | -------------- | ---------------- |
| 是否需要解析参数          | no           | yes            | yes              |
| 同步执行（等待Shell执行结果） | yes          | yes            | no               |
| 能够获得 shell 的输入和输出 | no           | yes            | yes              |
| Shell 执行结果返回值     | return value | object         | object           |
|                   |              |                |                  |

## `os.system`
```python
import os

return_code=os.system('ls -al .')

print(return_code)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
总用量 20
drwxrwxr-x 3 topeet topeet 4096 8月  11 00:56 .
drwxrwxr-x 6 topeet topeet 4096 7月  27 06:27 ..
drwxrwxr-x 3 topeet topeet 4096 8月  11 00:36 .idea
`-rw-rw-r-- 1 topeet topeet  504 7月  27 07:35 main.py`
-rwxrwxr-x 1 topeet topeet 2442 8月  11 00:56 test.py
`0`

> 也会将Shell语句的输出输出到的 Python的命令控制台中。
> 但是 Python 的能够获取的返回值，是数字，0 代表 Shell 语句/脚本的执行成功，否则表示Shell执行的状态值。
>  **适用于不需要详细的返回信息的 shell 脚本** 
>  传入 Shell 命令的**参数，都是完整的 String。**







## `subprocess.run`（推荐）
### 1 、 能够相当方便的控制 shell 命令的输入和输出
- 1 传入的参数是一个 **数组** 而不是字符串。
```python
import subprocess

return_code=subprocess.run(['ls','-al','.'])

print(return_code)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
总用量 20
drwxrwxr-x 3 topeet topeet 4096 8月  11 01:00 .
drwxrwxr-x 6 topeet topeet 4096 7月  27 06:27 ..
drwxrwxr-x 3 topeet topeet 4096 8月  11 00:36 .idea
-rw-rw-r-- 1 topeet topeet  504 7月  27 07:35 main.py
`-rwxrwxr-x 1 topeet topeet 2533 8月  11 01:00 test.py`
`CompletedProcess(args=['ls', '-al', '.'], returncode=0)`
- 2 执行返回的结果是一个CompletedProcess对象



### 2 、忽略shell 脚本执行的结果
```python
import subprocess

return_code=subprocess.run(['ls','-al','.'],stdout=subprocess.DEVNULL)

print(return_code)
```
> (base) topeet@ubuntu:~/test/python$ `python test.py`
`CompletedProcess(args=['ls', '-al', '.'], returncode=0)`
- 2 输出结果就仅有 Python 程序运行出的结果。





### 3 、指定 shell 命令的输入参数（通过 input 参数来传入）
```python
import subprocess

useless_cat_call=subprocess.run(['cat'],stdout=subprocess.PIPE,text=True,input="Hello")

print(useless_cat_call.stdout)

```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`Hello`

> - `stdout=subprocess.PIPE` 告诉 Python，**重定向 Shell 命令的输出**，并且这部分输出可以被后面的 Python 程序所调用。
> - `text=True` 告诉 Python，将 shell 命令的执行的 `stdout` 和 `stderr` 当成**字符串**. 默认是当成 bytes.
> - `input="Hello from the other side"` 告诉 Python，shell 命令的**输入参数**.


### 4 、开启 shell 命令的执行校验
- 1 当 shell 的执行出现任何问题，都会抛出一个异常。

```python
import subprocess

failed_command=subprocess.run(['false'],text=True)

print("The exit code was: %d" % failed_command.returncode)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
The exit code was: `1`





### 5、


### 6、subprocess.run方法参数的介绍
#### 核心控制参数​​
> 1. ​**​`args`​**​
>     - ​**​作用​**​：指定要执行的命令，支持​**​列表​**​（推荐）或​**​字符串​**​形式。
>     - ​**​注意​**​：列表形式可避免命令注入风险；字符串形式必须设置 `shell=True`。
```python
subprocess.run(["ls", "-l"])  # 安全方式（列表）[1,3] 
subprocess.run("ls -l", shell=True)  # 字符串需配合 shell=True[5]
```


> 2. ​**​`shell`​**​
>     - ​**​作用​**​：是否通过系统 Shell（如 `/bin/sh`或 `cmd.exe`）执行命令。
>     - ​**​风险​**​：`shell=True`可能引发安全漏洞（如执行恶意输入），非必要不启用
>     - ​**​适用场景​**​：需 Shell 特性（如通配符 `*`、管道 `|`）时使用。



> 3. ​**​`timeout`​**​
>     - ​**​作用​**​：设置命令超时时间（秒），超时抛出 `TimeoutExpired`异常。
>     - ​**​示例​**​：
```python
try:
    subprocess.run(["sleep", "10"], timeout=5)
except TimeoutExpired:
    print("命令超时！")  # 5秒后中断[3,6]
```

#### 输入/输出处理参数​​
> 1. ​**​`stdin`、`stdout`、`stderr`​**​
>     - ​**​作用​**​：控制子进程的标准流，可选值：
>         - `subprocess.PIPE`：捕获数据流（通过 `result.stdout`访问）
>         - `subprocess.DEVNULL`：丢弃输出（类似 `/dev/null`）。
>         - 文件对象：重定向到文件。
>     - ​**​示例​**​：
```python
result = subprocess.run(["ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
```

> 2. ​**​`capture_output`​**​
>     - ​**​作用​**​：简化输出捕获（等价于设置 `stdout=PIPE, stderr=PIPE`）。
>     - ​**​冲突​**​：不可与 `stdout`/`stderr`同时使用
>         



> 3. ​**​`input`​**​
>     - ​**​作用​**​：向子进程的 stdin 传递数据，需配合 `stdin=PIPE`（自动启用）。
>     - ​**​数据类型​**​：
>         - `text=True`时：​**​字符串​**​（如 `input="Hello"`）
>         - 默认：​**​字节流​**​（如 `input=b"Hello"`）。


> 4. ​**​`text`/ `encoding`​**​
>     - ​**​作用​**​：控制输入/输出的文本模式：
>         - `text=True`：**输入/输出自动转为字符串**（等价于 `universal_newlines=True`）
>         - `encoding="utf-8"`：指定编解码方式（如处理中文）。


#### 执行环境参数​​
> 1. ​**​`cwd`​**​
>     - ​**​作用​**​：设置子进程的工作目录。
>     - ​**​示例​**​：
```python
subprocess.run(["pwd"], cwd="/tmp")  # 输出 "/tmp
```

> 2. ​**​`env`​**​
>     - ​**​作用​**​：<span style="background:#d3f8b6">自定义环境变量（字典形式），默认继承父进程环境。</span>
>     - ​**​示例​**​：
```python
env = {"PATH": "/usr/bin", "MY_VAR": "test"}
subprocess.run(["echo", "$MY_VAR"], env=env, shell=True)[4](@ref)
```


#### 异常与状态处理​​
> 1. ​**​`check`​**​
>     - ​**​作用​**​：若子进程返回​**​非零退出码​**​，抛出 `CalledProcessError`异常。
>     - ​**​示例​**​：
```python
try:
    subprocess.run(["false"], check=True)  # 总是失败的命令
except CalledProcessError as e:
    print(f"错误码: {e.returncode}, 错误: {e.stderr}")
```


> 2. ​**​返回值 `CompletedProcess`​**​
>     - ​**​属性​**​：
>         - `returncode`：退出状态码（0 表示成功）。
>         - `stdout`/`stderr`：捕获的输出（文本或字节流）。
>         - `args`：执行的命令
>     - ​**​方法​**​：
>         - `check_returncode()`：<span style="background:#d3f8b6">非零退出码时抛出异常。</span>




#### 最佳实践总结​​
> 1. ​**​安全优先​**​：
>     - 使用​**​列表​**​传参（如 `["ls", "-l"]`），避免 `shell=True`除非必要

> 2. ​**​输出处理​**​：
>     - 需捕获输出时，用 `capture_output=True`+ `text=True`简化代码。

> 3. ​**​异常管理​**​：
>     - 关键命令添加 `check=True`+ `try/except`确保失败可追溯

> 4. ​**​跨平台注意​**​：
>     - Windows 部分命令（如 `dir`）需 `shell=True`

> 5. ​**​性能优化​**​：
>     - 避免频繁调用高开销命令（如反复启动 Shell）




### 7、


### 8、



## `subprocess.Popen`
### 1 、 `subprocess.Popen` 能够提供更大的灵活性。
- 2 `subprocess.run` 可以看成是 `subprocess.Popen` 一个简化抽象。 

### 2 、`subprocess.Popen`的使用与注意
> 1.默认情况下， `subprocess.Popen` 不会中暂停 Python 程序本身的运行`（异步）`
> 2.但是如果你非得同前面两种方式一样，同步运行，你可以加上 `.wait()` 方法。
> 3.当我们仍然处在异步的状况,通过 `poll()` 来轮询,知道shell 命令是否运行结束与否？当放回结果为 None，则表示程序还在运行，否者会返回一个状态码。

- 1 如果想， **指定输入参数** ，则需要通过 `communicate()` 方法。

```python
import subprocess

useless_cat_call=subprocess.Popen(['cat'],stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

output,errors=useless_cat_call.communicate(input="hello")
useless_cat_call.wait()

print(output)
print(errors)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`hello`



### 3 、



### 4 、




### 5、


### 6、


### 7、


### 8、




# 二、

## 
### 1 、


### 2 、


### 3 、

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



## 
### 1 、


### 2 、


### 3 、

### 4 、

### 5、


### 6、


### 7、


### 8、


# 三、

## 
### 1 、


### 2 、


### 3 、

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



## 
### 1 、


### 2 、


### 3 、

### 4 、

### 5、


### 6、


### 7、


### 8、


# 四、

## 
### 1 、


### 2 、


### 3 、

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



## 
### 1 、


### 2 、


### 3 、

### 4 、

### 5、


### 6、


### 7、


### 8、


# 五、

## 
### 1 、


### 2 、


### 3 、

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



## 
### 1 、


### 2 、


### 3 、

### 4 、

### 5、


### 6、


### 7、


### 8、


