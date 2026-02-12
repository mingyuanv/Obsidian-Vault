---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：



# 一、 ioctl基础

## 应用层 - 向设备发送控制和配置命令。
### 1 、函数原型
```c
#include <sys/ioctl.h>

int ioctl(int fd, unsigned int cmd, unsigned long args);
```

#### 参数含义
> fd ：是用户程序打开设备时返回的文件描述符
> 
> cmd ：是用户程序对设备的控制命令，
> 
> args：应用程序向驱动程序**下发的参数**，如果传递的参数为**指针类型，则可以接收驱动向用户空间传递的数据**（在下面的实验中会进行使用）
> 




### 2 、cmd 4段位域含义
> cmd[31:30]—数据（args）的传输方向（**读写**）
> 
> ​ cmd[29:16]—数据（args）的**大小**
> 
> ​ cmd[15:8]—>**命令的类型**，可以理解成命令的密钥，一般为ASCII码（0-255的一个字符，有部分字符已经被占用，每个字符的序号段可能部分被占用）
> 
> ​ cmd[7:0] —>**命令的序号**，是一个8bits的数字（序号，0-255之间）


### 3 、四个合成宏 定义如下所示：

#### 定义一个命令，但是不需要参数：
```d
#define _IO(type,nr) _IOC(_IOC_NONE,(type),(nr),0)
```


#### 定义一个命令，应用程序从驱动程序读参数：
```d
#define _IOR(type,nr,size) _IOC(_IOC_READ,(type),(nr),(_IOC_TYPECHECK(size)))
```


#### 定义一个命令，应用程序向驱动程序写参数：
```d
#define _IOW(type,nr,size) _IOC(_IOC_WRITE,(type),(nr),(_IOC_TYPECHECK(size)))
```


#### 定义一个命令，参数是双向传递的：
```d
#define _IOWR(type,nr,size) _IOC(_IOC_READ|_IOC_WRITE,(type),(nr),(_IOC_TYPECHECK(size)))
```

#### 宏定义参数说明如下所示：
> type：命令的类型，一般为一个ASCII码值，一个驱动程序一般使用一个type
> 
> ​ nr：该命令下序号。一个驱动有多个命令，一般他们的type，序号不同
> 
> ​ size：**args的类型**
> 

#### 举例：用合成宏定义cmd命令
```d 
#define CMD_TEST0 _IO('L',0)        //不需要参数

#define CMD_TEST1 _IOR('L',1,int)   //向驱动程序读参数

#define CMD_TEST2 _IOW('L',2,int)    //向驱动程序写参数
```



### 4 、用户层与内核层使用相同的宏定义



### 5、






## 驱动层
### 1 、应用程序中ioctl函数会调用file_operation结构体中的unlocked_ioctl接口
```c
long (*unlocked_ioctl)(struct file *file,unsigned int cmd,unsigned long arg);
```

> file：文件描述符。
> 
> ​ cmd：与应用程序的cmd参数对应，在驱动程序中对传递来的cmd参数进行判断从而做出不同的动作。
> 
> ​ arg：与应用程序的arg参数对应，从而实现内核空间和用户空间参数的传递。

### 2 、实例
```c
#define CMD_SWITCH_STATE _IOW('A',0,int) // 用户空间命令：切换GPIO状态
#define CMD_GET_STATE _IOR('A',1,int)    // 用户空间命令：获取GPIO状态

// 设备控制函数，处理来自用户空间的命令
static long rs485_ioctrl(struct file *file, unsigned int cmd, unsigned long args) {
    int state;
    int ret;
    switch (cmd) {
        case CMD_SWITCH_STATE:
            if (copy_from_user(&state, (int __user *)args, sizeof(int))) { // 从用户空间复制数据到内核空间
                ret = -EFAULT;
                break;
            }
            gpiod_set_value(ctrl_gpio, state); // 设置GPIO值
            break;
        case CMD_GET_STATE:
            state = gpiod_get_value(ctrl_gpio); // 获取GPIO值
            if (copy_to_user((int __user *)args, &state, sizeof(int))) { // 将内核空间的数据复制到用户空间
                ret = -EFAULT;
            }
            break;
        default:
            return -1; // 对于未知命令返回错误
    }
    return 0;
}
```




