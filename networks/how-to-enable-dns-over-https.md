## Foreword

DNS-over-HTTPS 协议现在逐渐被放到台面上讨论，目前 FireFox 是唯一支持该协议的浏览器。然而这个协议在 Firefox  中也不是默认就被开启的，启用 DoH 之前需要执行一系列的操作和修改，才能保证协议的运行。
在写手把手开启 DoH 协议的教程之前，我们先描述一下它的工作原理和过程。


## How DNS-over-HTTPS works

DNS-over-HTTPS 协议的工作原理是获取用户在浏览器地址栏输入的域名，并向 DNS 服务器发送查询，从而获取到该站点服务器的 IP 地址。
这也是常规 DNS 协议的工作原理。然而 DoH 在这个过程中会将 DNS 查询发送到 DoH 功能完备的 DNS 服务器中，并且会通过 443 HTTPS 加密端口来发送请求，而非传统的 53 纯文本端口。
查询过程当中， DoH 将 DNS 请求隐藏到了一个常规的 HTTPS 请求当中，所以第三方将无法嗅探到用户将要进行的 DNS 查询，并推断出用户将要访问的网站。
除此之外，DoH 还有第二个特性就是它能够在应用层面工作。应用程序可以在内部硬编码 DoH 兼容的解析器，并且在应用内部发送 DoH 查询。这种操作模式绕过了操作系统本身的 DNS 配置，默认情况下，操作系统的 DNS 配置是由本地的网络服务商提供的。这也意味着，支持 DoH 的应用程序能够有效的绕过 ISP 流量监管，访问那些不存在的网站，这也是 DoH 目前被夸赞的原因之一。

## How to enable?

### 方法一：从 firefox 设置项开启
* 点击 firefox 菜单，进入 `preferences` 页面。
* 进入 `General` 选项，下拉至 `Network Settings` 栏目，点击 `Settings` 按钮
    如图：
    [!img](/)
* 弹出框中选择 `Enable DNS over HTTPS` 选项，然后配置 DNS 解析服务，默认是 Cloudflare dns 服务.

### 方法二：从 `about:config` 页面配置

* 从 firefox 进入 `about:config` 页面 
* 首先配置 `network.trr.mode` 选项，这个配置可以开启 DoH 服务，提供了四个参数作为选项
  * 0  代表 firefox 默认安装时的参数(目前默认都是关闭，即默认值是 5)
  * 1 DoH 已经开启，Firefox 会从 DoH 和常规 DNS 中自动选择一个更加快速的方法使用
  * 2 DoH 已经开启，常规 DNS 作为备用选项
  * 3 DoH 已经开启，常规 DNS 已经关闭
  * 5 关闭 DoH
  *通常来说选项2比较适用*
* 下一步需要修改 `network.trr.uri` 选项，这个配置决定了使用哪家 DNS 查找服务商。有许多可以使用的服务点击[!这里](https://github.com/curl/curl/wiki/DNS-over-HTTPS#publicly-available-servers)获取，默认还是推荐 Cloudflare ：`https://mozilla.cloudflare-dns.com/dns-query`。
  [!img]




