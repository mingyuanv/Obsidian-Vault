---
title:
  - object Object
aliases: 
tags: 
description: 
source: 
dg-publish: true
---

# 备注(声明)：
[[嵌入式知识学习（通用扩展）/linux基础知识/assets/python入门/file-20250810171625353.png|Open: Pasted image 20250727213300.png]]
![RK3568（linux学习）/linux基础知识学习/assets/python入门/file-20250810170950326.png](assets/python入门/file-20250810171625353.png)



```cardlink
url: https://blog.csdn.net/zhiguigu/article/details/120217658?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522f6ec9dc20370da7774d894647366deff%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=f6ec9dc20370da7774d894647366deff&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-120217658-null-null.142%5Ev102%5Epc_search_result_base4&utm_term=python%E5%85%A5%E9%97%A8&spm=1018.2226.3001.4187
title: "万字【Python基础】保姆式教学，零基础快速入门Python_西安科技大学研究生院-CSDN博客"
description: "文章浏览阅读10w+次，点赞4.5k次，收藏1.9w次。本文带你快速入门Python，从语言介绍、安装指南、基本语法、数据类型、运算符到流程控制、列表、元组、字符串、字典、函数等知识点，适合初学者循序渐进学习。"
host: blog.csdn.net
```

# 一、python基础知识

## 
### 1 、python的特点
- 1 类库强⼤、㬵⽔语⾔（调⽤其他语⾔的类库）

### 2 、编译型和解释型
- 1 编译型是将代码（源⽂件）通过编译器，编译成机器码⽂件，当运⾏的时候直接执⾏机器码⽂件，例如C语⾔
- 2 执⾏快，不能跨平台

- 1 解释型是将源⽂件通过解释器，逐⾏进⾏翻译并运⾏。Python则属于解释型的语⾔。
- 2 执⾏慢，跨平台
### 3 、“#” 表⽰注释



### 4 、



### 5、


### 6、


### 7、


### 8、



