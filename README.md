# LyzWindows

修改时间：——2025-01-22 16:47:18 <br>

这是一个简单的项目。<br>
运行它，会显示一个窗口。<br>
<br>
窗口上会显示当前电脑上所有的窗口信息。<br>
包括：窗口标题、窗口大小、窗口位置、hwnd、...<br>
<br>
然后用户可以优雅地根据自己的需求，调整窗口的大小和位置。<br>
非常适合和我一样的强迫症患者。<br>
<hr>

修改日志：<br>
第一版 v0.0.1 <br>
这段时间我特别沉迷在cmd终端进行操作，甚至一度想抛弃windows的图形化界面...<br>
我所采用的是将程序封装成一个py脚本，然后因为电脑有充足的Python环境。<br>
加到环境变量后，只需 <br>
1.激活Python环境 <br>
```cmd
conda activate base
```
2.运行脚本 <br>
```cmd
python "D:\_\_bat\python\lyzWindow.py"
```
或者更加简洁一些，再写一个bat脚本：lw.bat
```bat
@echo off
setlocal

:: 调用 Python 脚本并传递参数
D:\Anaconda3\envs\home\python.exe "D:\_\_bat\python\lyzWindow.py" %1

endlocal
```
如此直接调用bat脚本即可：
```cmd
lw
```
<hr>
第二版 v0.0.2 <br>
考虑到并不是所有电脑都有Python环境，也不是谁都喜欢在cmd进行操作。<br>
所以将程序打包成一个exe，脱离环境的控制。<br>
并且考虑到命令行方式并不是所有人都能接受，所以使用tk重写。<br>
最终以窗口程序的方式进行呈现。
<hr>
第三版 v0.0.3 <br> 
又经过一段时间的使用，在公司也换上了大的屏幕2576x1416.<BR>
对需求又有了一些新的感悟，所以继续调整。<br>
1.希望窗口可以等比例缩放，根据电脑的宽高尺寸；<br>
2.希望可以直接在窗口操作exclude.json文件(排除一些不想控制窗口)；<br>
3.希望可以添加一些快捷键，比如 全屏、最小化、退出、刷新、调整窗口大小、调整窗口位置……<br>
<br>
0.!!!使用R进行重写!!!<br>
0.学习了Rust的结果返回后，我超级喜欢对错误信息的手动传递。拒绝未知错误。<br>
<hr>

第六版 v0.0.6 <br> 
时隔许久，完全懒得折腾了。一个文件搞定，暂告一段落。<br>
lw.py<br>
...<br>
和 lw.bat <br>
```cmd
*/python.exe */lw.py
```
没有python环境的毁灭吧<br>
把python.exe的路径写好 然后把.bat脚本加到环境变量路径下 直接启动<br>
<br>
![Snipaste_2025-07-05_16-28-00.png](Snipaste_2025-07-05_16-28-00.png)
<hr>
不想折腾了<br>
<hr>



















