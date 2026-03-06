本文介绍了一个通讯管理系统，涵盖了添加联系人、显示信息、删除与查找功能，以及清空和退出操作。通过结构体和函数实现，适合管理个人或团队通讯信息。


# 1、系统需求

说明： 通讯录 是一个可以记录亲人、好友信息的工具

系统所需要的功能：

- （1）添加联系人：向通讯录添加新人，信息包括（姓名、性别、年龄、联系电话、家庭住址）.
- （2）显示联系人：显示通讯录中记录联系人信息
- （3）删除联系人：按照姓名进行删除指定联系人
- （4）查找联系人：按照姓名查看指定联系人信息
- （5）修改联系人：按照姓名重新修改指定联系人
- （6）清空联系人：清空通讯录所有信息
- （7）退出通讯录：退出当前使用的通讯录

# 2、菜单功能

作用：用户选择功能界面

步骤：

- 封装函数显示该界面：showMenu()
- 在 main 函数中调用
```c
cout << "\t\t||-------------------------||"<< endl;
    cout << "\t\t||       通讯录管理系统    ||" << endl;
    cout << "\t\t||-------------------------||" << endl;
    cout << "\t\t*****************************" << endl;
    cout << "\t\t*****   1、添加联系人   *****"<< endl;
    cout << "\t\t*****   2、显示联系人   *****" << endl;
    cout << "\t\t*****   3、删除联系人   *****" << endl;
    cout << "\t\t*****   4、查找联系人   *****" << endl;
    cout << "\t\t*****   5、修改联系人   *****" << endl;
    cout << "\t\t*****   6、清空联系人   *****" << endl;
    cout << "\t\t*****   0、退出通讯录   *****" << endl;
    cout << "\t\t*****************************" << endl;
c123456789101112
```

# 3、退出功能

作用：退出通讯录系统

```c
//退出通讯录
            case 0: cout << "欢迎下次再来，拜拜！！！" << endl;
                system("pause");
                return 0;
                break;
c12345
```

# 4、添加联系人

作用：实现添加联系人功能，联系人上限为1000人，联系人信息包括（姓名、性别、年龄、联系电话、家庭住址）

添加联系人步骤：

- （1）设计联系人结构体
- （2）设计通讯录结构体
- （3）main函数创建通讯录
- （4）封装添加联系人函数
- （5）测试添加联系人功能

## 4.1 设计联系人结构体

```c
//联系人结构体
struct Person
{
    string m_Name;//姓名
    //1、男；2、女
    int m_Sex;//性别
    int m_Age;//年龄
    string m_phone;//电话
    string m_Addr;//住址
};
c12345678910
```

## 4.2 设计通讯录结构体

```c
//通讯录结构体
struct Addressbooks
{
    struct Person person[Max];
    int m_size;//通讯成员个数
};
c123456
```

## 4.3 main函数创建通讯录

```c
case 1: addPerson(&abs);//地址传递，修改形参
                break;
c12
```

## 4.4 封装添加联系人函数

