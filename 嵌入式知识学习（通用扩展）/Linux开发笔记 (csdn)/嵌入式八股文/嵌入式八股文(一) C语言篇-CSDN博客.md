---
title: "嵌入式八股文(一) C语言篇-CSDN博客"
source: "https://blog.csdn.net/sincerelover/article/details/137131847?spm=1001.2014.3001.5502"
author:
published:
created: 2025-04-21
description: "文章浏览阅读4.7k次，点赞43次，收藏183次。笔者在学习时发觉自己的C语言很久没有系统性重温一遍了，本期主要是对于嵌入式中常用的C语言语法进行一个汇总。_嵌入式八股"
tags:
  - "clippings"
---
## 系列文章目录

嵌入式 [八股文](https://so.csdn.net/so/search?q=%E5%85%AB%E8%82%A1%E6%96%87&spm=1001.2101.3001.7020) （一）C语言篇  
嵌入式八股文（二）Linux应用篇  
嵌入式八股文（三） [Linux驱动](https://so.csdn.net/so/search?q=Linux%E9%A9%B1%E5%8A%A8&spm=1001.2101.3001.7020) 篇  
嵌入式八股文（四）FreeRTOS篇

---

---

## 前言

  笔者在学习时发觉自己的C语言很久没有系统性重温一遍了，本期主要是对于嵌入式中常用的C语言语法进行一个汇总。本次内容对于着急刷嵌入式八股文的同学也有一定帮助，详细可以去看：  
https://www.bilibili.com/video/BV1VM4y137Pm?p=3&vd\_source=937f3264dce76f586bc0a69ee24dfafa  
本系列会不定期持续更新（随笔者的学习进度），大家可以收藏一下时不时看一下。

## 一、指针和变量

  变量和指针是编程语言中的两个核心概念，它们在程序设计和执行中各自扮演着重要的角色：

- 变量是编程语言中用于存储数据的标识符，它代表了一个可以 **存储数据值** 或 **引用（即内存地址）的内存位置** 。变量具有一个唯一的名称（即变量名），它允许程序在需要时访问和操作存储在该内存位置的数据。 **变量的值** 可以在程序执行过程中 **改变** ，这使得变量成为跟踪和操作程序数据的关键工具。
- 指针（若为32位机，默认在内存占4字节）则是编程语言中的一个特殊类型的变量，它存储的是 **另一个变量的内存地址** ，而不是直接的数据值。指针提供了一种间接访问和操作内存的方式，通过指针，程序可以获取和操作指定内存地址的数据。指针在编程中有很多应用，例如动态内存分配、数据结构操作以及函数参数传递等。

  变量和指针在编程中密切相关，但又有明显的区别。变量直接存储数据值，而指针存储的是指向数据值的内存地址。在使用上，变量可以直接通过其名称来访问和操作存储的数据，而指针则需要通过解引用操作（如使用星号\*操作符）来获取指向的数据。

**通过指针赋值**  
  在进行一个赋值操作时，其流程为“CPU从flash上读取i=123指令→CPU执行指令(从指令中解析得到i的地址和要输入的数据，再输入)”，这一个过程中实际上隐藏的对地址的操作，也可以通过指针复现这个过程，这二者是等价的。例如：

```c
//1.直接写入
int i;
i=123;
//2.通过地址操作写入
int i;
int *p；
p = & i;
*p = 123;
12345678
```

**指针函数和函数指针的区别—指针函数是返回指针的函数，而函数指针是指向函数的指针**

- 指针函数：实际上是一个返回指针的函数，这个指针可以是指向任何数据类型的指针，包括整型、浮点型、结构体等，指针函数的声明形式通常如下：
```c
type* function_name(parameters);
//这里的 type* 表示函数返回的是一个指向 type 类型数据的指针。
12
```
- 函数指针：是指向函数的指针，其函数名本身就是一个指向该函数的指针（其实这里不能称为函数名，应该叫做指针的变量名），可以通过它来调用函数。函数指针的声明形式通常如下：
```c
return_type (*function_pointer_name)(parameters);
//这里的 return_type 是函数返回的类型，function_pointer_name 是函数指针的名字，parameters 是函数的参数列表。
12
```

**补充1：指针和引用的区别**

- 引用是已存在变量的别名，没有自己的存储空间；
- 引用不能为空，需要初始化时就指定一个有效的对象；
- 指针可以随意更改指向，而引用不可以，其始终指向一个对象

**补充2：指针和数组的区别**  
  数组是一块连续的内存空间，其大小在编译时确定，可以用下标访问其元素；指针大小固定，仅保存地址值并且可以指向不同的数据类型。

**补充3：野指针**  
  野指针是指指针指向的位置是不可知的（随机的、不正确的、没有明确限制的）。野指针产生的原因主要有以下几种：  
指针变量未初始化、指针释放后未置空、指针操作超越变量作用域、指针的越界、指针指向的空间释放。

## 二、关键字

| 关键字类型 | 关键字 |
| --- | --- |
| 数据 | int、char、float、double等 |
| 控制流 | if、else、for、while、do、switch、case等 |
| 存储类关键字 | auto、static、extern等 |
| 其他 | return、void、struct、union，register等 |

### 1\. volatile

  volatile关键字可以用于告诉编译器不要对变量进行优化，即不要将变量缓存在寄存器中，应该直接从内存中读取或写入变量。这在多线程访问共享变量和中断处理函数中的变量时特别有用，能确保数据的正确性和实时性。  
代码如下（示例）：

```c
int i;
i=0;
i=1;
123
```

  此时i=0可以省略，为了进一步优化速度，通常这部分内容会放到CPU中，从而使得读取不通过内存，此时如果我们想使其每次都必须从内存读取防止数据被篡改就可以加该关键字。通常情况下，以下几种情况需要使用该关键字：

- 外部中断会改变变量时，需要使用volatile确保主程序能够立即看到修改后的值。
- 外部任务会改变变量，使用volatile可以确保变量值的及时可见性。
- 对硬件寄存器进行操作，使用volatile可以防止编译器优化，确保每次都直接读取寄存器的值。

### 2\. const

  简单来说，const关键字就是表明所有人都不能改变此变量，常用于设置常量，例如圆周率等。  
**补充：const和define的区别**

- define是预处理指令，在预处理阶段执行，const在编译阶段执行；
- define没有类型检查，仅文本替换，不分配内存，而const是存于数据段中；
- define用于创建符号常量，const常创建具有常量值的变值（例如：重力加速度g，声速v等）

### 3\. static

  在大型项目中，我们常常会出现变量名命名重复的问题，此时可以增加static关键字表示该定义只能在该文件下使用，不可传递到其他目录下。

```c
// file1.c  
static int globalVar = 10;  
  
// file2.c  
extern int globalVar; // 这会导致链接错误，因为 globalVar 在 file1.c 中是静态的
12345
```

**拓展用法**

- 静态局部变量：  
	  当 static 用于函数内部的局部变量时，该变量的生命周期会延长至整个程序的执行期间，而不是仅仅在函数被调用时存在。此外，该变量只会被初始化一次，即使函数被多次调用。
```c
void func() {  
    static int count = 0;  
    count++;  
    printf("%d\n", count);  
}
12345
```
- 静态函数：  
	  静态函数只能在定义它的文件中被调用。这有助于隐藏实现细节，并减少与其他文件的命名冲突。
```c
// file1.c  
static void staticFunction() {  
    // ... some code ...  
}  
  
// file2.c  
extern void staticFunction(); // 这会导致链接错误，因为 staticFunction 在 file1.c 中是静态的
1234567
```

### 4\. extern

  在对同一变量名进行引用时，常常会出现重复定义的情况，此时便可以在一个文件中正常定义，而在其他文件加入extern关键字进行定义，告诉cpu在处理这部分内容时，变量被定义在别处。例如：

```c
//子文件
int temp；
i=1;
//主函数
extern int temp；
12345
```

## 三、数据结构

### 1\. 结构体

#### 1.1 结构体基本内容

  结构体（struct）是编程语言中用于 **组合** 不同类型的数据到一个单独的数据类型的一种构造。结构体允许你创建复合数据类型，这些数据类型由多个基本数据类型（如整数、浮点数、字符等）或其他结构体组合而成。通过结构,我们可以使用同一个名字来引用这些相关的变量集合,使得数据的组织和管理更加方便。结构体通常具有如下特性：

- 组成元素：结构体可以包含多个不同类型的成员（或称为字段），这些成员可以是基本数据类型、其他结构体类型、指针类型等。
- 命名：每个结构体都有一个唯一的名称，用于在代码中引用该结构体类型。
- 定义与初始化：在使用结构体之前，需要先进行定义，即声明结构体的名称以及它所包含的成员类型和名称。之后，可以创建结构体的实例（即变量），并为其成员赋值。
- 访问成员：通过结构体变量和点运算符（在C/C++中）或箭头运算符（在通过指针访问结构体成员时），可以访问和修改结构体的成员。
```c
#include <stdio.h>   
// 定义一个结构体类型  
struct Student {  
    char name[50];  
    int age;  
    float score;  
};  
  
int main() {  
    // 创建一个结构体的实例（变量）  
    struct Student student1 = {"张三",20,90.5f};  

    // 访问结构体的成员并打印  
    printf("姓名: %s\n", student1.name);  
    printf("年龄: %d\n", student1.age);  
    printf("分数: %.1f\n", student1.score);  
  
    return 0;  
}
12345678910111213141516171819
```

  struct只有在实例化后才会分配空间，这里在32的硬件配置时经常使用(例如GPIOX)，感兴趣可以打开了解一下。

**补充：类(class)和结构体的主要区别**

- 结构体的访问权限默认为public，而类为private；
- 结构体继承方式为公有继承，类为私有；
- 一般情况下， 结构体用于表示数据结构，而类更多表示为具有行为和数据的对象。

#### 1.2 通过指针对结构体赋值

  在项目中，我们同样可以利用指针实现结构体赋值，这种方式的好处在于具有更高的灵活性和安全性(大项目中，如果使用全局变量进行数据传输可能导致数据跑飞)。具体实现如下所示：

```c
#include <stdio.h>  
#include <string.h>  
  
// 定义结构体类型  
struct Person {  
    char name[50];  
    int age;  
};  
  
int main() {  
    // 创建两个结构体的实例  
    struct Person person1 = {"Alice", 30};  
    struct Person person2;  
  
    // 创建指向结构体类型的指针，并让它指向person1  
    struct Person *ptr = &person1;  
  
    // 通过指针访问结构体的成员  
    printf("Name: %s, Age: %d\n", ptr->name, ptr->age);  
  
    // 通过指针对结构体进行赋值  
    // 将person1的值赋给person2  
    person2 = *ptr; // 解引用指针，获取其指向的结构体的值，并赋给person2  
  
    // 直接访问person2的成员，验证赋值是否成功  
    printf("person2 Name: %s, Age: %d\n", person2.name, person2.age);  
  
    // 也可以通过指针直接修改结构体的成员  
    strcpy(ptr->name, "Bob");  
    ptr->age = 25;  
  
    // 再次输出修改后的值  
    printf("Modified Name: %s, Age: %d\n", ptr->name, ptr->age);  
  
    return 0;  
}
123456789101112131415161718192021222324252627282930313233343536
```
- struct Person \*ptr = &person1; 创建了一个指向 person1 的结构体指针 ptr。
- printf(“Name through pointer: %s\\n”, ptr->name); 通过指针 ptr 访问 person1的name 成员。
- person2 = \*ptr; 通过解引用指针 ptr（即 \*ptr），获取 person1 的值，并将其赋给person2。

  通过指针给结构体赋值则是使用这个地址来获取结构体的值，并将这个值赋给另一个结构体变量。

#### 1.3 结构体指针

  在C语言中，结构体指针是一个特殊的指针变量，它指向一个结构体类型的变量或内存区域。通过使用结构体指针，你可以间接地访问和操作结构体的成员。这里我们对上例进行修改：

```c
#include <stdio.h>  
#include <string.h>  
  
// 定义结构体类型  
struct Person {  
    char name[50];  
    int age;  
};  
  
int main() {  
    // 创建两个结构体的实例  
    struct Person person1 = {"Alice", 30};  
    struct Person person2;  
  
    // 创建指向结构体类型的指针，并让它指向person1  
    struct Person *ptr = &person1;  
  
    // 通过指针访问person1的成员  
    printf("Name through pointer: %s\n", ptr->name);  
    printf("Age through pointer: %d\n", ptr->age);  
  
    // 通过结构体指针给结构体赋值  
    // 将ptr指向的结构体（即person1）的值赋给person2  
    memcpy(&person2, ptr, sizeof(struct Person)); // 使用memcpy通过指针复制结构体内容  
  
    // 直接访问person2的成员，验证赋值是否成功  
    printf("person2 Name: %s\n", person2.name);  
    printf("person2 Age: %d\n", person2.age);  
  
    return 0;  
}
12345678910111213141516171819202122232425262728293031
```

  在这个修改后的例子中，我使用了 memcpy 函数来通过结构体指针 ptr 复制 person1 的内容到 person2。memcpy 函数从 ptr 指向的地址开始，复制 sizeof(struct Person) 字节到 &person2 的地址。这样就实现了通过结构体指针给另一个结构体赋值的效果。此外，结构体指针最主要的功能在于你可以通过“ptr->XXX = ？”的形式来实现对某设定好的结构体的成员的改动，而普通的结构体变量则做不到这一点。

**注：这时候你可能会感觉到很懵，这不是一样的吗，实际上结构体指针和通过指针给结构体赋值不是同一个意思，但它们之间有关联。结构体指针是一个变量，它存储了一个结构体的内存地址。通过这个地址，你可以间接地访问和修改结构体的成员。而通过指针给结构体赋值，是指使用结构体指针来将一个结构体的值赋给另一个结构体。这通常涉及到解引用指针来获取其指向的结构体的值，然后将这个值赋给另一个结构体变量。**  
**补充：结构体中的成员也可以是函数指针，在使用时的功能和正常函数一样，赋值时和其他成员一样，例如：**

```c
#include <stdio.h>  
  
// 定义两个简单的函数  
void print_hello() {  
    printf("Hello, World!\n");  
}  
  
void print_goodbye() {  
    printf("Goodbye, World!\n");  
}  
  
// 定义结构体，其中包含一个函数指针成员  
typedef struct {  
    void (*print_func)(); // 函数指针成员，指向无参数无返回值的函数  
} FunctionStruct;  
  
int main() {  
    // 创建两个结构体实例，并分别初始化它们的函数指针成员  
    FunctionStruct fs_hello = {print_hello};  
    FunctionStruct fs_goodbye = {print_goodbye};    
    // 通过结构体中的函数指针调用函数  
    fs_hello.print_func(); // 输出: Hello, World!  
    fs_goodbye.print_func(); // 输出: Goodbye, World!  
    return 0;  
}
12345678910111213141516171819202122232425
```

#### 1.5 位域

  位域是一种结构体的特殊用法，用于在 **结构体中以位为单位** ，用于节省空间。其定义方式与普通结构体类似，但字段后加上`:n` 表示该字段占用n位，例如：  
`unsigned int a : n; // 表示占用3位` 值得注意的是，位域是 **按字节存储，不会跨字节** ，此外会 **限制数据类型**

### 2\. 联合体

  联合体，或称共用体，是一种特殊的数据类型，允许在相同的内存位置存储不同的数据类型。但需要注意的是，联合体在同一时刻只能存储一个成员的值，因为所有成员都共享相同的内存空间。这意味着当改变联合体中一个成员的值时，其他成员的值可能会被覆盖或改变。联合体常用于节省内存空间，或者在某些需要灵活处理不同数据类型的情况下使用。

```c
#include <stdio.h>  
  
union Data {  
    int i;  
    float f;  
    char str[20];  
};  
  
int main() {  
    union Data data;  
    data.i = 10;  
    printf("data.i : %d\n", data.i);  
  
    data.f = 220.5;  
    printf("data.f : %f\n", data.f);  
  
    strcpy(data.str, "Hello");  
    printf("data.str : %s\n", data.str);  
  
    return 0;  
}
123456789101112131415161718192021
```

**补充：联合体和结构体的主要区别**  
  联合体允许在同一内存位置存储不同的数据类型，但同一时刻只能存储一个成员的值；而结构体则将不同类型的数据组合在一起，每个成员都有自己的内存空间，并且可以同时存储所有成员的值。这两种数据结构各有其适用的场景，具体使用哪种取决于特定的需求和目标。

### 3\. 链表

#### 3.1 基本概念

  链表（Linked List）是一种常见的数据结构，它由一系列节点（ Node ）组成，每个节点包含两个部分：数据域和指针域。数据域用于存储数据元素，指针域则用于指向链表中的下一个节点。通过指针的连接，链表可以动态地存储数据，并且可以根据需要进行扩展或缩减。链表有多种类型，最常见的有单向链表、双向链表和循环链表。

- 单向链表：每个节点包含一个数据元素和一个指向下一个节点的指针。第一个节点（头节点）的指针指向链表中的第一个数据节点，最后一个节点的指针通常指向 NULL 表示链表的结束。只能从头节点开始顺序访问链表中的元素。
- 双向链表：每个节点除了包含一个数据元素外，还包含两个指针：一个指向前一个节点，一个指向下一个节点。双向链表可以从任意节点向前或向后遍历，第一个节点的前指针通常指向 NULL，最后一个节点的后指针也指向 NULL。
- 循环链表：循环链表与单向链表类似，但最后一个节点的指针指向头节点，形成一个环。循环链表可以循环遍历整个链表。

   接下来是一个简单的单向链表节点定义：

```c
typedef struct Node {  
   int data;               // 数据域  
   struct Node* next;     // 指针域，指向下一个节点  
} Node;
1234
```

#### 3.2 链表的插入和删除

  一般在插入时，我们选择传递指针(节省内存资源)，示例如下：

```c
#include <stdio.h>  
#include <stdlib.h>  
 
typedef struct Node {  
   int data;  
   struct Node* next;  
} Node;  
 
// 创建新节点  
Node* createNode(int data) {  
   Node* newNode = (Node*)malloc(sizeof(Node));  
   if (!newNode) {  
       printf("Memory allocation failed.\n");  
       exit(1);  
   }  
   newNode->data = data;  
   newNode->next = NULL;  
   return newNode;  
}  
 
// 在链表末尾插入节点  
void insertNode(Node** head, int data) {  
   Node* newNode = createNode(data);  
   if (*head == NULL) {  
       *head = newNode;  
   } else {  
       Node* current = *head;  
       while (current->next != NULL) {  
           current = current->next;  
       }  
       current->next = newNode;  
   }  
}  
 
// 遍历链表并打印节点数据  
void printList(Node* head) {  
   Node* current = head;  
   while (current != NULL) {  
       printf("%d ", current->data);  
       current = current->next;  
   }  
   printf("\n");  
}  
 
int main() {  
   Node* head = NULL; // 初始化空链表  
     
   // 插入节点  
   insertNode(&head, 1);  
   insertNode(&head, 2);  
   insertNode(&head, 3);  
     
   // 打印链表  
   printList(head); // 输出: 1 2 3   
     
   // 释放链表内存（这里省略了释放内存的代码）  
     
   return 0;  
}
1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859
```
```c
#include <stdio.h>  
#include <stdlib.h>  
 
// 定义链表节点  
typedef struct Node {  
   int data;  
   struct Node* next;  
} Node;  
 
// 创建新节点  
Node* createNode(int data) {  
   Node* newNode = (Node*)malloc(sizeof(Node));  
   if (!newNode) {  
       printf("Memory allocation failed.\n");  
       exit(1);  
   }  
   newNode->data = data;  
   newNode->next = NULL;  
   return newNode;  
}  
 
// 删除指定值的节点  
void deleteNode(Node** head, int value) {  
   // 处理头节点的情况  
   if (*head != NULL && (*head)->data == value) {  
       Node* temp = *head;  
       *head = (*head)->next;  
       free(temp);  
       return;  
   }  
     
   // 处理链表其他节点的情况  
   Node* current = *head;  
   while (current->next != NULL) {  
       if (current->next->data == value) {  
           Node* temp = current->next;  
           current->next = current->next->next;  
           free(temp);  
           return;  
       }  
       current = current->next;  
   }  
     
   // 如果没有找到要删除的节点  
   printf("Node with value %d not found in the list.\n", value);  
}  
 
// 遍历链表并打印节点数据  
void printList(Node* head) {  
   Node* current = head;  
   while (current != NULL) {  
       printf("%d ", current->data);  
       current = current->next;  
   }  
   printf("\n");  
}  
 
// 主函数  
int main() {  
   Node* head = NULL; // 初始化空链表  
     
   // 插入节点  
   head = createNode(1);  
   insertNode(&head, 2);  
   insertNode(&head, 3);  
   insertNode(&head, 4);  
   insertNode(&head, 5);  
     
   // 打印原始链表  
   printf("Original list: ");  
   printList(head);  
     
   // 删除节点  
   int valueToDelete = 3;  
   deleteNode(&head, valueToDelete);  
     
   // 打印删除节点后的链表  
   printf("List after deleting node with value %d: ", valueToDelete);  
   printList(head);  
     
   // 释放链表内存  
   Node* current = head;  
   while (current != NULL) {  
       Node* temp = current;  
       current = current->next;  
       free(temp);  
   }  
     
   return 0;  
}
123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990
```

  这部分代码的核心在于判断当前是否是最后一项(或者是要删除项的前一项)，可以简单理解为排火车，插入时需要考虑是否插入的地方后面没有人，如果没有就可以插进去了。同理，在删除时也需要知道被删除的人在“谁后边”，确定之后才能进行操作。

**补充：如何判断链表是否有环**  
  利用快慢指针，同时指向链表头，一个设置每次移动两个节点，另一个为单节点移动，观察是否会产生重合。

### 4\. 栈（Stack）

  栈是一种后进先出（LIFO）的数据结构，用于 **存储局部变量和函数调用的信息** 。在程序执行时，栈会自动分配和释放内存空间。每次函数调用时，都会在栈上创建一个新的栈帧（stack frame），用于存储该函数的局部变量和返回地址等信息。函数执行完毕后，对应的栈帧会被销毁，其占用的内存空间会被自动释放。栈的大小通常有限，并且栈上的数据访问速度非常快。

### 5\. 堆（Heap）

  堆是用于动态内存分配的区域，程序员可以在运行时显式地请求分配和释放内存。在C和C++等语言中，通常使用malloc、calloc、realloc和free等函数来在堆上分配和释放内存。堆的大小通常比栈大得多，且分配和释放内存的操作相对较慢（因为需要查找可用的内存块并进行 内存管理 ）。堆上的数据可以在程序的整个生命周期内存在，直到显式地释放它们。

**注 ：栈是自动管理内存的，主要用于存储局部变量和函数调用信息，其大小有限且访问速度快，向低地址拓展；堆是手动管理内存的，用于动态内存分配，其大小较大且分配和释放操作相对较慢，向高地址拓展。**

**补充：C语言中内存分配的方法：静态分配、堆上分配、栈上分配。**

### 6\. 队列

  队列（Queue） 是一种先进先出（FIFO，First In First Out）的数据结构。它就像日常生活中的排队一样，新加入的元素会被放到队尾，而访问元素时总是从队头开始取，队列不允许在中间位置进行插入或删除操作。  
队列的基本操作通常包括：

- 入队（Enqueue）：在队列的尾部添加一个新元素。
- 出队（Dequeue）：移除队列的头部元素，并返回该元素的值。
- 查看队头（Peek）：返回队列头部元素的值，但不移除它。
- 判断队列是否为空：检查队列中是否还有元素。

**注：队列与栈和堆在内存管理上有本质的区别，栈和堆是内存管理的两种方式，而队列则是一种数据结构，用于组织和管理数据。**

## 四、 内存

  内存是一个非常重要的概念，因为它决定了程序在运行时可以存储哪些数据以及这些数据是如何被访问的。内存是计算机中的一个重要组成部分，用于存储数据和程序指令。它分为多种类型，如RAM（随机存取存储器）、ROM（只读存储器）等，但在编程时，我们通常指的是RAM。RAM中的每一个字节都有一个唯一的地址，通过这个地址，我们可以读取或写入该字节的数据。

### 1\. 内存分配的方法

  常用的内存分配方法为：静态分配、堆上分配(也称为动态分配内存)、栈上分配，下表是详细的对比。

| 项目 | 静态分配 | 堆上分配 | 栈上分配 |
| --- | --- | --- | --- |
| 分配时机 | 编译阶段 | 执行时 | 执行时 |
| 移植性 | 较差 | 较好 | 较好 |
| 生命周期 | 整个程序 | 由程序员控制 | 生命周期与其所在的函数相对应 |
| 内存释放 | \- | 手动(free) | 自动 |
| 效率 | 快速，无需运行时开销 | 极高效，O(1)时间复杂度 | 较慢，涉及搜索可用内存块 |
| 内存碎片 | 几乎无碎片 | 可能有外部和内部碎片 | 无碎片 |

### 2\. malloc和free

  malloc 和 free 是C语言（以及C++中兼容C的部分）中用于动态内存管理的库函数。它们允许程序员在运行时分配和释放任意大小的内存块。  
1） malloc 函数  
  malloc的原理是调用mmap系统调用向操作系统按4K整数倍 **批量** 申请一或者多页，通过优化手段提高分配效率并 **零发** 给用户。

```c
//用于动态地分配内存块。它的原型在 stdlib.h 头文件中定义。
void *malloc(size_t size);
12
```
- 参数：size 指定了要分配的字节数
- 返回值
	- 如果内存成功分配，malloc 返回一个指向分配的内存块的指针。
	- 如果内存分配失败（例如，由于内存不足），malloc 返回 NULL。

  使用 malloc 时，需要注意以下几点：

- 返回的是 void 指针，因此需要将其转换为适当的类型才能使用。
- 分配的内存块是未初始化的，包含随机数据。
- **分配的内存块在堆上** ，因此其 **生命周期不受作用域的限制** 。

| 函数名 | 功能 |
| --- | --- |
| malloc | 分配 **用户** 内存，保证在 **虚拟地址** 空间上连续 |
| kmalloc | 分配 **内核** 内存，保证在 **物理地址** 空间上连续 |
| vmalloc | 分配 **内核** 内存，保证在 **虚拟地址** 空间上连续 |

2）free 函数

```c
//用于释放先前由 malloc、calloc、realloc 分配的内存块。它的原型也在 stdlib.h 头文件中定义。
void free(void *ptr);
12
```
- 参数：ptr是之前由 malloc、calloc 或 realloc 返回的指针。

**注：** 调用 free 后，指针本身的值不会被自动设置为 NULL，因此为了避免野指针（dangling pointer），通常建议将指针设置为 NULL。释放内存后，不应再访问该内存块，因为其内容可能已被覆盖或不可访问。

### 3\. 内存泄漏

  内存泄漏（Memory Leak）是指在计算机程序中，由于疏忽或错误造成程序未能释放已经不再使用的内存的情况。内存泄漏并不是指内存从物理内存中消失，而是指程序在运行过程中动态分配的内存由于某种原因在逻辑上无法被释放或回收，导致系统内存的浪费，严重时甚至会导致程序崩溃。内存泄漏的常见原因包括：

- 错误地使用动态内存分配：例如，在C或C++中，使用malloc、calloc、realloc或new分配的内存没有被free或delete释放。
- 循环引用：在对象间存在循环引用时，如果没有合适的机制来打破这种循环，内存可能无法被释放。
- 全局变量或静态变量使用不当：虽然它们本身不是动态分配的，但如果它们引用了动态分配的内存，并且这些引用在程序结束时没有被清除，也可能导致内存泄漏。
- 资源（非内存资源）未释放：虽然这里讨论的是内存泄漏，但也要注意到其他类型的资源（如文件句柄、数据库连接、网络套接字等）如果没有被正确关闭或释放，也可能导致类似的问题。

解决内存泄漏的方法通常包括：

- 使用内存分析工具来检测和定位内存泄漏。
- 确保动态分配的内存在使用完毕后被正确释放。
- 使用智能指针（如C++中的std::unique\_ptr和std::shared\_ptr）来自动管理内存。
- 仔细设计对象的生命周期和引用关系，避免循环引用。

### 4\. 内存溢出

  内存溢出（Out Of Memory，简称OOM）是指应用系统中存在无法回收的内存或使用的内存过多，最终使得程序运行 **所需的内存大于系统能提供的最大内存** 。内存溢出的原因可以有很多，以下是一些常见的原因：数组越界访问、指针错误、尝试未分配或者已经释放的地址空间。

### 5\. 内存对齐

  内存对齐是在存储数据时，将数据按一定规则放置在内存的过程。其原则为：以最大变量所占内存来分配内存空间。

### 6\. 虚拟地址空间布局

| 类型 | 存储区域 |
| --- | --- |
| 函数 | 代码段 |
| 局部变量 | 栈区 |
| 全局变量/静态变量 | 数据段 |
| 动态分配的变量 | 堆区 |
| 常量 | 只读数据段或者代码段 |

  这个布局是从高地址到低地址排列的，以下是对每个部分的解释：

1. 栈区（向下增长）：栈是用于存储局部变量、函数参数以及返回地址的地方。
2. 堆区（向上增长）：堆是用于动态内存分配的区域。
3. BSS段：BSS段用于存放 **未初始化** 的全局变量和静态变量。
4. Data段：Data段用于存放 **已初始化** 的全局变量和静态变量。
5. RO Data段：也称为常量区，用来存放只读数据，这个段的内容在程序运行期间不能被修改。
6. 代码段：代码段段包含程序的实际机器码及函数，通常是只读的。

### 7\. 内存碎片

  内存碎片是指内存分配和释放的过程中，导致内存分割成多个不连续小块，而导致不能为大内存的请求提供空间。这种现象会导致 **内存利用率下降** 、 **增加内存存在失败风险** 。内存碎片通常分为 **内部碎片** （分配比所需大）和 **外部碎片** （没有足够连续空间满足大内存分配），可以采用 **内存压缩** 、 **内存池** 、 **垃圾回收机制** 等方法进行解决。

## 五、算法

### 1\. 常见算法的时间复杂度和空间复杂度

| 算法 | 时间复杂度（最优） | 时间复杂度（平均） | 时间复杂度（最坏） | 空间复杂度 |
| --- | --- | --- | --- | --- |
| 线性搜索 | $O                                     (                                     1                                     )                                              O(1)                              O(1)$ | $O                                     (                                     n                                     )                                              O(n)                              O(n)$ | $O                                     (                                     n                                     )                                              O(n)                              O(n)$ | $O                                     (                                     1                                     )                                              O(1)                              O(1)$ |
| **二分搜索** | $O                                     (                                     1                                     )                                              O(1)                              O(1)$ | $O                                     (                                     log                                     ⁡                                     n                                     )                                              O(\log n)                              O(logn)$ | $O                                     (                                     log                                     ⁡                                     n                                     )                                              O(\log n)                              O(logn)$ | 迭代: $O                                     (                                     1                                     )                                              O(1)                              O(1)$, 递归: $O                                     (                                     log                                     ⁡                                     n                                     )                                              O(\log n)                              O(logn)$ |
| **冒泡排序** | $O                                     (                                     n                                     )                                              O(n)                              O(n)$ | $O                                     (                                                   n                                        2                                                  )                                              O(n^2)                              O(n2)$ | $O                                     (                                                   n                                        2                                                  )                                              O(n^2)                              O(n2)$ | $O                                     (                                     1                                     )                                              O(1)                              O(1)$ |
| **选择排序** | $O                                     (                                                   n                                        2                                                  )                                              O(n^2)                              O(n2)$ | $O                                     (                                                   n                                        2                                                  )                                              O(n^2)                              O(n2)$ | $O                                     (                                                   n                                        2                                                  )                                              O(n^2)                              O(n2)$ | $O                                     (                                     1                                     )                                              O(1)                              O(1)$ |
| **插入排序** | $O                                     (                                     n                                     )                                              O(n)                              O(n)$ | $O                                     (                                                   n                                        2                                                  )                                              O(n^2)                              O(n2)$ | $O                                     (                                                   n                                        2                                                  )                                              O(n^2)                              O(n2)$ | $O                                     (                                     1                                     )                                              O(1)                              O(1)$ |
| **快速排序** | $O                                     (                                     n                                     log                                     ⁡                                     n                                     )                                              O(n \log n)                              O(nlogn)$ | $O                                     (                                     n                                     log                                     ⁡                                     n                                     )                                              O(n \log n)                              O(nlogn)$ | $O                                     (                                                   n                                        2                                                  )                                              O(n^2)                              O(n2)$ | 迭代: $O                                     (                                     log                                     ⁡                                     n                                     )                                              O(\log n)                              O(logn)$, 递归: $O                                     (                                     n                                     )                                              O(n)                              O(n)$ |
| 归并排序 | $O                                     (                                     n                                     log                                     ⁡                                     n                                     )                                              O(n \log n)                              O(nlogn)$ | $O                                     (                                     n                                     log                                     ⁡                                     n                                     )                                              O(n \log n)                              O(nlogn)$ | $O                                     (                                     n                                     log                                     ⁡                                     n                                     )                                              O(n \log n)                              O(nlogn)$ | $O                                     (                                     n                                     )                                              O(n)                              O(n)$ |
| 堆排序 | $O                                     (                                     n                                     log                                     ⁡                                     n                                     )                                              O(n \log n)                              O(nlogn)$ | $O                                     (                                     n                                     log                                     ⁡                                     n                                     )                                              O(n \log n)                              O(nlogn)$ | $O                                     (                                     n                                     log                                     ⁡                                     n                                     )                                              O(n \log n)                              O(nlogn)$ | $O                                     (                                     1                                     )                                              O(1)                              O(1)$ |
| 广度优先搜索 | $O                                     (                                     V                                     +                                     E                                     )                                              O(V + E)                              O(V+E)$ | $O                                     (                                     V                                     +                                     E                                     )                                              O(V + E)                              O(V+E)$ | $O                                     (                                     V                                     +                                     E                                     )                                              O(V + E)                              O(V+E)$ | $O                                     (                                     V                                     )                                              O(V)                              O(V)$ |
| 深度优先搜索 | $O                                     (                                     V                                     +                                     E                                     )                                              O(V + E)                              O(V+E)$ | $O                                     (                                     V                                     +                                     E                                     )                                              O(V + E)                              O(V+E)$ | $O                                     (                                     V                                     +                                     E                                     )                                              O(V + E)                              O(V+E)$ | $O                                     (                                     V                                     )                                              O(V)                              O(V)$ |

### 2\. 冒泡算法

  冒泡排序是一种简单直观的排序算法，通过重复遍历待排序的数列， **比较相邻元素并交换位置** ，逐步将最大（或最小）的元素“冒泡”到数列的一端。

### 3\. 插入排序

  插入排序是一种简单的排序算法，类似于整理扑克牌的过程。它通过 **构建有序序列** ，对于未排序数据，在已排序序列中从后向前扫描，找到相应位置并插入。例如取出下一个元素，在已排序部分从后向前扫描，如果该元素（已排序）大于新元素，将该元素移到下一位置，直到找到已排序元素小于或者等于新元素的位置。

```c
void insertionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; ++i) {
        int key = arr[i];
        int j = i - 1;

        // 将key插入到arr[0..i-1]中
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}
1234567891011121314
```

### 4\. 快速排序

  快速排序是一种分治算法，它通过一个 **基准** 元素将 **数组分为两个子数组** ，然后递归地对这两个子数组进行排序。从数组中选择一个基准元素（pivot）；重新排列数组，所有比基准小的元素放在基准前面，所有比基准大的元素放在基准后面（分区操作）；递归地对基准前后的子数组进行快速排序。

```c
void swap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high]; // 选择最后一个元素作为基准
    int i = low - 1;       // 较小元素的索引

    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++; // 增加较小元素的索引
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return (i + 1);
}

void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);

        // 分别对基准前后两部分进行排序
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}
1234567891011121314151617181920212223242526272829
```

### 5\. 选择排序

  选择排序是一种简单直观的选择排序算法。它每次 **从未排序部分选择最小（或最大）的元素** ，并将其放到已排序部分的末尾。

```c
void selectionSort(vector<int>& arr) {
    int n = arr.size();

    for (int i = 0; i < n - 1; i++) {
        // 找到未排序部分的最小元素的索引
        int min_idx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[min_idx])
                min_idx = j;
        }

        // 将找到的最小元素与第一个未排序元素交换
        swap(arr[min_idx], arr[i]);
    }
}
123456789101112131415
```

内容来源：csdn.net

作者昵称：云雨歇

原文链接：https://blog.csdn.net/sincerelover/article/details/137131847

作者主页：https://blog.csdn.net/sincerelover

实付 元

[使用余额支付](https://blog.csdn.net/sincerelover/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

 [![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/Group-dark.png) 点击体验  
DeepSeekR1满血版](https://ai.csdn.net/?utm_source=cknow_pc_blogdetail&spm=1001.2101.3001.10583) 隐藏侧栏

![程序员都在用的中文IT技术交流社区](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_app.png)

程序员都在用的中文IT技术交流社区

程序员都在用的中文IT技术交流社区

![专业的中文 IT 技术社区，与千万技术人共成长](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_wechat.png)

专业的中文 IT 技术社区，与千万技术人共成长

专业的中文 IT 技术社区，与千万技术人共成长

![关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_video.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部