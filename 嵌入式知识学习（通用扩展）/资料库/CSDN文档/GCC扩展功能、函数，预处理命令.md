---
title: "GCC扩展功能、函数，预处理命令"
source: "https://blog.csdn.net/surfaceyan/article/details/139940255?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_utm_term~default-1-139940255-blog-49944429.235^v43^pc_blog_bottom_relevance_base8&spm=1001.2101.3001.4242.1&utm_relevant_index=4"
author:
  - "[[surfaceyan]]"
published: 2024-07-07
created: 2025-08-11
description: "文章浏览阅读1.5k次，点赞26次，收藏24次。GCC（GNU Compiler Collection）提供了许多扩展功能，这些功能在标准C和C++中没有定义，但可以提高代码的效率和可移植性。__LINE__ // int #line num 会重置该值。_gcc扩展语法"
tags:
  - "clippings"
---
---

## 前言

[GCC](https://so.csdn.net/so/search?q=GCC&spm=1001.2101.3001.7020) （GNU Compiler Collection）提供了许多扩展功能，这些功能在标准C和C++中没有定义，但可以提高代码的效率和可移植性。

---

## 一、GCC C语言扩展

- 128位的整数
	```c
	_int128 i_128;
	unsigned _int128 ui_128;
	c12
	```
- [线程私有变量](https://so.csdn.net/so/search?q=%E7%BA%BF%E7%A8%8B%E7%A7%81%E6%9C%89%E5%8F%98%E9%87%8F&spm=1001.2101.3001.7020) Thread-local storage (TLS)
	```c
	// 每个线程会有自己独立的变量a
	__thread static int a = 9;
	// C++11及之后
	std::thread_local
	c12345
	```
- 零长度数组
	```c
	// 可用于定义协议头等
	typedef struct line{
	  int length;
	  char contents[0];
	} line;
	line* l = (line*)malloc(sizeof(line) + 100)
	l->contents[99];
	c1234567
	```
- 具有可变参数的宏
	```c
	#define debug1(format, ...) fprintf (stderr, format, __VA_ARGS__)     // debug1("abc") is invalid
	#define debug2(format, args...) fprintf (stderr, format, args)        // debug2("abc") is invalid
	#define debug3(format, ...) fprintf (stderr, format, ## __VA_ARGS__)  // debug3("abc") is valid
	c123
	```
- struct和数组指定初始化
	```c
	int a[6] = { [4] = 29, [2] = 15 };//{ 0, 0, 15, 0, 29, 0 };
	int widths[] = { [0 ... 9] = 1, [10 ... 99] = 2, [100] = 3 };
	struct point p = { .y = yvalue, .x = xvalue };
	c123
	```
- 范围case
	```c
	case 'A' ... 'Z':
	case 1 ... 5:
	c12
	```

### 声明函数属性

[GNU](https://so.csdn.net/so/search?q=GNU&spm=1001.2101.3001.7020) C/C++  
在函数声明处添加形如：，指定函数属性  
\_\_attribute\_\_((xxx))

- alias(“target”)  
	alias属性导致声明作为另一个符号的别名发出
	```c
	void __f () { /* Do something. */; }
	void f () __attribute__ ((weak, alias ("__f")));
	c12
	```
- aligned (alignment)  
	对齐属性指定函数的第一条指令的最小对齐，以字节为单位, alignment必须是 an integer constant power of 2
- constructor destructor constructor(priority) destructor(priority)  
	constructor属性会使得函数在main()之前执行；deconstructor会使得函数在main()之后或exit()之后执行，constructor priority数值越小优先级越高，deconstructor与之相反。  
	另外，c++的静态对象和constructor属性的函数的顺序不确定？
- 函数弃用报警，deprecated
	```c
	__attribute__((deprecated("this function will removed in the future, please use xx instand"))) void old_fun();
	c1
	```
- noreturn
	```c
	void fatal () __attribute__ ((noreturn));
	void
	fatal (/* … */)
	{
	  /* … */ /* Print error message. */ /* … */
	  exit (1);
	}
	c12345678
	```
- section (“section-name”)  
	默认情况下，编译器将其生成的代码放在text section。有时你需要额外的sections，将函数放置在某个sections中，section属性正是用来做这件事的
	```c
	extern void foobar (void) __attribute__ ((section ("bar")));
	c1
	```
- visibility (“visibility\_type”)  
	该属性影响链接时该函数是否可见。  
	四种类型：default, hidden, protected or internal visibility
	- default  
		默认可见性。可被其他模块、共享库可见，也意味着声明实体被覆盖。在语言中对应“外部链接”。
	- hidden  
		模块外部不可见

### 变量属性

- section (“section-name”)  
	默认情况下，编译器将对象放在data section或bss section。
	```c
	struct duart a __attribute__ ((section ("DUART_A"))) = { 0 };
	struct duart b __attribute__ ((section ("DUART_B"))) = { 0 };
	char stack[10000] __attribute__ ((section ("STACK"))) = { 0 };
	int init_data __attribute__ ((section ("INITDATA")));
	main()
	{
	  /* Initialize stack pointer */
	  init_sp (stack + sizeof (stack));
	  /* Initialize initialized data */
	  memcpy (&init_data, &data, &edata - &data);
	  /* Turn on the serial ports */
	  init_duart (&a);
	  init_duart (&b);
	}
	c1234567891011121314151617
	```
	未初始化的变量放在common(or bss) section。使用section属性会更改变量进入的部分，如果未初始化的变量有多个定义，则可能导致链接器发出错误。可以使用-fno公共标志或nocommon属性强制初始化变量。
- visibility (“visibility\_type”)  
	详细定义见 **声明函数属性**
- aligned (alignment)  
	alignment=power(2, x)
	```c
	struct __attribute__ ((aligned (8))) S { short f[3]; };
	typedef int more_aligned_int __attribute__ ((aligned (8)));
	c12
	```

### 内敛汇编

。GCC提供李彤两种格式的内嵌汇编。1.基础形式，没有operands 2.扩展形式，有operands

- asm asm-qualifiers ( AssemblerInstructions )
	```c
	/* Note that this code will not compile with -masm=intel */
	#define DebugBreak() asm("int $3")
	c12
	```
```c
asm asm-qualifiers ( AssemblerTemplate 
                 : OutputOperands 
                 [ : InputOperands
                 [ : Clobbers ] ])

asm asm-qualifiers ( AssemblerTemplate 
                      : OutputOperands
                      : InputOperands
                      : Clobbers
                      : GotoLabels)
12345678910
```
```c
int src = 1;
int dst;   

asm ("mov %1, %0\n\t"
    "add $1, %0"
    : "=r" (dst) 
    : "r" (src));

printf("%d\n", dst);
c123456789
```

### 与原子操作相关的内建函数

#### 内存模型感知原子操作的内置函数

  以下内建函数基本匹配了C++11内存模型的需求。它们都是以“\_\_atomic”为前缀进行标识的，大多数都是重载的，因此可以与多种类型一起使用。  
  这些函数意在代替 `__sync` 。它们的主要不同为，内存序是作为函数的参数。  
  注意到， `__atomic` 假设程序遵守C++11内存模型。尤其是程序是自由数据竞争的。详见C++11标准。  
`__atomic` 可被用于1，2，4，8字节的任意整数，16字节类型的整数 `__nt28` 也是支持的。  
  四个非算数运算函数(load, store, exchage, compare\_exchange)也都有通用版本。通用版本工作在任意数据类型上。它使用lock-free内建函数，否则，外部调用将在运行时解决。此外部调用的格式与添加的“size\_t”参数相同，该参数作为指示所指向对象大小的第一个参数插入。所有对象的大小必须相同。

有6中内存序，和C++11中的内存模型对应。一个原子操作能够同时限制code motion和 映射到在线程之间同步的硬件指令。这种情况发生的程度受内存序的控制，这些顺序在这里以强度的近似升序列出。precise semantics见C++11内存模型。

1. `__ATOMIC_RELAXED`  
	暗示没有内部线程顺序限制。如果某个原子操作使用 relaxed 作为其 memory order，那么这个原子操作将退化为一个单纯的原子操作，不再具有线程同步节点的作用。
2. `__ATOMIC_CONSUME`
3. `__ATOMIC_ACQUIRE`
4. `__ATOMIC_RELEASE`
5. `__ATOMIC_ACQ_REL`
6. `__ATOMIC_SEQ_CST`
```c
// 返回 *ptr 的值
type __atomic_load_n (type *ptr, int memorder)

// atomic load的通用版本，将*ptr的值加载进*ret
void __atomic_load (type *ptr, type *ret, int memorder)

// 将val写入*ptr
void __atomic_store_n (type *ptr, type val, int memorder)

// 通用版本，将*val写入*ptr
void __atomic_store (type *ptr, type *val, int memorder)

// 原子交换操作，先返回*ptr的值，再将val写入*ptr
type __atomic_exchange_n (type *ptr, type val, int memorder)

// 通用版本，*ret=*ptr, *ptr=*val
void __atomic_exchange (type *ptr, type *val, type *ret, int memorder)

// 类似：{ *ptr op= val; return *ptr; }
// { *ptr = ~(*ptr & val); return *ptr; } // nand
// ptr指向的type对象必须是 整数或者指针类型，不能是布尔类型，支持所有内存模型
Built-in Function: type __atomic_add_fetch (type *ptr, type val, int memorder)
Built-in Function: type __atomic_sub_fetch (type *ptr, type val, int memorder)
Built-in Function: type __atomic_and_fetch (type *ptr, type val, int memorder)
Built-in Function: type __atomic_xor_fetch (type *ptr, type val, int memorder)
Built-in Function: type __atomic_or_fetch (type *ptr, type val, int memorder)
Built-in Function: type __atomic_nand_fetch (type *ptr, type val, int memorder)

// 类似：{ tmp = *ptr; *ptr op= val; return tmp; }
// { tmp = *ptr; *ptr = ~(*ptr & val); return tmp; } // nand
Built-in Function: type __atomic_fetch_add (type *ptr, type val, int memorder)
Built-in Function: type __atomic_fetch_sub (type *ptr, type val, int memorder)
Built-in Function: type __atomic_fetch_and (type *ptr, type val, int memorder)
Built-in Function: type __atomic_fetch_xor (type *ptr, type val, int memorder)
Built-in Function: type __atomic_fetch_or (type *ptr, type val, int memorder)
Built-in Function: type __atomic_fetch_nand (type *ptr, type val, int memorder)

// 先测试*(char*)ptr是否非空。再将其置为非空，最后返回先前的值。 ptr应当指向bool或者bool类型
bool __atomic_test_and_set (void *ptr, int memorder)

// 原子清除*ptr, *ptr=0, ptr应当指向bool或char类型
void __atomic_clear (bool *ptr, int memorder)

//  acts as a synchronization fence between threads based on the specified memory order.
void __atomic_thread_fence (int memorder)

// acts as a synchronization fence between a thread and signal handlers based in the same thread.
void __atomic_signal_fence (int memorder)

// ???
bool __atomic_always_lock_free (size_t size, void *ptr)
// ???
bool __atomic_is_lock_free (size_t size, void *ptr)

c123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354
```

#### 使用溢出检查执行算术的内置函数

以下内置函数允许执行简单的算术运算，同时检查运算是否溢出。

```c
bool __builtin_add_overflow (type1 a, type2 b, type3 *res)
bool __builtin_sadd_overflow (int a, int b, int *res)
bool __builtin_saddl_overflow (long int a, long int b, long int *res)
bool __builtin_saddll_overflow (long long int a, long long int b, long long int *res)
bool __builtin_uadd_overflow (unsigned int a, unsigned int b, unsigned int *res)
bool __builtin_uaddl_overflow (unsigned long int a, unsigned long int b, unsigned long int *res)
bool __builtin_uaddll_overflow (unsigned long long int a, unsigned long long int b, unsigned long long int *res)

Built-in Function: bool __builtin_sub_overflow (type1 a, type2 b, type3 *res)
Built-in Function: bool __builtin_ssub_overflow (int a, int b, int *res)
Built-in Function: bool __builtin_ssubl_overflow (long int a, long int b, long int *res)
Built-in Function: bool __builtin_ssubll_overflow (long long int a, long long int b, long long int *res)
Built-in Function: bool __builtin_usub_overflow (unsigned int a, unsigned int b, unsigned int *res)
Built-in Function: bool __builtin_usubl_overflow (unsigned long int a, unsigned long int b, unsigned long int *res)
Built-in Function: bool __builtin_usubll_overflow (unsigned long long int a, unsigned long long int b, unsigned long long int *res)

Built-in Function: bool __builtin_mul_overflow (type1 a, type2 b, type3 *res)
Built-in Function: bool __builtin_smul_overflow (int a, int b, int *res)
Built-in Function: bool __builtin_smull_overflow (long int a, long int b, long int *res)
Built-in Function: bool __builtin_smulll_overflow (long long int a, long long int b, long long int *res)
Built-in Function: bool __builtin_umul_overflow (unsigned int a, unsigned int b, unsigned int *res)
Built-in Function: bool __builtin_umull_overflow (unsigned long int a, unsigned long int b, unsigned long int *res)
Built-in Function: bool __builtin_umulll_overflow (unsigned long long int a, unsigned long long int b, unsigned long long int *res)
c1234567891011121314151617181920212223
```

以下函数与 `__builtin_add_overflow, __builtin_sub_overflow, or __builtin_mul_overflow` 相似，除了，它们不存储运算结果。

```c
bool __builtin_add_overflow_p (type1 a, type2 b, type3 c)
bool __builtin_sub_overflow_p (type1 a, type2 b, type3 c)
bool __builtin_mul_overflow_p (type1 a, type2 b, type3 c)
c123
```

例如，以下宏可用于在编译时便携式检查添加两个常量整数是否会溢出，并仅在已知安全且不会触发-Woverflow警告的情况下执行添加。

```c
#define INT_ADD_OVERFLOW_P(a, b) \
   __builtin_add_overflow_p (a, b, (__typeof__ ((a) + (b))) 0)

enum {
    A = INT_MAX, B = 3,
    C = INT_ADD_OVERFLOW_P (A, B) ? 0 : A + B,
    D = __builtin_add_overflow_p (1, SCHAR_MAX, (signed char) 0)
};
c12345678
```

### \- xxx

- 函数名作为字符串  
	GCC提供三个magic constants用以持有当前函数名的字符串

```c
extern "C" int printf (const char *, ...);

class a {
 public:
  void sub (int i)
    {
      printf ("__FUNCTION__ = %s\n", __FUNCTION__);
      printf ("__PRETTY_FUNCTION__ = %s\n", __PRETTY_FUNCTION__);
    }
};

int
main (void)
{
  a ax;
  ax.sub (0);
  return 0;
}
c123456789101112131415161718
```
- 获取函数的返回地址或帧地址  
	void \* \_\_builtin\_return\_address (unsigned int level)

## 二、GCC C++语言扩展

### interface和 pragmas

`#pragma para `

[https://www.cnblogs.com/zhoug2020/p/6616942.html](https://www.cnblogs.com/zhoug2020/p/6616942.html)  
[https://gcc.gnu.org/onlinedocs/gcc-11.4.0/gcc/C\_002b\_002b-Interface.html](https://gcc.gnu.org/onlinedocs/gcc-11.4.0/gcc/C_002b_002b-Interface.html)

### Template

C++ 是 language feature

## 二、预处理过程及其指令

### 预处理过程

#### 1\. 字符集转换

将文件转换为用于内部处理的字符集。

#### 2\. Initial processing

执行一系列文本转换。

1. 读取文件到内存并分行  
	GCC将LF, CR LF 和 CR作为行结束标识。  
	The C standard says that this condition provokes undefined behavior, so GCC will emit a warning message.似乎并没有警告
2. 三字符转换(添加 -trigraphs 选项)（默认 -Wtrigraphs）
	```c
	Trigraph:       ??(  ??)  ??<  ??>  ??=  ??/  ??'  ??!  ??-
	Replacement:      [    ]    {    }    #    \    ^    |    ~
	c12
	```
3. 连续行合并  
	以为 `\` 结尾的行与下一行合并。  
	`\` 和\`换行符之间不能有任何空格，否则预处理器会报错
4. 所有注释替换为单个空格
```c
/\
*
*/ # /*
*/ defi\
ne FO\
O 10\
20
1234567
```

#### 3\. token化和

```c
#define foo() bar
foo()baz
     → bar baz
not
     → barbaz
    
a+++++b
    → a ++ ++ + b
12345678
```

预处理标记分为五大类：标识符、预处理数字、字符串文字、标点符号和 其他 。标识符与C中的标识符相同：任何以字母或下划线开头的字母、数字或下划线序列。C的关键字对预处理器没有意义；它们是普通的标识符。例如，可以定义名称为关键字的宏。定义了可以被视为预处理关键字的唯一标识符。

#### 4\. 预处理语言

token化后，tokens流可能会被直接传输给 compiler’s parser。然后，如果包含预处理语言，则会先进行转换。这是大多数人认为的预处理器的工作。

预处理语言由要执行的指令和要扩展的宏组成。：

- 包含头文件。这些是可以替换到程序中的声明文件。
- 宏展开。您可以定义宏，宏是C代码任意片段的缩写。预处理器将在整个程序中用宏的定义替换宏。某些宏是自动为您定义的。
- 条件编译。您可以根据各种条件包括或排除程序的各个部分。
- 线路控制。如果使用程序将源文件组合或重新排列为中间文件，然后进行编译，则可以使用行控制来通知编译器每个源行的原始来源。
- 诊断。您可以在编译时检测问题并发出错误或警告。

### 头文件

```c
#include <file>  // 除comment之外的所有字符都是非法的
1
```

用于系统头文件。在系统目录的标准列表中搜索该文件。可以使用 `-I` 选项将目录前置到此列表中 。

```c
#include "file" 
1
```

此变体用于您自己程序的头文件。它首先在包含当前文件的目录中搜索名为file的文件，然后在引号目录中搜索，然后在用于＜file＞的相同目录中搜索。您可以使用 `-iquote` 选项将目录前置到引号目录列表中。  
  
header.h

```c
#include "header.h"
// 无限include
c12
```

**搜索路径：**  
如果/a/b/c.h中包含#include"h1.h"则GCC首先会从/a/b/目录下搜索h1.h

standard system directories

```c
cpp -v /dev/null -o /dev/null
1
```

### 宏命令

```c
#define X 1
#undef
c12
```

带宏参数

```c
#define WARN_IF(EXP) \
do { if (EXP) \
        fprintf (stderr, "Warning: " #EXP "\n"); } \
while (0)
WARN_IF (x == 0);
     → do { if (x == 0)
           fprintf (stderr, "Warning: " "x == 0" "\n"); } while (0);
c1234567
```

字符串化

```c
#define xstr(s) str(s)
#define str(s) #s
#define foo 4
str (foo)
     → "foo"
xstr (foo)
     → xstr (4)
     → str (4)
     → "4"
c123456789
```

连接

```c
#define COMMAND(NAME)  { #NAME, NAME ## _command }

struct command commands[] =
{
  COMMAND (quit),
  COMMAND (help),
  …
};

    ->
        struct command commands[] =
        {
          { "quit", quit_command },
          { "help", help_command },
          …
        };

c1234567891011121314151617
```

**具有可变参数的宏**

#### 标准预定义宏

```c
__FILE__  // string
__LINE__  //  int  #line num 会重置该值
__func__  // string
__DATE__  // string compile time
__TIME__  // string compile time

__cplusplus  // C++ language macro
c1234567
```

#### comman predefined macros

[https://gcc.gnu.org/onlinedocs/cpp/Common-Predefined-Macros.html](https://gcc.gnu.org/onlinedocs/cpp/Common-Predefined-Macros.html)

### 条件

```c
#ifdef MACRO

controlled text

#endif /* MACRO */
12345
```
```c
#if expression
    controlled text
#endif /* expression */

#if expression
    text-if-true
#else /* Not expression */
    text-if-false
#endif /* Not expression */

#if X == 1
    …
#elif X == 2
    …
#else /* X != 2 and X != 1*/
    …
#endif /* X != 2 and X != 1*/
1234567891011121314151617
```
```c
#if defined (__vax__) || defined (__ns16000__)
1
```
```c
#ifdef __vax__
#error "Won't work on VAXen.  See comments at get_last_object."
#endif

#if !defined(FOO) && defined(BAR)
#error "BAR requires FOO."
#endif
1234567
```

### xx

```c
_Pragma ("GCC dependency \"parse.y\"")

#define DO_PRAGMA(x) _Pragma (#x)
DO_PRAGMA (GCC dependency "parse.y")

c12345
```

如果某个头文件中有 `#pragma once` ，该文件只会在C文件中出现一次  
`#gragma pack(<opt:pow(2, x>)` 指定后续结构体内存对齐的字节数

## experiment

spin lock, sleep lock

```cpp
#include <unistd.h>
#include <stdio.h>
#include <iostream>
#include <thread>

using namespace std;

int a;
unsigned char atomic_int = 0;

void* call_fun(void*)
{
    
    for (size_t i = 0; i < 100000; i++)
    {
        while (__atomic_exchange_n(&atomic_int, 1, __ATOMIC_RELAXED) != 0)
        {
            sched_yield();  // sleep lock if true
        }
        
        ++a;
        usleep(1);
        // std::cout << "this is a:" << a << " endl" << std::endl;

        __atomic_clear(&atomic_int, __ATOMIC_RELAXED);
    }
    return NULL;
}

class spin_lock
{
private:
    unsigned char atom_char;
public:
    spin_lock(/* args */): atom_char(0) {}
    ~spin_lock() {}
    void lock()
    {
        while (__atomic_exchange_n(&atom_char, 1, __ATOMIC_RELAXED) != 0);
    }
    void unlock()
    {
        __atomic_clear(&atom_char, __ATOMIC_RELAXED);
    }
};

class sleep_lock
{
private:
    spin_lock sp_lock;
    unsigned char locked;
public:
    sleep_lock(/* args */): locked(0) {}
    ~sleep_lock() {}
    void lock()
    {
        sp_lock.lock();
        while (locked)
        {
            sp_lock.unlock();
            sched_yield();
            sp_lock.lock();
        }
        locked = 1;
        sp_lock.unlock();        
    }
    void unlock()
    {
        sp_lock.lock();
        locked = 0;
        sp_lock.unlock();
    }
};

class direct_sleep_lock
{
private:
    unsigned char atom_char;
public:
    direct_sleep_lock(/* args */): atom_char(0) {}
    ~direct_sleep_lock() {}
    void lock()
    {
        while (__atomic_exchange_n(&atom_char, 1, __ATOMIC_RELAXED) != 0)
        {
            sched_yield();
        }
    }
    void unlock()
    {
        __atomic_clear(&atom_char, __ATOMIC_RELAXED);
    }
};

direct_sleep_lock lock;
void* call_fun2(void*)
{
    for (size_t i = 0; i < 100000; i++)
    {
        lock.lock();
        ++a;
        usleep(1);
        lock.unlock();
    }
    return NULL;
}

int main()
{
    pthread_t ths[5];
    for (size_t i = 0; i < sizeof(ths)/sizeof(ths[0]); i++)
    {
        pthread_create(ths+i, NULL, call_fun2, NULL);
    }
    for (size_t i = 0; i < sizeof(ths)/sizeof(ths[0]); i++)
    {
        pthread_join(ths[i], NULL);
    }

    printf(".....a = %d\n", a);

}
cpp123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123
```

## 原子操作与内存序

```c
std::atomic<int> a;
std::atomic<int> b;
int x = 0;
int y = 0;

int main()
{
  std::thread th1([&]{ a.store(1); x = b.load(); });
  std::thread th2([&]{ b.store(1); y = a.load(); });
  th1.join(); th2.join();
}
1234567891011
```
```cpp
x.load(std::memory_order_aqcquire);
x.store(1, std::memory_order_release);
x.fetch_add(1, std::memory_order_acq_rel);
cpp123
```

---

## reference

在线文档： [https://gcc.gnu.org/onlinedocs/](https://gcc.gnu.org/onlinedocs/)

C++11内存模型： [https://www.cnblogs.com/dream397/p/17763965.html](https://www.cnblogs.com/dream397/p/17763965.html)

preprocesser [https://gcc.gnu.org/onlinedocs/cpp/](https://gcc.gnu.org/onlinedocs/cpp/)

内容来源：csdn.net

作者昵称：耶耶耶耶耶~

原文链接：https://blog.csdn.net/surfaceyan/article/details/139940255

作者主页：https://blog.csdn.net/surfaceyan

实付 元

[使用余额支付](https://blog.csdn.net/surfaceyan/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

[AI 搜索](https://ai.csdn.net/?utm_source=cknow_pc_blog_right_hover) [智能体](https://ai.csdn.net/cmd?utm_source=cknow_pc_blog_right_hover) [AI 编程](https://ai.csdn.net/coding?utm_source=cknow_pc_blog_right_hover) [AI 作业助手](https://ai.csdn.net/homework?utm_source=cknow_pc_blog_right_hover)

隐藏侧栏 ![程序员都在用的中文IT技术交流社区](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_app.png)

程序员都在用的中文IT技术交流社区

![专业的中文 IT 技术社区，与千万技术人共成长](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_wechat.png)

专业的中文 IT 技术社区，与千万技术人共成长

![关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_video.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部