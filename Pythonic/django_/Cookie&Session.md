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