```c
//1、添加联系人
void addPerson(struct Addressbooks *abs)//利用指针接收地址
{
    //判断通讯录是否已满，如果满了就不要添加
    if (abs->m_size == Max)
    {
        cout << "通讯录已满，添加失败！" << endl;
    }
    else
    {
        //姓名
        string name;
        cout << "请输入姓名：" << endl;
        cin >> name;
        abs->person[abs->m_size].m_Name = name;
        //性别
        cout << "请输入性别：" << endl;
        cout << "1----代表男" << endl;
        cout << "2----代表女" << endl;
        int sex=0;    
        while(true) 
        {
            cin >> sex;
            if (sex == 1 || sex == 2)
            {
                abs->person[abs->m_size].m_Sex = sex;
                if (sex == 1)
                    cout << "你输入通讯录联系人的性别是-男" << endl;
                else if(sex==2)
                    cout << "你输入通讯录联系人的性别是-女" << endl;
                break;
            }
            else
            {
                cout << "性别输入有误，请重新输入！！" << endl;
            }
        }
        //年龄
        cout << "请输入年龄：" << endl;
        int age;
        while (true)
        {
            cin >> age;
            if (age > 0 && age < 100)
            {
                abs->person[abs->m_size].m_Age = age;
                break;
            }    
            else
                cout << "你输入的年龄有误，请重新输入：" << endl;
        }
        //电话
        cout << "请输入电话：" << endl;
        string phone;
        while (true)
        {
            cin >> phone;
            if (phone[0] != '1')
            {
                cout << "你输入的电话号码不是1开头，请重新输入！" << endl;
                continue;
            }
            abs->person[abs->m_size].m_phone = phone;
            break;
        }
        //地址
        cout << "请输入地址：" << endl;
        string add;
        cin >> add;
        abs->person[abs->m_size].m_Addr = add;
        //更新通讯录人数
        abs->m_size++;
        cout << "通讯录联系人添加成功！！";
        system("pause");//按任意键继续
        system("cls");//清屏操作
    }
}
c1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖通讯管理系统——C++入门项目/c13d02b9c02a1a49b1a8d50aea211e51\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖通讯管理系统——C++入门项目/c13d02b9c02a1a49b1a8d50aea211e51_MD5.png)

# 5、显示联系人

作用：显示通讯录已有的联系人信息

显示联系人步骤：

- 封装显示联系人函数
- 测试显示联系人功能
```c
void showPerson(Addressbooks *abs)
{
    //判断通讯录人数是否为0，如果是0，提示为空
    //如果不为0显示联系人
    if (abs->m_size == 0)
    {
        cout << "当前记录为空！！" << endl;
    }
    else
    {
        for (int i = 0; i < abs->m_size; i++)
        {
            cout << "姓名： " << abs->person[i].m_Name << "\t";
            cout << "性别： " << (abs->person[i].m_Sex==1?"男":"女") << "\t";
            cout << "年龄： " << abs->person[i].m_Age << "\t";
            cout << "电话： " << abs->person[i].m_phone << "\t";
            cout << "住址： " << abs->person[i].m_Addr << endl;
        }
    }
    system("pause");
    system("cls");
}
c12345678910111213141516171819202122
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖通讯管理系统——C++入门项目/e1d0331eb548424f092fb0b945224afe\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖通讯管理系统——C++入门项目/e1d0331eb548424f092fb0b945224afe_MD5.png)

# 6、删除联系人

作用：按照姓名删除联系人

步骤：

- （1）封装检测联系人是否存在
- （2）封装删除联系人函数
- （3）测试删除联系人功能

## 6.1 检测联系人是否存在

说明：检测联系人是否存在，如果存在，返回联系人所在数组具体位置，不存在返-1

```c
int isExist(Addressbooks *abs, string name)
{
    for (int i = 0; i < abs->m_size; i++)
    {
        //找到用户的姓名
        if (abs->person[i].m_Name == name)
        {
            return i;
        }
    }
    return -1;
}
c123456789101112
```

## 6.2 封装删除联系人函数

```c
void deletePerson(Addressbooks * abs)
{
    cout << "请输入要删除联系人的姓名：" << endl;
    string name;
    cin >> name;
    int ret=isExist(abs, name);
    if (ret == -1)
    {
        cout << "通讯录无该联系人记录！！" << endl;
    }
    else
    {
        for (int i = ret; i < abs->m_size; i++)
        {
            //数据前移
            abs->person[i] = abs->person[i + 1];
        }
        abs->m_size--;
        cout << "删除成功！！！" << endl;
    }
    system("pause");
    system("cls");
}
c1234567891011121314151617181920212223
```

# 7、查找联系人

作用：按照姓名查找指定联系人信息

```c
void findPerson(Addressbooks *abs)
{
    cout << "请输入你要查找的联系人：" << endl;
    string name;
    cin >> name;
    //判断联系人是否存在通讯录
    int ret = isExist(abs, name);
    if (ret == -1)
    {
        cout << "对不起，通讯录无此人！！" << endl;
    }
    else
    {
        cout << "姓名： " << abs->person[ret].m_Name << "\t";
        cout << "性别： " << (abs->person[ret].m_Sex==1?"男":"女") << "\t";
        cout << "年龄： " << abs->person[ret].m_Age << "\t";
        cout << "电话： " << abs->person[ret].m_phone << "\t";
        cout << "住址： " << abs->person[ret].m_Addr << endl;
    }
    system("pause");
    system("cls");
}
c12345678910111213141516171819202122
```

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖通讯管理系统——C++入门项目/d3760772301d9805c27722a49a453c77\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖通讯管理系统——C++入门项目/d3760772301d9805c27722a49a453c77_MD5.png)

