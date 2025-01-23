# 使用说明

1. 下载代码，解压到任意目录
2. 确保你是windows10操作系统和python环境3.10
3. 进入到项目的cmd目录下，修改lw.bat文件：
   1. 将python路径修改为你的python路径
   2. 将.py文件路径修改为你的.py路径
   3. 别忘了最后还有一个 %*
   4. ```cmd
      python.exe解释器 _main.py脚本 %*
4. 进入到你所设置的python环境中，安装相关的python环境。例如：
   1. conda activate home
   2. pip install -r requirements.txt
5. (可选) 将.bat加入到你的环境变量中，这样就可以直接在windows中使用了.

## 开始使用
### 打开cmd
1. 输入：
   lw ls
2. 查看当前所有创建的标题
<br><br>
3. 输入：
   lw size 某个窗口标题 600x500
4. 则会把这个窗口设置为宽600 高500, 且居中显示
<br><br>
5. 输入：
   lw move 某个窗口标题 100 100
6. 则会把这个窗口移动到屏幕的(100,100)位置
<br><br><br>
### 参考命令如下：
```lw
lw
lw ls   (lw list)
lw h    (lw help)
lw get
lw size 窗口标题 600x500
lw size 窗口标题 4
lw move 窗口标题 100 100
lw move 窗口标题 5

   