## 软件安装（Windos）
### 1 、Python环境的安装
> [!PDF|note] [[嵌入式知识学习（通用扩展）/linux基础知识/assets/python入门/file-20250810171625640.pdf#page=5&selection=282,1,290,1&color=note|万字【Python基础】保姆式教学，零基础快速入门Python_西安科技大学研究生院-CSDN博客, p.5]]
> > 1）Python的安装步骤
> 
> 

### 2 、Pycharm的安装
> [!PDF|note] [[嵌入式知识学习（通用扩展）/linux基础知识/assets/python入门/file-20250810171625640.pdf#page=10&selection=67,0,70,7&color=note|万字【Python基础】保姆式教学，零基础快速入门Python_西安科技大学研究生院-CSDN博客, p.10]]
> > （2）Pycharm
> 
> 

### 3 、

### 4 、
### 5、


### 6、


### 7、


### 8、



## 
### 1 、标识符(变量名、函数名、类名等)的命名规范
> 1. 合法的标识符:字母，数字(不能开头),下划线，py3可以用中文（不建议），py2不可以。
> 2. 大小写敏感。
> 3. <span style="background:#affad1">不能使用关键字和保留字。</span>
> 关键字： if while for as import  
> 保留字：input，print range
> 4. 没有长度限制。
> 5. 望文生义，看到名字就知道要表达的意思。

- 1 大小写注意：
> 7. <span style="background:#d3f8b6">包名：全小写</span>，例如 time ;
>   8. <span style="background:#d3f8b6">类名：每个单词的首字母大写</span>，其他的小写，简称大驼峰命名，例如 HelloWorld ；
>   9. <span style="background:#d3f8b6">变量名/函数名:第一个单词的首字母小写</span>，后面的单词的首字母大写，简称小驼峰命名，例如 helloWorld ；
>   10. <span style="background:#d3f8b6">常量：全大写</span>，例如 HELLO 。



### 2 、


### 3 、

### 4 、

### 5、


### 6、


### 7、


### 8、

## 数据类型
### 1 、整型：整数


### 2 、浮点型：小数


- 2 科学计数法，<span style="background:#affad1">e表示乘以10几次方</span>，例如 b=1e10 表示1* 10的10次方。


### 3 、字符串的四种表现形式​
#### 单引号 `'xs'` 与双引号 `"xs"`（完全等价）
- 1 定义单行字符串

> - 单引号字符串内可直接包含双引号（无需转义）：`'She said, "Yes!"'`
> - 双引号字符串内可直接包含单引号：`"It's a nice day"`


#### ​​三引号 `"""..."""` 或 `'''...'''`
- 1 用于定义​**​多行字符串​**​，保留所有换行符和缩进格式

```python
    text = """Line 1
    Line 2"""
    print(text)  # 输出: Line 1\nLine 2
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/main.py 
> Hi, PyCharm
> `Line 1
>     `Line 2`



### 4 、布尔类型（bool）
- 1 True为真，False为假；1表示真，0表示假。


### 5、​`None`（内置的空值）
- 1 `None` 与以下常见“空值”本质不同

|​**​类型​**​|​**​示例​**​|​**​与 `None` 是否相等​**​|​**​说明​**​|
|---|---|---|---|
|​**​数字 0​**​|`0`|`False`|0 是整数类型|
|​**​空字符串​**​|`""`|`False`|空字符串是 `str` 类型|
|​**​空列表​**​|`[]`|`False`|空列表是 `list` 类型|
|​**​布尔假值​**​|`False`|`False`|`False` 是 `bool` 类型|

- 2 **​核心区别​**​：`None` 表示 ​**​“无值”或“未定义”​**​，而其他空值仅表示数据容器的“空状态”
- 2 `None` 仅与自身相等（`None is None` 为 `True`），与其他任何值比较均为 `False`

```python
if None:
    print("不会执行")  # 实际输出: 跳过此分支
else:
    print("执行此分支")  # 输出: 执行此分支 [1,2,4](@ref)
```


### 6、列表、元组、字典、集合也是常见的数据类型


### 7、表达式均有固定字面值
- 1 表达式是由数字、算符、数字分组符号（括号）、变量等对象的组合叫做表达式

### 8、


## 类型转换（强制类型转换）
### 1 、`int()`


### 2 、`float()`


### 3 、`str()`


### 4 、举例
```python
str1="333"
int1=11
float1=1.1

#字符串转整型
aa=int(str1)
print(aa)

#浮点型转整型
bb=int(float1)
print(bb)

# 字符串转浮点型
cc=float(str1)
print(cc)

# 整型转浮点型
dd=float(int1)
print(dd)

# 浮点型转字符串
ee=str(float1)
print(ee)

# 整型转字符串
rr=str(int1)
print(rr)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
333
1
333.0
11.0
1.1
11


### 5、


### 6、


### 7、


### 8、

## 运算符
### 1 、`+`，`-`，`*`，`/`（真除法）,`//`（地板除，舍去小数部分）,`%`（取余数）,`**`（幂运算）


### 2 、=（等号右边的值赋值等号左边）


### 3 、`+=`，`-=`，`*=`，`/=`,`%=`,`**=`（ 增强赋值运算符）


### 4 、\== （等于），！=（不等于） >=   <=   >    <（布尔运算法）


### 5、 not、and和or（逻辑运算符）
> and：前后都为真则为真  
> or：有一个为真则为真  
> not:非真，非假


### 6、


### 7、


### 8、


## 流程控制
### 1 、if（条件分支）
```python
if 布尔表达式1： #如果为真则执行内部的代码块
    代码块
elif 布尔表达式2：
    代码块
elif 布尔表达式3：
    代码块
....
else:
    代码块
```

**举例**
```python
a=69

if a>60:
    print("及格")
elif a>90:
    print("A")
else:
    print("C")
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`及格`



### 2 、while循环
```python
while 布尔表达式: 
    代码块
```


```
a=69
while a==69:
    print("1")
```

### 3 、for循环（技术循环）
```python
l=[3,2,1]
for 变量 in 可迭代对象:
    代码块
```


```python
l=[1,2,3]

for n in l:
    print(n)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
1
2
3


### 4 、range（可迭代对象）
```python
range(start=0,stop,step=1)
```
>start值的是<span style="background:#affad1">开始下标</span>。range序列里面的所有元素都有下标，第一个元素的下标是0，所以，默认是从0开始。
>stop是<span style="background:#affad1">结束位置</span>。结束的位置下标为（元素个数-1），例如range里面有4个元素，那么结束下标最大为3,大于3则跳出range。
>step是<span style="background:#affad1">步长</span>，如果step是2，那么每次会隔开1个元素，<span style="background:#d3f8b6">默认步长为1</span>，即每个元素都会取到。
- 1 可以不写star和step，但结束位置一定要写的


**举例**
```python
for n in range(12,4,-4):
    print(n)

```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
12
8


### 5、continue（跳过本次循环，后面的循环继续执行）
```python
for n in range(1,10):
    if n==5:
        continue
    print(n)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
1
2
3
`4
`6
7
8
9
### 6、break（终止所有循环）
```python
for n in range(1,10):
    if n==5:
        break
    print(n)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
1
2
3
4

### 7、


### 8、


## 列表(List)
### 1 、列表的特点
- 1 可以存放任何数据，包括整型，浮点型，字符串，布尔型等等

### 2 、列表的创建
```python
# 混合列表
l=[1,2,"a",0.2,true,1>2]

# 空列表
l=[]
```

#### 从列表中获取数据(元素)
```python
print(l[2])
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`a`
#### 列表的遍历
```python
for i in l:
	print(i,end="")
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`12a0.2TrueFalse`


#### 交换数据 - 对指定下标的元素进行数据交换
```python
l[2],l[3]=l[3],l[2]
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`120.2aTrueFalse`



### 3 、添加元素

|       函数       |            说明            |
| :------------: | :----------------------: |
|    append()    |        向列表末尾添加对象         |
| extend(可迭代的对象) | 将可迭代对象中数据分别添加到列表中，并添加到未尾 |
| insert(下标，对象)  |       向指定下标位置添加对象        |

- 1 统⼀⽤法是：
```python
# 变量.函数
l.extend([7,7,7])
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`12a0.2TrueFalse777`


### 4 、删除元素

| clear()  |             清空列表              |
| :------: | :---------------------------: |
|  pop()   | 删除**下标指定**的元素，如果不加下标则删除最后一个元素 |
| remove() |          删除**指定的对象**          |
|  del()   |        删除变量或指定**下标**的值        |
```python
l.remove(0.2)
print(l)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`[1, 2, 'a', True, False]`



### 5、修改元素
```
l[2]=777
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`[1, 2, 777, 0.2, True, False]



### 6、列表⾼级特性
#### 切⽚操作（把1个列表切分为多个列表）
```
# 变量[起始下标:结束下标] #结束下标取不到

print(l[0:3])
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
**[1, 2, 'a']**

- 1 注意
> ①如果**下标从0开始可以省略不写**，例如 n = l[:4] 
> ②如果**结束下标取的是最后一个元素，可以省略不写**，例如 n = l[3:] 
> ③如果列表中的元素都要，开始和结束下标都可以省略，例如 n = l[:] 
> ④n = l[: `-1` ] 表示从0开始 - **到倒数二个元素**


#### ` n = l[开始:结束:步⻓]`
- 1 可以正向去操作列表，也可以反向去操作列表
```
n=l[-1:-4:-2]
print(n)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
**[False, 0.2]**




#### 列表的⽐较运算
- 1 列表之间进⾏⽐较，以相同下标进⾏⽐较，从⼩到⼤进⾏⽐较，如果值相同则⽐较下⼀组元素，如果不同直接出结果

```
l=[1,2,3]
l2=[1,3,5]

print(l<l2)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`True`



#### 逻辑运算（and、not、or）
- 1 跟⽐较运算符相似，返回结果都是布尔值（True/False）
- 2  **`and`（逻辑与）​**：左右条件​**​均需为 `True`​**​ 才返回 `True`，否则返回 `False`。
 - 2 **`or`（逻辑或）​**：左右条件​**​至少一个为 `True`​**​ 即返回 `True`，全 `False` 才返回 `False`
- 2 **`not`（逻辑非）​**：对布尔值取反（`True` → `False`，`False` → `True`）。

```python
l=[1,2,3]
l2=[1,3,5]

print((l<l2)and(l2<l))
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`False`


#### 拼接运算（`+`）
- 1 进⾏两个列表拼接
```
l=[1,2,3]
l2=[1,3,5]

print(l+l2)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`[1, 2, 3, 1, 3, 5]`


#### 重复操作（`*`）
- 1 复操作符为 * ，后⾯常跟数字，表⽰将列表⾥⾯的元素重复复制⼏遍
```
l=[1,2,3]
print(l*2)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`[1, 2, 3, 1, 2, 3]`

#### 成员关系操作（ in和not in）
- 1 ⽤来判断元素是否在列表中，返回结果是布尔值，
```
l=[1,2,3,4]

print(5 not in l)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`True`


#### 列表的其他⽅法

|                              |                      |
| ---------------------------- | -------------------- |
| copy()                       | 浅拷贝                  |
| coumt(对象)                    | 返回对象在列表中出现的次数        |
| index(value,开始下标,结束下标)       | 元素出现的第一次下标位置，也可自定义范围 |
| reverse()                    | 原地翻转                 |
| sort(key=None,reverse=False) | 快速排序，默认从小到大排序，key:算法 |
| len()                        | 获取列表的长度(元素)          |

- 1 例如：将列表⾥⾯的所有元素进⾏翻转
```
l=[1,2,3,4]
l.reverse()

print(l)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`[4, 3, 2, 1]`

#### 冒泡排序法
- 1 例如:将列表`[5,4,3,2,1]`⾥⾯的所有元素⽤冒泡排序的思想进⾏从⼩到⼤排序
```python
l=[2,1,6,4,3]

for i in range(1,len(l)):
    for j in range(len(l)-i):
        if l[j]>l[j+1]:
            l[j],l[j+1]=l[j+1],l[j]

print(l)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`[1, 2, 3, 4, 6]`




#### 选择排序
- 1 让列表中的元素，固定⼀个元素和其他元素进⾏⽐较，不符合条件互换位置。
```python
l=[2,1,6,4,3]

for i in range(0,len(l)-1):
    for j in range(i+1,len(l)):
        if l[i]>l[j]:
            l[i],l[j]=l[j],l[i]
print(l)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`[1, 2, 3, 4, 6]`




#### ⼆维列表
```python
变量[外层列表下标][内层列表的下标]

例如输出⼆位列表中的第⼀个列表⾥⾯的下标为1的元素:
l=[[1,3,2],[3,2,1]]
print(l[0][1])
```

##### 对二维列表进⾏遍历
```python
l=[[1,3,2],[3,2,1]]

for i in l:
    for j in i:
        print(j)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`1
`3`
`2`
`3`
`2`
`1






### 7、


### 8、


## 元组
### 1 、可以⽤来存放任何数据类型
> 1. 不能修改，不可变类型 
> 2. 用（）的形式 
> 3. 元组也是可迭代对象 
> 4. 元组是有序的，下标操作,支持切面操作[:]

### 2 、元组的创建及访问
```python
1. 创建： 直接创建，例如 t = (1,2,3,4,5)
2. 访问： t[下标] #获取元素 
3. 切片操作： t[:] 返回元组

t=(1,2,3,4,5)

print(t[2])
n=t[0:4]
print(n)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`3`
`(1, 2, 3, 4)`


### 3 、修改和删除（list(),tuple(),del）
- 1 可以通过将元组转换成列表的形式进⾏修改和删除等操作，最后再将列表转换成元组，完成元组的修改和删除
```python
t=(1,2,3)
l=list(t)
l[2]=0
t=tuple(l)
print(t)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`(1, 2, 0)`

- 1 删除元组中的元素可⽤ `del t[下标] `⽅法，前提还是⼀样的先将元组转换成列表
```
t=(1,2,3)
l=list(t)
del l[2]
t=tuple(l)
print(t)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`(1, 2)`


### 4 、元组的操作符（⽅法跟列表的操作符是⼀样）
> 1. 比较运算符
> 	< > >= <= == !=
> 2. 逻辑运算符 
> 	`and not or `
> 3. 拼接运算符 
> 	+ 
> 4. 重复操作符
> 	`*` 
> 5. 成员关系操作符
> 	`in not in `

```
t=(1,2,3)
print(2 not in t)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`False`



### 5、元组的⽅法（和前⾯所介绍的列表的⽅法是⼀样的）
#### Python列表和元组函数和内置函数说明表

|序号|函数|说明|
|---|---|---|
|1|append(对象)|向列表中添加对象，并添加到末尾。|
|2|extend(可迭代对象)|将可迭代对象中的数据逐个添加到列表中，并添加到末尾。|
|3|insert(下标, 对象)|向列表的指定下标位置插入对象。|
|4|clear()|清空列表中的所有元素。|
|5|pop([下标])|删除下标指定的元素（如果不提供下标，则删除并返回最后一个元素）。|
|6|remove(对象)|删除列表中第一个匹配的指定对象。|
|7|del|删除变量或删除列表中指定下标的元素（例如：`del list[下标]`）。|
|8|copy()|创建并返回列表的浅拷贝。|
|9|count(对象)|返回对象在列表中出现的次数。|
|10|index(值, [开始下标, 结束下标])|返回元素第一次出现的下标位置（可指定搜索范围）。|
|11|reverse()|原地翻转列表中的元素顺序（修改原列表，不返回新列表）。|
|12|sort(key=None, reverse=False)|对列表进行原地排序（默认从小到大，可设置降序或自定义key函数）。|
|13|len()|获取列表的长度（元素个数）（注：`len()`是内置函数，用法如`len(list)`）。|



#### 还有2个⽅法值得新增：
```python
1. count(value) 统计某个值出现的次数，value是指定的值 
2. index(value,[start],[stop]) 返回value在元组中出现的下标位置（第一次出现的下标）

t=(1,2,3,4,5,3)

n1=t.count(3)
n2=t.index(4,0,6)

print(n1)
print(n2)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`2`
`3`




### 6、


### 7、


### 8、


## 字符串
### 1 、在Python中，字符和字符串没有区别


### 2 、字符串的特点
> 1. 字符串不可变类型
> 2. 字符串是可迭代对象
> 3. 字符串**支持索引和切片操作**
> 4. **支持操作符;**
>	拼接：+ 
> 	重复操作符：* 
> 	比较运算符： > < <= >= == != 
>	 逻辑运算符：not and or 
> 	成员关系： in not in

### 3 、字符串的⽅法
- 1 字符串的常⽤⽅法有以下这些：
#### 字符串方法说明表

| 序号  | 函数                                 | 说明                                      |
| --- | ---------------------------------- | --------------------------------------- |
| 1   | capitalize()                       | 把字符串的**首字符改为大写，其余字符转为小写**               |
| 2   | casefold()                         | 将整个字符串转为小写（支持 Unicode 特殊字符）             |
| 3   | encode(encoding='编码', errors='策略') | 将字符串编码为二进制数据（str → bytes）               |
| 4   | decode(encoding='编码', errors='策略') | 将二进制数据解码为字符串（bytes → str）               |
| 5   | count(sub[, start[, end]])         | 返回子字符串 sub 在字符串中出现的次数（可选范围：start 到 end） |
| 6   | find(sub[, start[, end]])          | 返回 sub 首次出现的下标，未找到返回 -1（可选范围）           |
| 7   | index(sub[, start[, end]])         | 返回 sub 首次出现的下标，未找到报错（可选范围）              |
| 8   | upper()                            | 将字符串中所有字符转为大写                           |
| 9   | lower()                            | 将字符串中所有字符转为小写                           |

- 1 例⼦：将字符串 “hello world” 的第⼀个字⺟⼤写
```python
a="hello word"
b=a.capitalize()
print(b)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`Hello word`



### 4 、格式化输出（format 和 $% ）（字符串按照某种格式进行输出）

#### Python中常用字符串格式化方法的对比总结

|方法类型|语法示例|特点说明|适用场景|
|---|---|---|---|
|​**​format() 方法​**​||||
|数字下标|`"{0} 嘿嘿".format("Python")`  <br>`s = "{0}{1}{2}".format(a,b,c)`|通过`{0}`、`{1}`等数字下标指定参数位置|需明确控制参数顺序|
|自动顺序|`"{}{}{} 嘿嘿".format(a, "JAVA", "C++")`|空花括号`{}`自动按顺序匹配参数|简单场景，无需命名参数|
|关键字参数|`"{a}{b}{c}".format(b="JAVA", a="C++", c="C#")`|通过`{a}`、`{b}`等命名占位符，参数顺序可自由调整|参数较多或需明确语义时|
|​**​% 格式化​**​||||
|`%s` 格式符|`"%s * %s = %s" % (i, j, i*j)`  <br>`"姓名: %s, 年龄: %d" % ("张三", 25)`|使用`%s`(字符串)、`%d`(整数)等格式符  <br>需用元组`(值1, 值2)`传递多个参数|兼容旧版Python，简洁的数值格式化|

#### format()方法讲解
##### 基础语法与参数传递
- 1 通过 `{}` 占位符标记插入位置，支持多种参数传递方式：
```python
1、按参数顺序填充：
"{} {}".format("A", "B")  # 输出 "A B" 

2、通过数字指定位置（可重复使用）：
"{1} before {0}".format("X", "Y")  # 输出 "Y before X" 

3、使用关键字提高可读性：
"{name} is {age} years old".format(name="Alice", age=30)  # 输出 "Alice is 30 years old" 

```

##### 二、数字格式化

通过 `:` 后接格式说明符控制数字显示：

|​**​需求​**​|​**​格式​**​|​**​示例​**​|​**​输出​**​|
|---|---|---|---|
|保留2位小数|`{:.2f}`|`"{:.2f}".format(3.14159)`|`3.14`|
|千分位分隔|`{:,}`|`"{:,}".format(1234567)`|`1,234,567`|
|百分比显示|`{:.2%}`|`"{:.2%}".format(0.4567)`|`45.67%`|
|十六进制|`{:x}`|`"{:x}".format(255)`|`ff`|
|科学计数法|`{:.2e}`|`"{:.2e}".format(123456)`|`1.23e+05`|


##### 🔤 三、字符串格式化

控制文本对齐、截断与填充：

| ​**​需求​**​ | ​**​格式​**​ | ​**​示例​**​                 | ​**​输出​**​     |
| ---------- | ---------- | -------------------------- | -------------- |
| 左对齐（宽度10）  | `{:<10}`   | `"{:<10}".format("Hi")`    | `"Hi "`        |
| 右对齐（宽度10）  | `{:>10}`   | `"{:>10}".format("Hi")`    | `" Hi"`        |
| 居中对齐（宽度10） | `{:^10}`   | `"{:^10}".format("Hi")`    | `" Hi "`       |
| 用 `*` 填充居中 | `{:*^10}`  | `"{:*^10}".format("Hi")`   | `"****Hi****"` |
| 截取前3个字符    | `{:.3}`    | `"{:.3}".format("Python")` | `"Pyt"`        |
|            |            |                            |                |

#### 例子讲解 - 用%s 结合循环语句输出九九乘法表
```python
4.%s
语法为 “%s”%（值） ，最常用的参数可以是任意值。

for i in range(1, 10):
    for j in range(1, i + 1):
        print("%s * %s = %s" % (i, j, i * j), end="\t")
    print()
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
1 * 1 = 1	
2 * 1 = 2	2 * 2 = 4	
3 * 1 = 3	3 * 2 = 6	3 * 3 = 9	
4 * 1 = 4	4 * 2 = 8	4 * 3 = 12	4 * 4 = 16	
5 * 1 = 5	5 * 2 = 10	5 * 3 = 15	5 * 4 = 20	5 * 5 = 25	
6 * 1 = 6	6 * 2 = 12	6 * 3 = 18	6 * 4 = 24	6 * 5 = 30	6 * 6 = 36	
7 * 1 = 7	7 * 2 = 14	7 * 3 = 21	7 * 4 = 28	7 * 5 = 35	7 * 6 = 42	7 * 7 = 49	
8 * 1 = 8	8 * 2 = 16	8 * 3 = 24	8 * 4 = 32	8 * 5 = 40	8 * 6 = 48	8 * 7 = 56	8 * 8 = 64	
9 * 1 = 9	9 * 2 = 18	9 * 3 = 27	9 * 4 = 36	9 * 5 = 45	9 * 6 = 54	9 * 7 = 63	9 * 8 = 72	9 * 9 = 81	







### 5、转义字符
```python
1. “\n” ：换行符
2. “\'”:单引号
3. “\“”:双引号
4. "\\" : \
```
- 1 值得注意的是 \\ 
```python
a="fhkfhk\
gdfgdggf\
djljdls"

print(a)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`fhkfhkgdfgdggfdjljdls`



### 6、



### 7、


### 8、

## 字典（dict）（存储数据）
### 1 、字典的特点
- 1 字典中的数据以映射关系存储。
> 1. 字典是Python中唯一的映射类型
> 2. 字典是无序的
> 3. 字典是可迭代对象
> 4. 字典的构成
>     键：key
>     值：value
>     映射：**键映射值**
>     键-值：键值对，又叫 项 


### 2 、创建字典
```python
1. 直接创建
d={"a":1,"b":2}
print(d)

2. dict(可迭代对象)
d=dict([("a",1),("b",2)])
d=dict(a=1,b=2)
```




### 3 、字典访问
```python
1.变量名[键名] #键所对应的值

d=dict(a=1,b=2)
print(d["a"])

2. 添加一个键值对
	变量名[键名]=值 
3. 修改一个键值对的值
	变量名[键名]=值
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`1`

### 4 、字典的⽅法
#### 📚 Python字典核心方法速查表

|​**​序号​**​|​**​函数/方法​**​|​**​说明​**​|​**​示例​**​|
|---|---|---|---|
|1|`clear()`|清空字典所有键值对，原字典变为空字典（原地操作，无返回值）|`d = {'a':1}; d.clear(); # {}`|
|2|`copy()`|返回字典的浅拷贝（只复制第一层，嵌套对象不复制）|`d1 = {'a': [1,2]}; d2 = d1.copy(); d2['a'].append(3); # d1['a']变为[1,2,3]`|
|3|`dict.fromkeys(iter, value=None)`|​**​类方法​**​：用可迭代对象中的元素作为键创建新字典，值统一为`value`（默认为`None`）|`keys = ['a','b']; d = dict.fromkeys(keys, 0); # {'a':0, 'b':0}`|
|4|`get(key[, default])`|安全获取键对应的值。若键不存在返回`default`（默认为`None`），避免`KeyError`|`d = {'a':1}; d.get('b', 0); # 0`|
|5|`items()`|返回字典键值对的动态视图（类集合对象），元素为`(key, value)`元组|`d = {'a':1}; list(d.items()); # [('a', 1)]`|
|6|`pop(key[, default])`|删除指定键的键值对并返回其值。键不存在时：若提供`default`则返回它，否则抛`KeyError`|`d = {'a':1}; d.pop('a'); # 1`|
|7|`popitem()`|删除并返回最后插入的键值对（Python 3.7+保证LIFO）。空字典调用会抛`KeyError`|`d = {'a':1}; d.popitem(); # ('a', 1)`|
|8|`values()`|返回字典所有值的动态视图（类集合对象）|`d = {'a':1}; list(d.values()); # [1]`|

- 1 例⼦：返回指定字典中的所有值
```python
d=dict(a=1,b=2)
c=d.values()

print(list(c))
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
>` [1, 2]`



### 5、补充（for循环、成员关系操作符）
```python
1. 字典可以使用for循环
    for i in d2:
        print(i) #键，不包含值
2. 输出一个键值对
    for i in d2.items():
        print(i)
3. 成员关系操作符
        in/not in
        只能查询键
```



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





# 二、函数

## 函数的基础知识
### 1 、创建和使⽤
```python
1.创建函数
def 函数名(参数): 
    代码块（函数的实现/函数体）

2.函数的调用
函数名(参数)

def fun(a,n):
	print(a*n)

fun("=",5)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
=====

- 2 参数可以为1个或者多个，用逗号隔开。




### 2 、函数的运行机制
```python
1. 从函数调用开始执行
2. 通过函数名字找到函数定义的位置（创建函数的位置）
3. 执行函数体
4. 执行完毕之后，返回到函数的调用处
```

### 3 、函数的特点
```python
1. 避免了代码的冗余
2. 提高了代码的可维护性
3. 提高了代码的可重用性
4. 提高了代码的灵活性
```

### 4 、函数的参数
```python
1. 形式参数：形参
        在定义函数的时候传递的参数
2. 实际参数：实参    
        在调用函数时传递的参数
3. 无参
        没有任何参数
4. 位置参数：
    实参的位置和形参一一对应，不能多也不能少

```

```python
5.关键字参数：
    用形参的名字作为关键字来指定具体传递的值，则在函数调用时，前后顺序将不受影响。

def fun(a,n):
	print(a*n)

fun(n=5,a="=")
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
=====


```python
6.位置参数和关键字参数混用：
    当位置参数和关键字参数混用时，位置参数在前

def fun(a,n):
	print(a*n)

fun("=",n=5)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
=====

```python
7.默认参数：
    给了默认值的参数--形参
    如果传递了新的值，那么默认值就被覆盖了

def fun(a=10,b=20,c=30):
    print(a,b,c)

fun()
fun(20,30,10)
fun(30,b=10,c=20)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`10 20 30
`20 30 10`
`30 10 20`


```python
8.可变成参数：
    def 函数名(*a)
    本质上封装成了元组

    def 函数名(**kwargs)
        将参数封装成了字典

def fun(*b):
	print(b)

def fun1(**b):
	print(b)

fun(10,20,30)
fun1(a=10,b=20,c=30)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`(10, 20, 30)`
`{'a': 10, 'b': 20, 'c': 30}`


- 1 可变成参数和位置参数混用的时候：可变参数优先
```python
def fun(b,*a):
    print(a,b)

fun(10,20,30)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`(20, 30) 10`



### 5、函数的文档


- 2 在函数体的第一行用 “”" “”" 进行文档说明


- 1 获取函数的文档内容
```python
def fun(b,*a):
    """
    :param b: 位置参数
    :param a: 可变参数
    :return:
    """
    print(a,b)


fun(10,20,30)
print(fun.__doc__)

help(fun)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
> (20, 30) 10
> 
>     :param b: 位置参数
>     :param a: 可变参数
>     :return:
Help on function fun in module __main__:
> 
> fun(b, * a)
>     :param b: 位置参数
>     :param a: 可变参数
>     :return:





### 6、函数的返回值
```python
关键字：return
返回值谁调用就返回给谁
1. 任何函数都有返回值
2. 如果不写return ，也会默认加一个return None
3. 如果写return ，不写返回值 也会默认加一个None
4. 可以返回任何数据类型
5. return后面的代码不在执行，代表着函数的结束
```


### 7、函数的变量的作用域
```python
1. 局部变量
        定义在函数内部的变量
        先赋值在使用
        从定义开始到包含他的代码结束
        在外部无法访问
2. 全局变量
        1. 定义在源文件的开头
        2. 作用范围：整个文件
        3. 局部变量和全局变量发生命名冲突时，以局部变量优先
       
3.global
        声明全局变量
4.nonlocal
    声明的是局部变量

def fun():
    """
    :param b: 位置参数
    :param a: 可变参数
    :return:
    """
    b=100
    def fun1():
        # 声明后，才能同步更改fun函数的变量b的值。
        nonlocal b
        b=200
        print(b)

    fun1()
    print(b)


fun()
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`200`
`200`

- 2 `nonlocal`关键字只能用于嵌套函数内部，引用外层（非全局）作用域中的变量。

### 8、内嵌函数
- 1 内部函数的作⽤范围：从定义开始到包含给他的代码块结束
- 2 在内部函数中不能进⾏a+=1,a=a+1这样的操作，解决 ⽅案是nonlocal 和global。

```python
def fun():
    """
    :param b: 位置参数
    :param a: 可变参数
    :return:
    """
    b=100
    def fun1():
        # 声明后，才能同步更改fun函数的变量b的值。
        nonlocal b
        b=b+1
        print(b)

    fun1()
    print(b)

fun()
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`101`
`101`


### 9、闭包
> 编程范式：⼀种编程范式，对代码进⾏提炼和抽象概括，使得重⽤性更⾼

> 如果**内部函数调⽤了外部函数的局部变量，并外部函数返回内部函数的函数对象** （函数名）。
> 这就形成了闭包，闭包的作⽤是可以传递更少的形参，可以传递更多的实参—更加安全，间接性的访问内部函数，例如：

```python
def fun(b):

    print(b)
    def fun1(c):

        print(c)
        return "ming"

    return fun1

print(fun(200)(300))
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`200`
`300`
`ming`

#### 闭包是有条件的：
> 1. 必须是一个**内嵌函数** 
> 2. **外部函数必须返回内部函数的函数对象** 
> 3. 内部函数必须使用外部函数的局部变量



### 10、 lambda表达式
```python
1. 匿名函数
        没有名字的函数
2. 使用时机：
        只使用一次的时候
3. 语法：
        关键字： lambda
        lambda 参数1，参数2:返回值
4. lambda的书写形式更加的简洁，优雅
        l = lambda x:x
        print(l(100))
5. lambda的优先级最低

```
- 2 ​**​无命名函数​**​，仅用于简化单次调用的场景，避免`def`定义的开销



### 11、






## 自带函数的使用
### 1 、print() （输出内容）
```
print(要输出的内容)
```

```python
print("ming")
```
- 1 字符串，需要加上" "才是正确的格式

#### `end` 参数
- 1 语法结构​​：`print(value, end="str")`

> - `value`：需输出的内容（变量 `i` 或其他对象）。
> - `end="str"`：`str` 可为任意字符串：
>     - `end=""`：无后缀，**直接拼接后续输出**
>     - `end=","`：以逗号结尾（如 `0,1,2,`）。
>     - `end="\t"`：用制表符分隔







### 2 、 input()（接收⽤⼾输⼊）
```python
input（输出的内容）
```


```python
n = input("请输入密码：") #把输入内容赋给n，用 n 接收一下
print(n) 
```
- 1 成功接收⽤⼾输⼊的内容并打印出来。

### 3 、type(对象)  （返回对象的类型）
```python
f=11
print(type(f))
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
<class 'int'>
进程已结束,退出代码0



### 4 、isinstance(对象,class) （判断数据类型）
```python
f=11
n=isinstance(f,int)
print(n)
```
> /home/topeet/miniconda3/envs/rknn/bin/python3 /home/topeet/test/python/test.py 
`True`

### 5、`range(start, stop, step)`
#### **参数规则​**​

|​**​参数​**​|​**​说明​**​|​**​默认值​**​|​**​约束​**​|
|---|---|---|---|
|`start`|序列起始值（包含）|`0`|整数类型|
|`stop`|序列终止值（不包含）|必填|整数类型|
|`step`|步长（相邻元素差值）|`1`|非零整数|

> - ​**​步长为负时​**​：需满足 `start > stop`，否则返回空序列
> - ​**​步长为 0​**​：触发 `ValueError`
> 

```python
list(range(1, 10, 2))   # [1, 3, 5, 7, 9]（正步长）[3](@ref)
list(range(10, 0, -2))  # [10, 8, 6, 4, 2]（负步长）[5,10](@ref)
```



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


# 三、综合性练手项目

## 名⽚管理系统（未）
### 1 、系统需求
- 1 1.程序启动，显示名片管理系统欢迎界面，并显示功能菜单

```python
**************************************************
欢迎使用【名片管理系统】V1.0

1. 新建名片
2. 显示全部
3. 查询名片

4. 退出系统
**************************************************

```

> 2.用户用数字选择不同的功能  
3.根据功能选择，执行不同的功能  
4.用户名片需要记录用户的 姓名、电话、QQ、邮件  
5.如果查询到指定的名片，用户可以选择 修改 或者 删除 名片



### 2 、效果预览
- 1 视频演示的链接
[Python练手项目之名片管理系统演示\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV1aZ4y1F7n6/?vd_source=83485b71343f442522d28357f4bb93eb)



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


