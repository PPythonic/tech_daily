# 1.http协议无状态问题
`http`协议没有多次请求之间的关联功能, 协议的本意也没有考虑到多次请求之间的状态维持, 每一次请求都被协议认为是一次性的. 但在某些场景下如一次请求多次访问,我们希望可以保存登录状态, 协议并没有直接提供会话跟踪的支持, 需要靠其他手段来实现目标.


# 二、会话追踪技术 -- cookie
## 1、对cookie的理解
* **cookie是一个`k-v`的数据结构，用于保存需要维护状态的数据，`cookie`与`session`最大的区别在于 -- `cookie`把数据保存在客户端，`session`把数据保存在服务端。

* cookie一般由服务器设置，并可以保存在`http`的请求头和响应头中。

* `cookie`由浏览器保存，浏览器实现了`cookie`的保存和发送，而服务器对`cookie`的设置和接收则需要我们配置。

* 通过`cookie`可以在多个会话之间共享一些必要的信息如登录状态数据，历史访问记录，个性化定制设置等，以实现会话跟踪，**让用户感觉到网站可以`记录`自己的偏好，减少不必要的重复输入，从而提升用户体验。**

## 2、cookie的使用接口
`django`的服务端发送响应有三种方式：

```
return HttpResponse()
return render()
return redirect()
```

这三种方法实例化的结果都是`HttpResponse`类的实例，可以直接用于设置`cookie`。

在`response`对象上执行`set_cookie(key, value,..)`即可设置`cookie`，其中特别注意`cookie`属性的设置。

**cookie的设置**
服务器在响应对象上进行`set_cookie`操作，一旦设置完成，客户端后续的请求就可以根据`cookie`的属性规则携带`cookie`数据。

```
def set_cookie(key, value='', max_age=None, expires=None, path='/', domain=None, secure=False, httponly=False, samesite=None)
```

**`cookie`的获取**
服务器在请求对象上通过`request.COOKIES`得到`cookie`字典数据，注意此处拿到的`cookie`数据从安全性来说是未被验证正确性的。
```
@cached_property
def COOKIES(self):
    raw_cookie = get_str_from_wsgi(self.environ, 'HTTP_COOKIE', '')
    return parse_cookie(raw_cookie)
```

*注意1：cookie在set的时候可以设置他被发送的范围，每个`cookie`都有对应的`domain+path`属性，这约束了cookie发送范围，只有当http的请求落在此范围中的url，才会携带此cookie。*

*注意2：一个cookie就是一个key-value项，不过他还携带有属性，一个cookies是一个字典，保存了很多cookie项，注意单个cookie项和整个cookies字典的关系。*

## 3、cookie的属性

```
max_age:
失效延迟时间，单位是秒，设置成60秒就代表在设置玩之后的60秒内，此cookie有效，超时之后cookie失效，浏览器会删除失效的cookie。此参数默认是None，意味着直到浏览器关闭，即默认是会话cookie。
注意：如果max_age是0，意味着让浏览器立即删除此cookie，即此cookie即刻失效。

expires:
指定失效时间，同样用于设置使cookie失效，只不过是另一种时间指定方式。

domain:
此cookie可以被使用的域名范围。

path：
与domain配合着使用，默认是跟路径'/'，意味着在当前domain范围下的任何url都会携带此cookie。可以主动设置其他路径以缩小发送的范围，从而约束某一cookie只应用于某些url。

secure：
默认是False，一般配合https协议使用，在https协议下，只有secure属性是True的cookie才允许被发送。

httponly：
默认是False，这意味着js也可以通过document.cookie来访问和设置此cookie，而如果设置成True，则意味着只允许服务端来访问和设置此cookie。
```

## 4、使用cookie的问题
**cookie的安全性问题**
服务器是根据客户端发送过来的`cookie`进行状态判断，这种保存在客户端的cookie数据非常容易修改和伪装，服务器基本无法知晓cookie的正确性，也就不能完全相信cookie的数据。

此外，cookie很容易被盗取，如果客户端cookie里面包含私密数据的话，就更不安全了。

**cookie的覆盖问题**
在服务端上设置新的cookie会让客户端更新本地cookie。

**cookie的合理性问题**
什么样的数据适合放到`cookie`中？
`cookie`的数据是每次交互都要被传输的，所以：
* 应该是常用的数据，如果不常用只会浪费带宽减小效率，最好是多次交互中都要使用或者修改。
* 应该是小数据量
* 不应该是非常私密的数据

*所以cookie特别适合发送sessionid，他能满足上述所有条件*

**cookie的存储问题**
`cookie`是客户端临时存储，按规定单个`cookie`文件存储量最大是`4kb`，每个域名下的`cookie`文件不能超过20个，不应该将`cookie`用于存储滥用，要使用客户端的存储功能应该启用`localstorage`。

**cookie的访问限制问题**
`js`的`document.cookie`可以获取`cookie`的数据，将会在控制台输出一个字符串格式的`key-value`数据，如果此cookie的属性`htttponly=true`就不能通过此cookie获取。