# 8、修改联系人

作用：按照姓名重新修改指定联系人

```c
void modifyPerson(Addressbooks * abs)
{
    cout << "请输入要修改联系人的姓名：" << endl;
    string name;
    cin >> name;
    int ret = isExist(abs, name);
    if (ret == -1)
    {
        cout << "对不起，你所要修改的联系人并不在此通讯录！！" << endl;

    }
    else
    {
        string name;
        cout << "请重新输入要修改的姓名：" << endl;
        cin >> name;
        abs->person[ret].m_Name = name;
        int sex;
        cout << "请重新输入要修改的性别：" << endl;
        while (true)
        {
            cin >> sex;
            if (sex == 1 || sex == 2)
            {
                abs->person[ret].m_Sex = sex;
                break;
            }
            else
            {
                cout << "你输入的有误，请重新输入：" << endl;
            }
                
        }
        int age;
        cout << "请重新输入要修改的年龄：" << endl;
        cin >> age;
        abs->person[ret].m_Age = age;
        string phone;
        cout << "请重新输入要修改的电话：" << endl;
        cin >> phone;
        abs->person[ret].m_phone = phone;
        string addre;
        cout << "请重新输入要修改的地址：" << endl;
        cin >> addre;
        abs->person[ret].m_Addr = addre;
        cout << "修改成功了！！" << endl;
    }
    system("pause");
    system("cls");
}
c1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950
```

添加信息：

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖通讯管理系统——C++入门项目/a7e3bc2680d81633506e8563b86382a7\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖通讯管理系统——C++入门项目/a7e3bc2680d81633506e8563b86382a7_MD5.png)

修改联系人：  
![XGRIDS/高通平台开发/📒C++编程入门/assets/📖通讯管理系统——C++入门项目/23c2066f850012d7307c3d79cc5f4686\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖通讯管理系统——C++入门项目/23c2066f850012d7307c3d79cc5f4686_MD5.png)

修改之后联系人：

![XGRIDS/高通平台开发/📒C++编程入门/assets/📖通讯管理系统——C++入门项目/f17475335eaa1e7efbb7898275b476f9\_MD5.png](嵌入式知识学习（通用扩展）/linux基础知识/📒C++编程入门/assets/📖通讯管理系统——C++入门项目/f17475335eaa1e7efbb7898275b476f9_MD5.png)

# 9 清空通讯录

```c
void cleanPerson(Addressbooks * abs)
{
    cout << "你是否一定要清空：是输入：Y/y，否输入：N/n" << endl;
    char ch;
    while (true)
    {
        cin >> ch;
        if (ch == 'Y' || ch == 'y')
        {
            //将当期记录联系人数量置为0，做逻辑清空操作
            abs->m_size = 0;
            cout << "通讯录已经清空！" << endl;
            break;
        }
        else if (ch == 'N' || ch == 'n')
        {
            cout << "请重新操作：" << endl;
            break;
        }
        else
        {
            cout << "输入错误，请重新输入：" << endl;
        }
    }
    system("pause");
    system("cls");
}
c123456789101112131415161718192021222324252627
```

# 10 全部代码