### 3 、






# 二、IOCTL驱动传参实验

##  驱动程序编写
### 1 、unlocked_ioctl函数的实现
```c
#define CMD_TEST0 _IO('L',0)
#define CMD_TEST1 _IOW('L',1,int)
#define CMD_TEST2 _IOR('L',2,int)


static long cdev_test_ioctl(struct file *file,unsigned int cmd,unsigned long arg){

    int val; //定义int类型向应用空间传递的变量val
    switch(cmd){

        case CMD_TEST0:
            printk("this is CMD_TEST0\n");
            break;

        case CMD_TEST1:

            printk("this is CMD_TEST1\n");
			printk("arg is %ld\n",arg);//打印应用空间传递来的arg参数
            break;;

        case CMD_TEST2:

            val=1;
            printk("this is CMD_TEST2\n");
            if(copy_to_user((int *)arg,&val,sizeof(val))!=0){

                printk("copy_to_user error \n");	
            }
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


#define CMD_TEST0 _IO('L',0)
#define CMD_TEST1 _IOW('L',1,int)
#define CMD_TEST2 _IOR('L',2,int)

struct device_test{

    dev_t dev_num;//设备号
    int major;  
    int minor;

    struct cdev cdev_test;  // 字符设备结构体
    struct class *class;    // 类指针
    struct device *device;  // 设备指针

    char kbuf[32];  // 内核缓冲区,存放数据


};
// 实例化一个设备结构体变量
struct device_test dev1;


static long cdev_test_ioctl(struct file *file,unsigned int cmd,unsigned long arg){

    int val; //定义int类型向应用空间传递的变量val
    switch(cmd){

        case CMD_TEST0:
            printk("this is CMD_TEST0\n");
            break;

        case CMD_TEST1:

            printk("this is CMD_TEST1\n");
			printk("arg is %ld\n",arg);//打印应用空间传递来的arg参数
            break;;

        case CMD_TEST2:

            val=1;
            printk("this is CMD_TEST2\n");
            if(copy_to_user((int *)arg,&val,sizeof(val))!=0){

                printk("copy_to_user error \n");	
            }
            break;

        default:
            break;

        
    }

    return 0;

}





struct file_operations cdev_test_fops={

    .owner = THIS_MODULE, //将owner字段指向本模块，可以避免在模块的操作正在被使用时卸载该模块
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





##  编写测试 APP
### 1 、测试代码ioctl.c
```c
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <string.h>

#define CMD_TEST0 _IO('L',0)
#define CMD_TEST1 _IOW('L',1,int)
#define CMD_TEST2 _IOR('L',2,int)


int main(int argc,char *argv[]){

    int fd;
    int val;

    //使用非阻塞的方式打开设备
    fd = open("/dev/test",O_RDWR);//打开/dev/test设备
    if(fd < 0 ){
		printf("file open error \n");
	}

    if(!strcmp(argv[1],"write")){

        //如果第二个参数为write，向内核空间写入1
        ioctl(fd,CMD_TEST1,1);
    }
    else if(!strcmp(argv[1],"read")){

        //如果第二个参数为read，则读取内核空间传递向用户空间传递的值
        ioctl(fd,CMD_TEST2,&val);
        printf("val is %d\n",val);

    }


    close(fd);

    return 0;

}
```

### 2 、






## 测试
### 1 、运行测试
> [root@topeet:~]# `insmod ioctl.ko`
> [root@topeet:/]# [  138.303614] ioctl: loading out-of-tree module taints kernel.
> [  138.304648] alloc_chrdev_region is ok
> [  138.304679] major is 236
> [  138.304692] minor is 0
> 
> [root@topeet:~]# `./ioctl write`
> [  216.092011] this is CMD_TEST1
> [  216.092100] arg is 1
> [root@topeet:~]# `./ioctl read`
> [  221.441715] this is CMD_TEST2
> val is 1
> 

### 2 、




# 三、IOCTL地址传参实验

## 编写测试 APP
### 1 、总代码
```c
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <stdlib.h>

