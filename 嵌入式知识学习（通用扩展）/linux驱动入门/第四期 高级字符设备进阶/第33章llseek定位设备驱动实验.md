---
title: "{{title}}"
aliases: 
tags: 
description: 
source:
---

# 备注(声明)：
## 引入

> 将**两个字符串依次进行写入，并对写入完成的字符串进行读取**，如果仍采用之前的方式，第二次的写入值会覆盖第一次写入值，那要如何来实现上述功能呢？这就要轮到llseek出场了。



# 一、定位设备llseek

##  lseek函数 - 移动文件的读写位置。（应用层）
### 1 、函数原型：
```c
off_t lseek(int fd,off_t offset,int whence);
```


### 2 、头文件：
```d
#include <sys/types.h>
​#include <unistd.h>
```



### 3 、参数含义：
> fd: 文件描述符；
> 
> ​ off_t offset: **偏移量**，单位是字节的数量，可以正负，如果是**负值表示向前移动**；如果是正值，表示向后移动。
> 
> ​ whence：当前位置的基点，可以使用以下三组值。
> 
> ​ SEEK_SET：相对于文件**开头**
> 
> ​ SEEK_CUR:相对于当前的文件**读写指针位置**
> 
> ​ SEEK_END:相对于文件**末尾**




### 4 、函数返回值 - 成功返回当前位移大小，失败返回-1



### 5、函数使用示例：
- 1 把文件位置指针设置为5：
```c
lseek(fd,5,SEEK_SET);
```

- 1 把文件位置设置成文件末尾：
```c
lseek(fd,0,SEEK_END);
```


- 1 确定当前的文件位置：
```c
lseek(fd,0,SEEK_CUR);
```



### 6、


### 7、


### 8、



## 驱动程序的完善
### 1 、要做的工作
> lseek函数会调用file_operation结构体中的**llseek接口**，所以需要对驱动中的llseek函数进行填充，并且**完善read和write函数中偏移相关的部分**。

### 2 、llseek.c总代码
```c
#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/kdev_t.h>
#include <linux/uaccess.h>
#include <linux/atomic.h>



#define BUFSIZE 1024  //设置最大偏移量为1024
static char mem[BUFSIZE]={0};  //设置数据存储数组mem

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




static int cdev_test_open(struct inode *inode,struct file *file){

    // 设置私有数据为设备结构体地址，方便其他函数使用
    file->private_data=&dev1;

    printk("This is cdev_test_open\r\n");

    return 0;
}

static int cdev_test_release(struct inode *inode, struct file *file)
{
    printk("This is cdev_test_release\r\n");
    return 0;
}


static ssize_t cdev_test_write (struct file *file,const char __user *buf,size_t size,loff_t *off){

    loff_t p=*off; //将写入数据的偏移量赋值给loff_t类型变量p
    size_t count=size;

    if(p>BUFSIZE){
        return -1;

    }
    if(count>BUFSIZE-p){

        count=BUFSIZE-p; //如果要写入的偏移值超出剩余的空间，则写入到最后位置
    }

    //从'mem+p'位置开始写入buf，共count个字节
    if(copy_from_user(mem+p,buf,count)!=0){

        printk("copy_from_user  error\r\n");

        return -1;
    }

    printk("mem is %s,p is %llu\n",mem+p,p);//打印写入的值
    *off = *off + count;//更新偏移值

    return 0;
}


static ssize_t cdev_test_read (struct file *file, char __user *buf,size_t size,loff_t *off){


    loff_t p=*off; //将读取数据的偏移量赋值给loff_t类型变量p
    int i;
    size_t count=size;
    if(p>BUFSIZE){
        return -1;

    }
    if(count>BUFSIZE-p){

        count=BUFSIZE-p; //如果要读取的偏移值超出剩余的空间，则读取到最后位置
    }

    //将'mem+p'开始的count个字节复制到用户空间的buf中
    if(copy_to_user(buf,mem+p,count)!=0){

        printk("copy_from_user  error\r\n");

        return -1;
    }

    for(i=0;i<20;i++){

        printk("buf[%d] is %c",i,mem[i]);//将mem中的值打印出来

    }

   printk("mem is %s,p is %llu,count is %d\n",mem+p,p,count);
   *off=*off+count; //更新偏移值

    return 0;
}


static loff_t cdev_test_llseek(struct file *file,loff_t offset,int whence){

    loff_t new_offset; //定义loff_t类型的新的偏移值
    switch(whence){

        case SEEK_SET:
            if(offset<0){

                return -EINVAL;
                break;
            }
            if(offset>BUFSIZE){

                return -EINVAL;
                break;
            }
            new_offset=offset; //如果whence参数为SEEK_SET，则新偏移值为offset
            break;

        case SEEK_CUR:
            if(offset + file->f_pos < 0){

                return -EINVAL;
                break;
            }
            if(offset + file->f_pos > BUFSIZE){

                return -EINVAL;
                break;
            }
            //如果whence参数为SEEK_CUR，则新偏移值为file->f_pos + offset，file->f_pos为当前的偏移值
            new_offset=offset + file->f_pos;
            break;

        case SEEK_END:
            if(offset + file->f_pos<0){

                return -EINVAL;
                break;
            }
            //如果whence参数为SEEK_END，则新偏移值为BUFSIZE + offset，BUFSIZE为最大偏移量
            new_offset=offset + BUFSIZE;
            break;

        default:
            break;
    }

    file->f_pos=new_offset;//更新file->f_pos偏移值
    return new_offset;

}










struct file_operations cdev_test_fops={

    .owner = THIS_MODULE, //将owner字段指向本模块，可以避免在模块的操作正在被使用时卸载该模块
    .open=cdev_test_open,
    .read=cdev_test_read,
    .write=cdev_test_write,
    .llseek=cdev_test_llseek,
    .release=cdev_test_release

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


### 3 、llseek函数完善：
```c
static loff_t cdev_test_llseek(struct file *file,loff_t offset,int whence){

    loff_t new_offset; //定义loff_t类型的新的偏移值
    switch(whence){

        case SEEK_SET:
            if(offset<0){

                return -EINVAL;
                break;
            }
            if(offset>BUFSIZE){

                return -EINVAL;
                break;
            }
            new_offset=offset; //如果whence参数为SEEK_SET，则新偏移值为offset
            break;

        case SEEK_CUR:
            if(offset + file->f_pos < 0){

                return -EINVAL;
                break;
            }
            if(offset + file->f_pos > BUFSIZE){

                return -EINVAL;
                break;
            }
            //如果whence参数为SEEK_CUR，则新偏移值为file->f_pos + offset，file->f_pos为当前的偏移值
            new_offset=offset + file->f_pos;
            break;

        case SEEK_END:
            if(offset + file->f_pos<0){

                return -EINVAL;
                break;
            }
            //如果whence参数为SEEK_END，则新偏移值为BUFSIZE + offset，BUFSIZE为最大偏移量
            new_offset=offset + BUFSIZE;
            break;

        default:
            break;
    }

    file->f_pos=new_offset;//更新file->f_pos偏移值
    return new_offset;

}

