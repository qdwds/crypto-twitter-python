# 新推文监控
当前项目功能是监控用户发送最新推文，有新推文之后推送消息到[钉钉](https://open.dingtalk.com/document/robots/custom-robot-access)上

## 添加新用户
添加新用户时候需要把`is_add_user`变量改为`True`,然后执行`python3 main.py`等待运行结束即可

## 开始监控
监控用户时候需要把`is_add_user`gaiwei`False`，然后后台运行任务