#define CMD_TEST0 _IOW('L',1,int)

//定义要传递的结构体
struct args{

    int a;
    int b;
    int c;

};


int main(int argc,char *argv[]){

    int fd;

    //定义args*类型的结构体变量test
    struct args *test;
    test=(struct args *)malloc(sizeof(struct args));


	test->a = 1;
	test->b = 2;
	test->c = 3;



    //使用非阻塞的方式打开设备
    fd = open("/dev/test",O_RDWR,0777);//打开/dev/test设备
    if(fd < 0 ){
		printf("file open error \n");
	}

    //使用ioctl函数传递结构体变量test(地址)
    ioctl(fd,CMD_TEST0,test);



    close(fd);

    return 0;

}
```

### 2 、






## 驱动程序编写
### 1 、unlocked_ioctl函数的实现
```c
static long cdev_test_ioctl(struct file *file,unsigned int cmd,unsigned long arg){

    struct args *test;
    //在尝试使用 copy_from_user 函数之前，你需要确保这个指针指向有效的内存地址。
    test=(struct args *)kmalloc(sizeof(struct args),GFP_KERNEL);


    switch(cmd){

        case CMD_TEST0:

            //将用户空间传递来的arg赋值给test
            if(copy_from_user(test,(struct args  *)arg,sizeof(test))!=0){

                printk("copy_from_user error \n");	
            }

            //对传递的值进行打印验证
			printk("a = %d\n",test->a);
  			printk("b = %d\n",test->b);
  	  		printk("c = %d\n",test->c);

            break;


        default:
            break;
        
    }


    return 0;
}

```

### 2 、总代码
```c
#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/kdev_t.h>
#include <linux/uaccess.h>
#include <linux/slab.h>


#define CMD_TEST0 _IOW('L',1,int)

struct args{

    int a;
    int b;
    int c;

};


struct device_test{

    dev_t dev_num;//设备号
    int major;  
    int minor;

    struct cdev cdev_test;  // 字符设备结构体
    struct class *class;    // 类指针
    struct device *device;  // 设备指针

    char kbuf[32];  // 内核缓冲区,存放数据


};
// 实例化一个设备结构体变量
struct device_test dev1;


static long cdev_test_ioctl(struct file *file,unsigned int cmd,unsigned long arg){

    struct args *test;
    //在尝试使用 copy_from_user 函数之前，你需要确保这个指针指向有效的内存地址。
    test=(struct args *)kmalloc(sizeof(struct args),GFP_KERNEL);


    switch(cmd){

        case CMD_TEST0:

            //将用户空间传递来的arg赋值给test
            if(copy_from_user(test,(struct args  *)arg,sizeof(test))!=0){

                printk("copy_from_user error \n");	
            }

            //对传递的值进行打印验证
			printk("a = %d\n",test->a);
  			printk("b = %d\n",test->b);
  	  		printk("c = %d\n",test->c);

            break;


        default:
            break;
        
    }


    return 0;
}





struct file_operations cdev_test_fops={

    .owner = THIS_MODULE, //将owner字段指向本模块，可以避免在模块的操作正在被使用时卸载该模块
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






## 测试
### 1 、运行测试
> [root@topeet:~]# insmod ioctl.ko
[ 1875.734112] alloc_chrdev_region is ok
[ 1875.737840] major is 236
[ 1875.740545] minor is 0
[root@topeet:~]# ./ioctl
[ 1881.316493] a = 1
[ 1881.318581] b = 2
[ 1881.320514] c = 0


### 2 、


### 3 、不建议动态分配内存，考虑在栈上直接定义一个 `struct args` 变量，而不是指针。



### 4 、




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