```

> 在第4行使用switch语句对传递的whence参数进行判断，whence在这里可以有三个取值，分别为SEEK_SET、SEEK_CUR和SEEK_END。
> 
> 在6-16、17-28、29-38行代码中，分别对三个参数所代表的功能进行实现，其中需要注意的是file->f_pos指的是当前文件的偏移值。
> 
> 在第40行和41行分别对f_pos偏移值进行更新，对新的偏移值进行返回。



### 4 、write接口函数完善：
```c
static ssize_t cdev_test_write (struct file *file,const char __user *buf,size_t size,loff_t *off){

    loff_t p=*off; //将写入数据的偏移量赋值给loff_t类型变量p
    size_t count=size;

    if(p>BUFSIZE){
        return -1;

    }
    if(count>BUFSIZE-p){

        count=BUFSIZE-p; //如果要写入的偏移值超出剩余的空间，则写入到最后位置
    }

    //从'mem+p'位置开始写入buf，共count个字节
    if(copy_from_user(mem+p,buf,count)!=0){

        printk("copy_from_user  error\r\n");

        return -1;
    }

    printk("mem is %s,p is %llu\n",mem+p,p);//打印写入的值
    *off = *off + count;//更新偏移值

    return 0;
}
```

> 相较于之前的write接口函数，在第7行和第10行分别加入了对偏移值p和读取数量进行判定，在第13行通过**偏移值p**进行内核空间和用户空间数据的传递，最后在第18行对偏移值进行更新。


### 5、read接口函数完善
```c
static ssize_t cdev_test_read (struct file *file, char __user *buf,size_t size,loff_t *off){


    loff_t p=*off; //将读取数据的偏移量赋值给loff_t类型变量p
    int i;
    size_t count=size;
    if(p>BUFSIZE){
        return -1;

    }
    if(count>BUFSIZE-p){

        count=BUFSIZE-p; //如果要读取的偏移值超出剩余的空间，则读取到最后位置
    }

    //将'mem+p'开始的count个字节复制到用户空间的buf中
    if(copy_to_user(buf,mem+p,count)!=0){

        printk("copy_from_user  error\r\n");

        return -1;
    }

    for(i=0;i<20;i++){

        printk("buf[%d] is %c",i,mem[i]);//将mem中的值打印出来

    }

   printk("mem is %s,p is %llu,count is %d\n",mem+p,p,count);
   *off=*off+count; //更新偏移值

    return 0;
}
```

> 相较于之前的read接口函数，在第7行和第10行分别**加入了对偏移值p和读取数量进行判定**，在第13行通过偏移值p进行内核空间和用户空间数据的传递，最后在第21行对偏移值进行更新。


### 6、偏移量off（读写的起始位置）


### 7、


### 8、



## 编写应用测试代码llseek.c
### 1 、完整代码
```c
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>


