# supervisor的作用
项目中有些脚本需要通过后台进程运行，保证不被异常中断，可以使用supervisor来实现。

supervisor是用Python开发的一套通用的进程管理工具，能把一个普通的命令行进程变成后台deamon，并监控进程状态，并在进程异常退出时重新启动。它是通过fork/exec的方式把这些被管理的进程当做supervisor的子进程来启动，这样只要在supervisor的配置文件中，把要管理的可执行文件的路径写进去即可。也实现当子进程挂掉的时候，父进程可以准确获取子进程挂掉的信息，可以选择是否自己启动和报警。supervisor还提供了一个功能，可以为supervisord或者每个子进程设置一个非root的user，这个user就可以管理它对应的进程。

# 安装supervisor
debian/ubuntu可以直接通过 sudo apt install supervisor 安装 (建议使用apt安装)

# 配置文件
supervisor安装成功后， 配置文件在 
/etc/supervisor/supervisord.conf 

supervisor的配置文件默认是不全的，不过在大部分默认的情况下，上面说的基本功能已经满足。而其管理的`子进程配置文件`在
/etc/supervisor/conf.d/*.conf

然后，给需要supervisor管理的脚本程序编写一个子进程配置文件，举个栗子：/etc/supervisor/conf.d/test.conf

```shell
#项目名
[program:game]
#脚本目录
directory=/opt/bin
#脚本执行命令
command=/usr/bin/python /opt/bin/test.py
#supervisor启动的时候是否随着同时启动，默认True
autostart=true
#当程序exit的时候，这个program不会自动重启,默认unexpected
#设置子进程挂掉后自动重启的情况，有三个选项，false,unexpected和true。如果为false的时候，无论什么情况下，都不会被重新启动，如果为unexpected，只有当进程的退出码不在下面的exitcodes里面定义的
autorestart=false
#这个选项是子进程启动多少秒之后，此时状态如果是running，则我们认为启动成功了。默认值为1
startsecs=1
#日志输出 
stderr_logfile=/tmp/game_stderr.log 
stdout_logfile=/tmp/game_stdout.log 
#脚本运行的用户身份 
user = test 
#把 stderr 重定向到 stdout，默认 false
redirect_stderr = true
#stdout 日志文件大小，默认 50MB
stdout_logfile_maxbytes = 20M
#stdout 日志文件备份数
stdout_logfile_backups = 20


[program:test] #说明同上
directory=/opt/bin 
command=/usr/bin/python /opt/bin/test.py 
autostart=true 
autorestart=false 
stderr_logfile=/tmp/test_stderr.log 
stdout_logfile=/tmp/test_stdout.log 
```

配置文件详解

```shell
;[program:theprogramname]      ;这个就是咱们要管理的子进程了，":"后面的是名字，最好别乱写和实际进程
                                有点关联最好。这样的program我们可以设置一个或多个，一个program就是
                                要被管理的一个进程
;command=/bin/cat              ; 这个就是我们的要启动进程的命令路径了，可以带参数
                                例子：/home/test.py -a 'hehe'
                                有一点需要注意的是，我们的command只能是那种在终端运行的进程，不能是
                                守护进程。这个想想也知道了，比如说command=service httpd start。
                                httpd这个进程被linux的service管理了，我们的supervisor再去启动这个命令
                                这已经不是严格意义的子进程了。
                                这个是个必须设置的项
;process_name=%(program_name)s ; 这个是进程名，如果我们下面的numprocs参数为1的话，就不用管这个参数
                                 了，它默认值%(program_name)s也就是上面的那个program冒号后面的名字，
                                 但是如果numprocs为多个的话，那就不能这么干了。想想也知道，不可能每个
                                 进程都用同一个进程名吧。

                                
;numprocs=1                    ; 启动进程的数目。当不为1时，就是进程池的概念，注意process_name的设置
                                 默认为1    。。非必须设置
;directory=/tmp                ; 进程运行前，会前切换到这个目录
                                 默认不设置。。。非必须设置
;umask=022                     ; 进程掩码，默认none，非必须
;priority=999                  ; 子进程启动关闭优先级，优先级低的，最先启动，关闭的时候最后关闭
                                 默认值为999 。。非必须设置
;autostart=true                ; 如果是true的话，子进程将在supervisord启动后被自动启动
                                 默认就是true   。。非必须设置
;autorestart=unexpected        ; 这个是设置子进程挂掉后自动重启的情况，有三个选项，false,unexpected
                                 和true。如果为false的时候，无论什么情况下，都不会被重新启动，
                                 如果为unexpected，只有当进程的退出码不在下面的exitcodes里面定义的退 
                                 出码的时候，才会被自动重启。当为true的时候，只要子进程挂掉，将会被无
                                 条件的重启
;startsecs=1                   ; 这个选项是子进程启动多少秒之后，此时状态如果是running，则我们认为启
                                 动成功了
                                 默认值为1 。。非必须设置
;startretries=3                ; 当进程启动失败后，最大尝试启动的次数。。当超过3次后，supervisor将把
                                 此进程的状态置为FAIL
                                 默认值为3 。。非必须设置
;exitcodes=0,2                 ; 注意和上面的的autorestart=unexpected对应。。exitcodes里面的定义的
                                 退出码是expected的。
;stopsignal=QUIT               ; 进程停止信号，可以为TERM, HUP, INT, QUIT, KILL, USR1, or USR2等信号
                                  默认为TERM 。。当用设定的信号去干掉进程，退出码会被认为是expected
                                  非必须设置
;stopwaitsecs=10               ; 这个是当我们向子进程发送stopsignal信号后，到系统返回信息
                                 给supervisord，所等待的最大时间。 超过这个时间，supervisord会向该
                                 子进程发送一个强制kill的信号。
                                 默认为10秒。。非必须设置
;stopasgroup=false             ; 这个东西主要用于，supervisord管理的子进程，这个子进程本身还有
                                 子进程。那么我们如果仅仅干掉supervisord的子进程的话，子进程的子进程
                                 有可能会变成孤儿进程。所以咱们可以设置可个选项，把整个该子进程的
                                 整个进程组都干掉。 设置为true的话，一般killasgroup也会被设置为true。
                                 需要注意的是，该选项发送的是stop信号
                                 默认为false。。非必须设置。。
;killasgroup=false             ; 这个和上面的stopasgroup类似，不过发送的是kill信号
;user=chrism                   ; 如果supervisord是root启动，我们在这里设置这个非root用户，可以用来
                                 管理该program
                                 默认不设置。。。非必须设置项
;redirect_stderr=true          ; 如果为true，则stderr的日志会被写入stdout日志文件中
                                 默认为false，非必须设置
;stdout_logfile=/a/path        ; 子进程的stdout的日志路径，可以指定路径，AUTO，none等三个选项。
                                 设置为none的话，将没有日志产生。设置为AUTO的话，将随机找一个地方
                                 生成日志文件，而且当supervisord重新启动的时候，以前的日志文件会被
                                 清空。当 redirect_stderr=true的时候，sterr也会写进这个日志文件
;stdout_logfile_maxbytes=1MB   ; 日志文件最大大小，和[supervisord]中定义的一样。默认为50
;stdout_logfile_backups=10     ; 和[supervisord]定义的一样。默认10
;stdout_capture_maxbytes=1MB   ; 这个东西是设定capture管道的大小，当值不为0的时候，子进程可以从stdout
                                 发送信息，而supervisor可以根据信息，发送相应的event。
                                 默认为0，为0的时候表达关闭管道。。。非必须项
;stdout_events_enabled=false   ; 当设置为ture的时候，当子进程由stdout向文件描述符中写日志的时候，将
                                 触发supervisord发送PROCESS_LOG_STDOUT类型的event
                                 默认为false。。。非必须设置
;stderr_logfile=/a/path        ; 这个东西是设置stderr写的日志路径，当redirect_stderr=true。这个就不用
                                 设置了，设置了也是白搭。因为它会被写入stdout_logfile的同一个文件中
                                 默认为AUTO，也就是随便找个地存，supervisord重启被清空。。非必须设置
;stderr_logfile_maxbytes=1MB   ; 这个出现好几次了，就不重复了
;stderr_logfile_backups=10     ; 这个也是
;stderr_capture_maxbytes=1MB   ; 这个一样，和stdout_capture一样。 默认为0，关闭状态
;stderr_events_enabled=false   ; 这个也是一样，默认为false
;environment=A="1",B="2"       ; 这个是该子进程的环境变量，和别的子进程是不共享的
;serverurl=AUTO                ;
```

# 运行
apt安装的通过 /etc/init.d/supervisor start 运行

# 子进程管理

1.查看所有子进程的状态
```
# supervisorctl status
```

2.关闭、开启指定的子进程
```
# supervisorctl stop test
# supervisorctl start test
```
3.关闭、开启所有子进程
```
# supervisor stop all
# supervisor start all
```