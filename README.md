# 原理
检测上钩水花音效的分贝峰值

# 使用指南

1. 进入游戏，找好钓点，把音效以外的声音关掉
2. 使用vs code打开这个文件所在文件夹，然后运行python脚本[1]
3. 根据自己的音量调整阈值[2]和钓鱼时间

# 注
[1] 运行程序时，会有几秒的等待期，供用户切换回魔兽窗口。之后魔兽窗口必须永远保持聚焦（Focused）。  
[2] 如果钓鱼时，水花音效响了，程序没有收钩，那就把阈值调低100；如果鱼没上勾就因为杂音收钩了，那就把阈值调高100。找到大概合适的阈值后再微调。
