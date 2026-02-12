---
title: "GCC高级特性详解-CSDN博客"
source: "https://blog.csdn.net/u013920085/article/details/49944429?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522622441bc91264a2da2de7e395647e851%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=622441bc91264a2da2de7e395647e851&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-2-49944429-null-null.142^v102^pc_search_result_base4&utm_term=gcc%E6%89%A9%E5%B1%95%E8%AF%AD%E6%B3%95%E3%80%82&spm=1018.2226.3001.4187"
author:
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
published:
created: 2025-08-11
description: "文章浏览阅读1.5k次。1.对齐 __alignof__操作符返回数据类型或指定数据项的分界对齐(boundary alignment). 如: __alignof__(long long); The keyword `__alignof__' allows you to inquire about how an object is aligned, or the minimum alignment us_gcc 扩展语法"
tags:
  - "clippings"
---
1.对齐  
\_\_alignof\_\_操作符返回数据类型或指定数据项的分界对齐(boundary alignment).  
如: \_\_alignof\_\_(long long);  
  
The keyword \`\_\_alignof\_\_' allows you to inquire about how an object is aligned, or the minimum alignment usually required by a type. Its syntax is just like \`sizeof'.

For example, if the target machine requires a \`double' value to be aligned on an 8-byte boundary, then \`\_\_alignof\_\_ (double)' is 8. This is true on many RISC machines. On more traditional machine designs, \`\_\_alignof\_\_ (double)' is 4 or even 2.

Some machines never actually require alignment; they allow reference to any data type even at an odd addresses. For these machines, \`\_\_alignof\_\_' reports the \_recommended\_ alignment of a type.

If the operand of \`\_\_alignof\_\_' is an lvalue rather than a type, its value is the required alignment for its type, taking into account any minimum alignment specified with [GCC](https://so.csdn.net/so/search?q=GCC&spm=1001.2101.3001.7020) 's \`\_\_attribute\_\_' extension (\*note Variable Attributes::). For example, after this declaration:

struct foo { int x; char y; } foo1;

the value of \`\_\_alignof\_\_ (foo1.y)' is 1, even though its actual alignment is probably 2 or 4, the same as \`\_\_alignof\_\_ (int)'.

It is an error to ask for the alignment of an incomplete type.

  
  
2.匿名联合  
在结构中，可以声明某个联合而不是指出名字，这样可以直接使用联合的成员，就好像它们  
是结构中的成员一样。  
例如：  
struct {  
char code;  
union {  
chid\[4\];  
int unmid;  
};  
char\* name;  
} morx;  
可以使用morx.code, morx.chid, morx.numid和morx.name访问;  
  
3.变长数组  
数组的大小可以为动态值，在运行时指定尺寸.  
例如：  
void add\_str(const char\* str1, const char\* str2)  
{  
char out\_str\[strlen(str1)+strlen(str2)+2\];  
  
strcpy(out\_str, str1);  
strcat(out\_str, " ");  
strcat(out\_str, str2);  
printf("%s\\n", out\_str);  
}  
  
变长数组也可作为函数参数传递。  
如：  
void fill\_array(int len, char str\[len\])  
{  
  
...  
  
}  
  
4.零长度数组  
允许创建长度为零的数组,用于创建变长结构.只有当零长度数组是结构体的最后一个成员  
的时候,才有意义.  
例如：  
typedef struct {  
int size;  
char str\[0\];  
}vlen;  
  
printf("sizeof(vlen)=%d\\n", sizeof(vlen)), 结果是sizeof(vlen)=4.  
  
也可以将数组定义成未完成类型也能实现同样功能.  
例如：  
typedef struct {  
int size;  
char str\[\];  
}vlen;  
  
vlen initvlen = {4, {'a', 'b', 'c', 'd'}};  
  
printf("sizeof(initvlen)=%d\\n", sizeof(initvlen));  
  
5.属性关键字\_\_attribute\_\_  
\_\_attribute\_\_可以为函数或数据声明赋属性值.给函数分配属性值主要是为了执行优化处理.  
  
例如：  
void fatal\_error() \_\_attribute\_\_ ((noreturn)); //告诉编译器该函数不会返回到调用者.  
int get\_lim() \_\_attribute\_\_ ((pure, noline)); //确保函数不会修改全局变量,  
//而且函数不会被扩展为内嵌函数  
struct mong {  
char id;  
int code \_\_attribute\_\_ ((align(4));  
};  
  
声明函数可用的属性:  
alias, always\_inine, const, constructor, deprecated, destructor, format,format\_arg,  
malloc, no\_instrument, \_function, noinline, noreturn, pure, section, used, weak  
声明变量可用的属性：  
aligned, deprecated, mode, nocommon, packed, section, unused, vector\_size, weak  
声明数据类型可用的属性：  
aligned, deprecated, packed, transparent\_union, unused  
  
6.具有返回值的复合语句  
复合语句是大括号包围的语句块, 其返回值是复合语句中最后一个表达式的类型和值.  
例如：  
ret = ({  
int a = 5;  
int b;  
b = a+3;  
});  
返回值ret的值是8.  
  
7.条件操作数省略  
例如：  
x = y? y:z;  
如果y为表达式,则会被计算两次,GCC支持省略y的第二次计算  
x = y?: z;  
以消除这种副作用.  
  
8.枚举不完全类型  
可以无需明确指定枚举中的每个值, 声明方式和结构一样, 只要声明名字, 无需指定内容.  
例如：  
enum color\_list;  
.....  
enum color\_list {BLACK, WHITE, BLUE};  
  
9.函数参数构造  
void\* \_\_builtin\_apply\_args(void);  
void\* \_\_builtin\_apply(void (\*func)(), void\* arguments, int size);  
\_\_builtin\_return(void\* result);  
  
10.函数内嵌  
通过关键字inline将函数声明为内嵌函数, ISO C中的相应关键字是\_\_inline\_\_  
  
11.函数名  
内嵌宏\_\_FUNCTION\_\_保存了函数的名字, ISO C99中相应的宏是\_\_func\_\_  
  
12.函数嵌套  
支持函数内嵌定义, 内部函数只能被父函数调用.  
  
13.函数原型  
新的函数原型可以覆盖旧风格参数列表表明的函数定义, 只要能够和旧风格参数的升级相匹配  
既可.  
例如：  
下面可用的函数原型, 在调用是short参数可以自动升级为int  
int trigzed(int zvalue);  
......  
int trized(zvalue)  
short zvalue;  
{  
return (zvalue==0);  
}  
  
14.函数返回地址和堆栈帧  
void\* \_\_builtin\_return\_address(unsigned int level);  
void\* \_\_builtin\_frame\_address(unsigned int level);  
  
15.标识符  
标识符可以包含美元符号$.  
  
16.整数  
long long int a; //Singed 64-bit integer  
unsigned long long int b; //Unsigned 64-bit integer  
a = 8686LL;  
b = 8686ULL;  
  
17.更换关键字  
命令行选项-std和-ansi会使关键字asm,typeof和inline失效,但是在这里可以使用他们的  
替代形式\_\_asm\_\_, \_\_typeof\_\_和\_\_inline\_\_  
  
18.标识地址  
可以使用标识来标记地址,将它保存到指针中,再用goto语句跳转到标记处.可通过&&操作符  
返回地址.而对表达式得出的所有空指针,使用goto语句可进行跳转.  
例如：  
#include <stdio.h>  
#include <time.h>  
int main(void)  
{  
void\* target;  
time\_t noe;  
  
now = time((time\_t\*)NULL);  
if (now & 0x1)  
target = &&oddtag;  
else  
target = &&eventag;  
  
goto \*target;  
enentag:  
printf("The time value %ld is even\\n", now);  
return 0;  
  
oddtag:  
printf("The time value %ld is odd\\n", now);  
return 0;  
}  
  
19.局部标识声明  
使用关键字\_\_label\_\_说明标识为局部标识,然后在该范围内使用.  
{  
\_\_label\_\_ restart, finished; //声明两个局部标识  
...  
goto restart;  
}  
  
20.左值表达式  
赋值操作符的左边可以使用复合表达式.  
例如：  
(fn(), b) = 10; //访问复合表达式的最后一个成员变量的地址  
和fn(), (b = 10);相同  
  
ptr = &(fn(), b); //取复合表达式的最后一个成员的地址, ptr指向b  
  
((a>5)?b:c) = 100; //条件表达式也可作为左值, 如果a大于5,则b的值是100,否则c的值是100  
  
21.可变参数的宏  
ISO C99创建宏的变参宏如下：  
#define errout(fmt,...) fprintf(stderr, fmt, \_\_VA\_ARGS\_\_)  
  
GCC支持上面形式,同时支持下面形式:  
#define errout(fmt,args...) fprintf(stderr, fmt, args)  
  
22.字符串  
一行新的字符可以被嵌入到字符串中,而不需要使用转义符\\n.可按照字面意思将他们包含在源码中.  
例如:  
char\* str1 = "A string on\\ntwo lines";  
char\* str1 = "A string on  
two lines";  
上面两个字符串等价.  
  
字符串换行符\\可以省略.  
例如：  
char\* str3 = "The string will \\  
be joined into one line.";  
char\* str4 = "The string will  
be joined into one line.";  
上面两个字符串等价.  
  
23.指针运算  
支持void和函数指针加减运算,进行运算的单位是1.  
  
24.Switch和Case分支语句  
例如：  
支持 case 8... 10:  
  
25.typedef  
关键字typedef可根据表达式的数据类型创建数据类型.  
typedef name = expression;  
  
例如：  
typedef smallreal = 0.0f;  
typedef largereal = 0.0;  
smallreal real1;  
largereal real2;  
类型smallreal为单精度浮点类型, 而largereal为双精度浮点类型.  
  
#define swap(a,b) \\  
({ typedef \_tp = a; \\  
\_tp temp = a; \\  
a = b; \\  
b = temp; })  
  
26.typeof  
关键字typeof可以声明类型表达式.用法与sizeof类型, 但是结果是类型而不是size.  
例如：  
char\* pchar; //A char pointer  
typeof (\*pchar) ch; //A char  
typeof (pchar) pcarray\[10\]; //Ten char pointers  
  
27.联合体强制类型转换  
如果数据项和联合体中成员类型相同,可以将数据项强制转为联合.  
例如：  
union dparts {  
unsigned char byte\[8\];  
double dbl;  
};  
  
double v = 3.1415;  
printf("%02X", ((union dparts)v).byte\[0\]);  
  
但是联合强制类型转换的结果不能作为左值.  
例如：  
(union dparts)v.dbl = 1.2; // Error  

内容来源：csdn.net

作者昵称：zhnlion

原文链接：https://blog.csdn.net/u013920085/article/details/49944429

作者主页：https://blog.csdn.net/u013920085

实付 元

[使用余额支付](https://blog.csdn.net/u013920085/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

[AI 搜索](https://ai.csdn.net/?utm_source=cknow_pc_blog_right_hover) [智能体](https://ai.csdn.net/cmd?utm_source=cknow_pc_blog_right_hover) [AI 编程](https://ai.csdn.net/coding?utm_source=cknow_pc_blog_right_hover) [AI 作业助手](https://ai.csdn.net/homework?utm_source=cknow_pc_blog_right_hover)

隐藏侧栏 搜索 ![程序员都在用的中文IT技术交流社区](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_app.png)

程序员都在用的中文IT技术交流社区

![专业的中文 IT 技术社区，与千万技术人共成长](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_wechat.png)

专业的中文 IT 技术社区，与千万技术人共成长

![关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_video.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部