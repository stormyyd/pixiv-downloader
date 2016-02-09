## 介绍

一个P站图片的下载器。准确地说应该是图片地址的获取器。

## 依赖

### Python3

脚本采用 Python3 编写。

### pixivpy

GitHub：[https://github.com/upbit/pixivpy](https://github.com/upbit/pixivpy)

安装：

    pip3 install pixivpy

如果遇到权限不够的问题，请加上 sudo：

    sudo pip3 install pixivpy

### aria2

官网：[https://aria2.github.io](https://aria2.github.io)

安装：Linux、OS X 用户自行使用对应的包管理工具安装，Windows 用户请到官网自行查找下载地址。

## 使用

```
用法: url.py [-h] (-w | -u) id [id ...]

必选参数:
  id          画师或作品ID。

可选参数:
  -h, --help  显示帮助信息然后退出。
  -w, --work  如果要下载作品，请带上这个选项。
  -u, --user  如果要下载画师的作品，请带上这个选项。
```

执行完成后会在当前目录生成形如 user_id.aria2（选择下载画师的作品） 或 work_id.aria2（选择下载作品） 的文件。

接下来调用 aria2 进行下载：

    aria2c -i user_id.aria2

或

    aria2c -i work_id.aria2

下载完成的图片会放在以作品名为文件名的文件夹中。

注意：第一次使用本脚本会要求输入一个P站帐号用于登录P站，帐号和密码会以 json 的形式保存在 config.json 文件中。如果输错了的话删除掉 config.json 重新运行即可。

## License

本程序在 [Do What The Fuck You Want To Public License](https://github.com/stormyyd/pixiv-downloader/blob/master/LICENSE) 授权下发布。
