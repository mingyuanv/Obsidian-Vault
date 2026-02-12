---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：




# 一、每个实验的要完成的任务

### 1 、实验一：通过ioctl对定时器进行控制，分别实现打开定时器、关闭定时器和设置定时时间的功能。


### 2 、实验二：对实验一的应用程序进行封装，从而让应用编程人员更好的对设备进行编程。


### 3 、





# 二、 ioctl控制定时器实验

##  驱动程序编写
### 1 、关键代码
```c
#define TIMER_OPEN _IO('L',0)
#define TIMER_CLOSE _IO('L',1)
#define TIMER_SET _IOW('L',2,int)


static long cdev_test_ioctl(struct file *file,unsigned int cmd,unsigned long arg){

    struct device_test *test_dev = (struct device_test *)file->private_data;//设置私有数据

    switch(cmd){

        case TIMER_OPEN:
            add_timer(&timer_test);//添加一个定时器
            break;

        case TIMER_CLOSE :

            del_timer(&timer_test);//删除一个定时器
			
            break;

        case TIMER_SET :

            test_dev->counter=arg;//设置定时循环时间
            timer_test.expires=jiffies_64+msecs_to_jiffies(test_dev->counter);//设置定时时间

            break;

        default:
            break;
    }
    return 0;

}
```


### 2 、完整代码
```c
#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/kdev_t.h>
#include <linux/uaccess.h>


#define TIMER_OPEN _IO('L',0)
#define TIMER_CLOSE _IO('L',1)
#define TIMER_SET _IOW('L',2,int)

struct device_test{

    dev_t dev_num;//设备号
    int major;  
    int minor;

    struct cdev cdev_test;  // 字符设备结构体
    struct class *class;    // 类指针
    struct device *device;  // 设备指针

    int counter;


};
// 实例化一个设备结构体变量
struct device_test dev1;

//定义function_test定时功能函数
static void function_test(struct timer_list *t);

//定义一个定时器
DEFINE_TIMER(timer_test,function_test);

/* 定时处理函数 */
static void function_test(struct timer_list *t){

    printk("this is function test\n");

    //使用mod_timer函数将定时时间设置为五秒后
    mod_timer(&timer_test,jiffies_64+msecs_to_jiffies(dev1.counter));


}





static int cdev_test_open(struct inode *inode, struct file *file)
{
    file->private_data=&dev1;//设置私有数据
    return 0;
}

static int cdev_test_release(struct inode *inode, struct file *file)
{
    file->private_data=&dev1;//设置私有数据

    return 0;
}








static long cdev_test_ioctl(struct file *file,unsigned int cmd,unsigned long arg){

    struct device_test *test_dev = (struct device_test *)file->private_data;//设置私有数据

    switch(cmd){

        case TIMER_OPEN:
            add_timer(&timer_test);//添加一个定时器
            break;

        case TIMER_CLOSE :

            del_timer(&timer_test);//删除一个定时器
			
            break;

        case TIMER_SET :

            test_dev->counter=arg;
            timer_test.expires=jiffies_64+msecs_to_jiffies(test_dev->counter);//设置定时时间

            break;

        default:
            break;

        
    }

    return 0;

}





struct file_operations cdev_test_fops={

    .owner = THIS_MODULE, //将owner字段指向本模块，可以避免在模块的操作正在被使用时卸载该模块
    .open = cdev_test_open,
	.release = cdev_test_release,
    .unlocked_ioctl=cdev_test_ioctl,

};


static int __init chr_fops_init(void){

    int ret;

    /*1 创建设备号*/
    ret=alloc_chrdev_region(&dev1.dev_num,0,1,"alloc_name");
    if(ret<0){
        goto err_chrdev;
    }
    printk("alloc_chrdev_region is ok\n");

    //打印设备号
    dev1.major=MAJOR(dev1.dev_num);
    dev1.minor=MINOR(dev1.dev_num);
    printk("major is %d \r\n", dev1.major); //打印主设备号
    printk("minor is %d \r\n", dev1.minor); //打印次设备号

    /*2 初始化cdev*/
    dev1.cdev_test.owner=THIS_MODULE;
    cdev_init(&dev1.cdev_test,&cdev_test_fops);

    /*3 添加一个cdev,完成字符设备注册到内核*/
   ret=cdev_add(&dev1.cdev_test,dev1.dev_num,1);
    if(ret<0)
    {
        goto  err_chr_add;
    }

    /*4 创建类*/
    dev1.class=class_create(THIS_MODULE,"test");
    if(IS_ERR(dev1.class)){

        ret=PTR_ERR(dev1.class);
        goto err_class_create;
    }

    /*5  创建设备*/
    dev1.device=device_create(dev1.class,NULL,dev1.dev_num,NULL,"test");
    if(IS_ERR(dev1.device))
    {
        ret=PTR_ERR(dev1.device);
        goto err_device_create;
    }

return 0;

//错误处理
err_device_create:
    class_destroy(dev1.class);

err_class_create:
    cdev_del(&dev1.cdev_test);

err_chr_add:
    unregister_chrdev_region(dev1.dev_num,1);

err_chrdev:
    return ret;

}



static void __exit chr_fops_exit(void) //驱动出口函数
{
    /*注销字符设备*/
    unregister_chrdev_region(dev1.dev_num, 1); //注销设备号
    cdev_del(&dev1.cdev_test);                 //删除cdev
    device_destroy(dev1.class, dev1.dev_num);       //删除设备
    class_destroy(dev1.class);                 //删除类
}


module_init(chr_fops_init);
module_exit(chr_fops_exit);

MODULE_LICENSE("GPL v2");
MODULE_AUTHOR("topeet");
```


