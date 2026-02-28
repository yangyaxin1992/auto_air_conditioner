1.安装环境：
1.1 jdk安装部署
    - 配置环境变量：右击“我的电脑”-->"属性"-->"高级系统设置"-->"高级"-->"环境变量" 
1）在系统变量里新建"JAVA_HOME"变量，变量值为：D:\Private\jdk_8u152（根据自己的jdk的安装路径填写）
2）在系统变量里新建"classpath"变量，变量值为：.;%JAVA_HOME%\lib;%JAVA_HOME%\lib\tools.jar 
3）找到path变量（已存在不用新建）添加变量值：%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin
    - 检查环境是否配置ok
“Windows+R”-->输入“cmd”-->Enter，输入java -version(记得中间有个空格)，如果显示jdk版本信息就说明环境变量配置成功了

1.2 安装python
    - 配置python环境变量 
方法1）在"Path"行，添加python安装路径即可(如，D:\Program Files\Python\Python37)
方法2）使用cmd命令添加path环境变量
在cmd下输入： path=%path%;D:\Program Files\Python\Python37  接着按"Enter"回车键 （D:\Program Files\Python\Python37是python安装目录）
     - 检查环境是否配置ok
设置成功以后，在cmd命令行，输入命令"python"，就可以有相关显示

1.3 安装allure
下载allure-commandline-2.13.0，解压放在某一目录下；
    -  配置allure环境变量
在path中添加： D:\Program Files\allure-commandline-2.13.0\allure-2.13.0\bin
    - 检查是否安装配置好：
在cmd中，输入allure --version

1.4 