int main(int argc,char *argv[]){

    int fd;
    unsigned int off;

    char readbuf[13]={0};
    char readbuf1[19]={0};

    fd = open("/dev/test",O_RDWR,666);//打开/dev/test设备
    if(fd < 0 ){
		printf("file open error \n");
	}

    write(fd,"hello word",13);//向fd写入数据hello world
    off = lseek(fd,0,SEEK_CUR);//读取当前位置的偏移量
    printf("off is %d\n",off);

    off=lseek(fd,0,SEEK_SET);//将偏移量设置为0
    printf("off is %d\n",off);

    read(fd,readbuf,sizeof(readbuf));//将写入的数据读取到readbuf缓冲区 hello word
    printf("read is %s\n",readbuf);

    off = lseek(fd,0,SEEK_CUR);//读取当前位置的偏移量
    printf("off is %d\n",off);




    off=lseek(fd,-1,SEEK_CUR);//将当前位置的偏移量向前挪动一位
    printf("off is %d\n",off);

    write(fd,"Linux",6);//向fd写入数据Linux
    off = lseek(fd,0,SEEK_CUR);//读取当前位置的偏移量
    printf("off is %d\n",off);

    off=lseek(fd,0,SEEK_SET);//将偏移量设置为0
    printf("off is %d\n",off);

    read(fd,readbuf1,sizeof(readbuf1));//将写入的数据读取到readbuf1缓冲区  hello worlLinux
    printf("read is %s\n",readbuf1);

    off = lseek(fd,0,SEEK_CUR);//读取当前位置的偏移量
    printf("off is %d\n",off);

    close(fd);

    return 0;

}

```


### 2 、


### 3 、



### 4 、



### 5、


### 6、


### 7、


### 8、

## 测试
### 1 、运行测试
> [root@topeet:~]# `insmod llseek.ko`
> [  250.383570] llseek: loading out-of-tree module taints kernel.
> [root@topeet:~]# [  250.384660] alloc_chrdev_region is ok
> [  250.384698] major is 236
> [  250.384710] minor is 0
> 
> [root@topeet:~]# `./lseek`
> [  257.072929] This is cdev_test_open
> [  257.073046] mem is heloff is 13
> off is 0
> lo read is hello word
> off is 13
> off is 12
> off is 18
> off is 0
> read is hello word
> off is 19
> word,p is 0
> [root@topeet:~]# [  257.074980] buf[0] is h
> [  257.074982] buf[1] is e
> [  257.075004] buf[2] is l
> [  257.075016] buf[3] is l
> [  257.075025] buf[4] is o
> [  257.075035] buf[5] is
> [  257.075046] buf[6] is w
> [  257.075055] buf[7] is o
> [  257.075065] buf[8] is r
> [  257.075076] buf[9] is d
> [  257.075086] buf[10] is
> [  257.075096] buf[11] is
> [  257.075106] buf[12] is
> [  257.075115] buf[13] is
> [  257.075125] buf[14] is
> [  257.075134] buf[15] is
> [  257.075165] buf[16] is
> [  257.075172] buf[17] is
> [  257.075178] buf[18] is
> [  257.075186] buf[19] is
> [  257.075201] mem is hello word,p is 0,count is 13
> [  257.078870] mem is Linux,p is 12
> [  257.080682] buf[0] is h
> [  257.080684] buf[1] is e
> [  257.080698] buf[2] is l
> [  257.080709] buf[3] is l
> [  257.080719] buf[4] is o
> [  257.080731] buf[5] is
> [  257.080736] buf[6] is w
> [  257.080745] buf[7] is o
> [  257.080756] buf[8] is r
> [  257.080765] buf[9] is d
> [  257.080775] buf[10] is
> [  257.080785] buf[11] is
> [  257.080795] buf[12] is L
> [  257.080803] buf[13] is i
> [  257.080813] buf[14] is n
> [  257.080822] buf[15] is u
> [  257.080831] buf[16] is x
> [  257.080840] buf[17] is
> [  257.080849] buf[18] is
> [  257.080858] buf[19] is
> [  257.080868] mem is hello word,p is 0,count is 19
> [  257.083384] This is cdev_test_release
> 




### 2 、


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