```c
#include<iostream>
#include<string>
#define Max 10000
using namespace std;
//联系人结构体
struct Person
{
    string m_Name;//姓名
    //1、男；2、女
    int m_Sex;//性别
    int m_Age;//年龄
    string m_phone;//电话
    string m_Addr;//住址
};
//通讯录结构体
struct Addressbooks
{
    struct Person person[Max];
    int m_size;//通讯成员个数
};
//1、添加联系人
void addPerson(struct Addressbooks *abs)//利用指针接收地址
{
    //判断通讯录是否已满，如果满了就不要添加
    if (abs->m_size == Max)
    {
        cout << "通讯录已满，添加失败！" << endl;
    }
    else
    {
        //姓名
        string name;
        cout << "请输入姓名：" << endl;
        cin >> name;
        abs->person[abs->m_size].m_Name = name;
        //性别
        cout << "请输入性别：" << endl;
        cout << "1----代表男" << endl;
        cout << "2----代表女" << endl;
        int sex=0;    
        while(true) 
        {
            cin >> sex;
            if (sex == 1 || sex == 2)
            {
                abs->person[abs->m_size].m_Sex = sex;
                if (sex == 1)
                    cout << "你输入通讯录联系人的性别是-男" << endl;
                else if(sex==2)
                    cout << "你输入通讯录联系人的性别是-女" << endl;
                break;
            }
            else
            {
                cout << "性别输入有误，请重新输入！！" << endl;
            }
        }
        //年龄
        cout << "请输入年龄：" << endl;
        int age;
        while (true)
        {
            cin >> age;
            if (age > 0 && age < 100)
            {
                abs->person[abs->m_size].m_Age = age;
                break;
            }    
            else
                cout << "你输入的年龄有误，请重新输入：" << endl;
        }
        //电话
        cout << "请输入电话：" << endl;
        string phone;
        while (true)
        {
            cin >> phone;
            if (phone[0] != '1')
            {
                cout << "你输入的电话号码不是1开头，请重新输入！" << endl;
                continue;
            }
            abs->person[abs->m_size].m_phone = phone;
            break;
        }
        //地址
        cout << "请输入地址：" << endl;
        string add;
        cin >> add;
        abs->person[abs->m_size].m_Addr = add;
        //更新通讯录人数
        abs->m_size++;
        cout << "通讯录联系人添加成功！！";
        system("pause");//按任意键继续
        system("cls");//清屏操作
    }
}
// 2、显示联系人 
void showPerson(Addressbooks *abs)
{
    //判断通讯录人数是否为0，如果是0，提示为空
    //如果不为0显示联系人
    cout <<"编号\t"<< "姓名\t" << "性别\t" << "年龄\t" << "电话\t" << "住址\t" << endl << endl;
    if (abs->m_size == 0)
    {
        cout << "当前记录为空！！" << endl;
    }
    else
    {
        for (int i = 0; i < abs->m_size; i++)
        {
            cout << i+1<<"\t"<<abs->person[i].m_Name << "\t" << (abs->person[i].m_Sex == 1 ? "男" : "女") << "\t" 
                << abs->person[i].m_Age << "\t" << abs->person[i].m_phone << "\t" << abs->person[i].m_Addr << endl;
        }
    }
    system("pause");
    system("cls");
}
//菜单界面
void showMenu()
{
    cout << "\t\t||-------------------------||"<< endl;
    cout << "\t\t||       通讯录管理系统    ||" << endl;
    cout << "\t\t||-------------------------||" << endl;
    cout << "\t\t*****************************" << endl;
    cout << "\t\t*****   1、添加联系人   *****"<< endl;
    cout << "\t\t*****   2、显示联系人   *****" << endl;
    cout << "\t\t*****   3、删除联系人   *****" << endl;
    cout << "\t\t*****   4、查找联系人   *****" << endl;
    cout << "\t\t*****   5、修改联系人   *****" << endl;
    cout << "\t\t*****   6、清空联系人   *****" << endl;
    cout << "\t\t*****   0、退出通讯录   *****" << endl;
    cout << "\t\t*****************************" << endl;
}
//检测联系人是否存在，如果存在，返回联系人所在数组具体位置，不存在返-1
int isExist(Addressbooks *abs, string name)
{
    for (int i = 0; i < abs->m_size; i++)
    {
        //找到用户的姓名
        if (abs->person[i].m_Name == name)
        {
            return i;
        }
    }
    return -1;
}
//删除指定联系人
void deletePerson(Addressbooks * abs)
{
    cout << "请输入要删除联系人的姓名：" << endl;
    string name;
    cin >> name;
    int ret=isExist(abs, name);
    if (ret == -1)
    {
        cout << "通讯录无该联系人记录！！" << endl;
    }
    else
    {
        for (int i = ret; i < abs->m_size; i++)
        {
            //数据前移
            abs->person[i] = abs->person[i + 1];
        }
        abs->m_size--;
        cout << "删除成功！！！" << endl;
    }
    system("pause");
    system("cls");
}
//查找指定联系人
void findPerson(Addressbooks *abs)
{
    cout << "请输入你要查找的联系人：" << endl;
    string name;
    cin >> name;
    //判断联系人是否存在通讯录
    int ret = isExist(abs, name);
    if (ret == -1)
    {
        cout << "对不起，通讯录无此人！！" << endl;
    }
    else
    {
        cout << "姓名： " << abs->person[ret].m_Name << "\t";
        cout << "性别： " << (abs->person[ret].m_Sex==1?"男":"女") << "\t";
        cout << "年龄： " << abs->person[ret].m_Age << "\t";
        cout << "电话： " << abs->person[ret].m_phone << "\t";
        cout << "住址： " << abs->person[ret].m_Addr << endl;
    }
    system("pause");
    system("cls");
}
//修改指定的联系人的信息
void modifyPerson(Addressbooks * abs)
{
    cout << "请输入要修改联系人的姓名：" << endl;
    string name;
    cin >> name;
    int ret = isExist(abs, name);
    if (ret == -1)
    {
        cout << "对不起，你所要修改的联系人并不在此通讯录！！" << endl;

    }
    else
    {
        string name;
        cout << "请重新输入要修改的姓名：" << endl;
        cin >> name;
        abs->person[ret].m_Name = name;
        int sex;
        cout << "请重新输入要修改的性别：" << endl;
        while (true)
        {
            cin >> sex;
            if (sex == 1 || sex == 2)
            {
                abs->person[ret].m_Sex = sex;
                break;
            }
            else
            {
                cout << "你输入的有误，请重新输入：" << endl;
            }
                
        }
        int age;
        cout << "请重新输入要修改的年龄：" << endl;
        cin >> age;
        abs->person[ret].m_Age = age;
        string phone;
        cout << "请重新输入要修改的电话：" << endl;
        cin >> phone;
        abs->person[ret].m_phone = phone;
        string addre;
        cout << "请重新输入要修改的地址：" << endl;
        cin >> addre;
        abs->person[ret].m_Addr = addre;
        cout << "修改成功了！！" << endl;
    }
    system("pause");
    system("cls");
}
//清空所有联系人
void cleanPerson(Addressbooks * abs)
{
    cout << "你是否一定要清空：是输入：Y/y，否输入：N/n" << endl;
    char ch;
    while (true)
    {
        cin >> ch;
        if (ch == 'Y' || ch == 'y')
        {
            //将当期记录联系人数量置为0，做逻辑清空操作
            abs->m_size = 0;
            cout << "通讯录已经清空！" << endl;
            break;
        }
        else if (ch == 'N' || ch == 'n')
        {
            cout << "请重新操作：" << endl;
            break;
        }
        else
        {
            cout << "输入错误，请重新输入：" << endl;
        }
    }
    system("pause");
    system("cls");
}
int main()
{
    system("color 5E");
    int select;
    //创建通讯录结构体变量
    Addressbooks abs;
    //初始化通讯录中的个数
    abs.m_size = 0;
    cout << "我是贾维斯，欢迎来到通讯管理系统！" << endl;
    while (true)
    {
        //显示菜单
        showMenu();
        //输入需要选择的功能
        cout << "请输入你要选择的操作：" << endl;
        
        cin >> select;
        switch (select)
        {
            //添加联系人
            case 1: addPerson(&abs);//地址传递，修改形参
                break;
            //显示联系人
            case 2: showPerson(&abs);
                break;
            //删除联系人
            case 3: deletePerson(&abs);
                break;
            //查找联系人
            case 4: findPerson(&abs);
                break;
            //修改联系人
            case 5: modifyPerson(&abs);
                break;
            //清空联系人
            case 6: cleanPerson(&abs);
                break;
            //退出通讯录
            case 0: cout << "欢迎下次再来，拜拜！！！" << endl;
                system("pause");
                return 0;
                break;
            default: cout << "你输入的不规范，请重新输入" << endl;
                break;
        }
    }

    system("pause");
    return 0;
}
```