### 3 、




## 应用测试代码ioctl_timer.c

```c
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>

#define TIMER_OPEN _IO('L',0)
#define TIMER_CLOSE _IO('L',1)
#define TIMER_SET _IOW('L',2,int)


int main(int argc,char *argv[]){

    int fd;

    //使用非阻塞的方式打开设备
    fd = open("/dev/test",O_RDWR);//打开/dev/test设备
    if(fd < 0 ){
		printf("file open error \n");
	}

    //定时循环一秒
    ioctl(fd,TIMER_SET,1000);
    ioctl(fd,TIMER_OPEN);
    sleep(3);

    //定时循环三秒
    ioctl(fd,TIMER_SET,3000);
    sleep(7);
    ioctl(fd,TIMER_CLOSE);


    close(fd);

    return 0;

}
```

> 第8-10行通过合成宏定义了三个ioctl命令，分别代表**定时器打开、定时器关闭、定时时间设置**。
> 
> 第18行和第21行将定时时间分别设置为1秒和3秒。
> 
> 第19行打开定时器。
> 
> 第23行关闭定时器。





## 测试
> [root@topeet:~]# **insmod ioctl_timer.ko**
> [  331.183476] ioctl_timer: loading out-of-tree module taints kernel.
> [root@topeet:~]# [  331.184552] alloc_chrdev_region is ok
> [  331.184578] major is 236
> [  331.184590] minor is 0
> 
> [root@topeet:~]# **./ioctl_timer**
> [  336.771074] this is function test
> [  337.784407] this is function test
> [  338.797647] this is function test
> [  341.971165] this is function test
> [  345.171075] this is function test





# 三、封装驱动API接口

## 拆分封装库文件
### 1 、timerlib.h
```c
#ifndef _TIMERLIB_H_
#define _TIMERLIB_H_

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>

#define TIMER_OPEN _IO('L',0)
#define TIMER_CLOSE _IO('L',1)
#define TIMER_SET _IOW('L',2,int)

int dev_open();//定义设备打开函数

int timer_open(int fd);//定义定时器打开函数
int timer_close(int fd);//定义定时器关闭函数
int timer_set(int fd,int arg);//定义设置计时时间函数


#endif
```

### 2 、dev_open.c
```c
#include <stdio.h>
#include"timerlib.h"

int dev_open(){

    int fd;

    //使用非阻塞的方式打开设备
    fd = open("/dev/test",O_RDWR,0777);//打开/dev/test设备
    if(fd < 0 ){
		printf("file open error \n");
	}

    return fd;
}


```

### 3 、timer_close.c
```c
#include <stdio.h>
#include"timerlib.h"

int timer_close(int fd){
    
	int ret;
	ret = ioctl(fd,TIMER_CLOSE);
	if(ret < 0){
		printf("ioctl close error \n");
		return -1;
	}
	return ret;

}

```