# 3、会话跟踪技术 -- session
## 1、对session的理解
`session`把数据存放在服务器上，并使用一个标签`session-key`唯一标记此数据。`session-key`作为`cookie`发送给客户端，即客户端只保存`session-key`，然后通过`cookie`发送给服务端，以表明身份，所以`session`比`cookie`更安全。

每一次请求到达服务器的时候，服务器获取`cookie`中保存的`session-key`，然后在数据库`django-session`表中寻找对应的`session-data`，进一步处理业务逻辑。

`session`的使用有如下优点：
* 数据保存在服务端，客户端仅保存一个`sessionid`
* `sessionid`数据量很小，适合每次发送
* 安全性，`sessionid`是一个随机字符串，不携带任何私密数据

## 2、session的使用接口

`django`实现了`session`，帮我们完成了许多操作，且提供使用的接口非常简单：
```
request.session['nama'] = 'xxx'
```

设置`session`的时候会执行如下三个操作:
```
1、创建一个随机字符串sessionid
2、把sessionid作为session-key，以及一个session_data字典加入到django-session表中
3、set-cookie，把sessionid发送给客户端
```

*注意1：session_data是一个字典，然后通过orm存到django_session表中（应该有字典到字符串的序列化和加密操作）*

*注意2：如果发现客户端的cookie中含有sessionid说明这不是第一次登录，将会使用sessionid更新此sessionid对应的session_data数据。*

*注意3：如果有两个用户在同一台电脑的同一个浏览器上访问同一个url，因为sessionid是作为cookie存在，所以两个人会使用同一个sessionid。*

*而对于服务器而言，只认session不认人，使用同一个sessionid的操作会覆盖之前的数据以导致在服务器上的session_data数据会相互覆盖，这样的结果是数据紊乱*

**session的读取**

读取`session`的接口同样很简单：
```
name = request.session['name']
```

读取的时候会执行如下三个操作：
```
1、获取request.COOKIE中的sessionid
2、拿着sessionid作为session-key到数据库的django-session表中查找对应的session-data，底层就是执行orm的objects.filter(session_key=sessionid)
3、获取session-data数据作进一步处理
```

**session的删除**

```
1、del request.session['xxx'] # 删除一个会话对象属性
2、request.session.flush()   # 删除所有会话数据
```

清空会话信息时会执行以下操作：
```
1、删除django-session表中的session-key=sessionid的记录，底层操作就是执行orm的objects.filter(session_key=sessionid).delete()。
2、删除response中的cookie里的sessionid记录
```

*注意1：服务器把sessionid作为cookie的数据发送给客户端保存，一般是会话cookie即不关闭浏览器就可以一直保存会话跟踪。但一旦关闭了浏览器，则此sessionid便不再有效。但django颁发的cookie默认有效时间是2周，所以cookie会被保存到客户端硬盘上，即使关闭了浏览器也继续保存。*

*注意2：因为服务器无法获知客户端浏览器将会在什么时候关闭，更无法获知浏览器什么时候会执行清空cookie的操作。客户端一般只有在logout的时候才会主动告知删除session，其他情况下浏览器不会主动告知，所以服务器的session不能无限保存，被迫要设置失效时间（不然存储空间浪费），在一定时间内如果还没有用户重新访问此session，便被服务端认为此用户已失效，进而可以删除session数据。*

## 3、session的属性
settings中还可以配置全局的session属性：

```
# settings.py文件

    SESSION_ENGINE = 'django.contrib.sessions.backends.db'   # 引擎（默认）
    SESSION_COOKIE_NAME ＝ "sessionid"                       # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
    SESSION_COOKIE_PATH ＝ "/"                               # Session的cookie保存的路径（默认）
    SESSION_COOKIE_DOMAIN = None                             # Session的cookie保存的域名（默认）
    SESSION_COOKIE_SECURE = False                            # 是否Https传输cookie（默认）
    SESSION_COOKIE_HTTPONLY = True                           # 是否Session的cookie只支持http传输（默认）
    SESSION_COOKIE_AGE = 1209600                             # Session的cookie失效日期（2周）（默认）
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False                  # 是否关闭浏览器使得Session过期（默认）
    SESSION_SAVE_EVERY_REQUEST = False                       # 是否每次请求都保存Session，默认修改之后才保存（默认）
```

## 4、使用session的问题
1、session的正常工作依赖于cookie的启用，如果客户端禁用cookie功能，该如何保证session正常工作？---重写url

2、同一台电脑同一个浏览器，访问同一个`url`，保存着同一个`sessionid`，如何处理多用户使用同一`sessionid`登录而导致的数据紊乱问题？---使用用户认证组件，使用账户密码来区别用户

# 四、总结

1、cookie和session都是为了解决http协议自身并不支持状态维持的缺点

2、会话跟踪的目的是为了让多次请求之间可以共享数据，以提供更好的用户体验

3、cookie和session都需要保存状态维持数据，只不过cookie是保存在客户端，session保存在服务端。