### 4 、timer_open.c
```c
#include <stdio.h>
#include"timerlib.h"

int timer_open(int fd){
    
	int ret;
	ret = ioctl(fd,TIMER_OPEN);
	if(ret < 0){
		printf("ioctl open error \n");
		return -1;
	}
	return ret;

}

```

### 5、timer_set.c
```c
#include <stdio.h>
#include"timerlib.h"

int timer_set(int fd,int arg){
    
	int ret;
	ret =ioctl(fd,TIMER_SET,arg);
	if(ret < 0){
		printf("ioctl set error \n");
		return -1;
	}
	return ret;

}
```

### 6、


### 7、测试要用到的应用程序ioctl_timer.c文
```c
#include <stdio.h>
#include"timerlib.h"



int main(int argc,char *argv[]){

    int fd;
    fd=dev_open();

    timer_set(fd,1000);
    timer_open(fd);
    sleep(3);

    timer_set(fd,3000);
    sleep(7);
    timer_close(fd);


    close(fd);

    return 0;

}
```

### 8、



## 编译应用程序
### 1 、将存放功能函数的c文件编译成.o文件（方便链接）
```c
aarch64-linux-gnu-gcc -c dev_open.c

aarch64-linux-gnu-gcc -c timer*.c
```
> topeet@ubuntu:~/Linux/test/test_ming/36-ioctl_timer/app$ `export PATH=$PATH:/home/topeet/Linux/rk356x_linux/prebuilts/gcc/linux-x86/aarch64/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin/`
topeet@ubuntu:~/Linux/test/test_ming/36-ioctl_timer/app$ `aarch64-linux-gnu-gcc -c dev_open.c`
topeet@ubuntu:~/Linux/test/test_ming/36-ioctl_timer/app$ `aarch64-linux-gnu-gcc -c timer*.c
`

### 2 、将相应的.o文件编译成.a静态库（这里要注意库的名称都以lib开头）
```c
aarch64-linux-gnu-ar rcs libtimer.a timer*.o

aarch64-linux-gnu-ar rcs libopen.a dev_open.o
```
> topeet@ubuntu:~/Linux/test/test_ming/36-ioctl_timer/app$ `aarch64-linux-gnu-ar rcs libtimer.a timer*.o`
topeet@ubuntu:~/Linux/test/test_ming/36-ioctl_timer/app$ `aarch64-linux-gnu-ar rcs libopen.a dev_open.o
`


### 3 、链接静态库，交叉编译ioctl_timer.c测试文件

```c
aarch64-linux-gnu-gcc -o ioctl_timer ioctl_timer.c -L./ -ltimer -lopen
```
> topeet@ubuntu:~/Linux/test/test_ming/36-ioctl_timer/app$ `aarch64-linux-gnu-gcc -o ioctl_timer ioctl_timer.c -L./ -ltimer -lopen`

> - **`-L./`**：告诉编译器在当前目录（`.`）查找库文件。`-L` **后面跟的是库文件搜索路径**。在这个例子中，我们指定了当前目录作为额外的库文件查找路径。
>     
> - **`-ltimer`** 和 **`-lopen`**：这两个选项用于链接静态或动态库。`-l` 选项后面跟随的是库的名字，但不包括开头的 `lib` 和结尾的 `.a` 或 `.so` 扩展名。
>     
>     - `-ltimer` 指示编译器链接名为 `libtimer.a` 或 `libtimer.so` 的库文件（如果它们存在于 `-L` 指定的目录中）。
>     - `-lopen` 则指示编译器寻找并链接名为 `libopen.a` 或 `libopen.so` 的库文件。



### 4 、




## 测试
> [root@topeet:~]# **insmod ioctl_timer.ko**
> [  331.183476] ioctl_timer: loading out-of-tree module taints kernel.
> [root@topeet:~]# [  331.184552] alloc_chrdev_region is ok
> [  331.184578] major is 236
> [  331.184590] minor is 0
> 
> [root@topeet:~]# **./ioctl_timer**
> [  336.771074] this is function test
> [  337.784407] this is function test
> [  338.797647] this is function test
> [  341.971165] this is function test
> [  345.171075] this is function test





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


