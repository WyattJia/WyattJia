偶然间发现 Ruby 和 JavaScript 这两门语言都会为 object 提供自带提供一个 freeze 接口，调用之后可以将一个 mutable 的 object 变成 immutable 。 比如说 JavaScript 中的这段实现：

``` javascript
'use strict';

// 定义一个对象 object1
const object1 = {
    property1: 42
    };


// 根据 object1 ，调用 Object.freeze() 方法定义一个 object2
const object2 = Object.freeze(object1);


// 试着给 object2 的 property1 属性重新赋值
object2.property1 = 18;

// 会返回一个错误
object2.property1 = 18;
                  ^
TypeError: Cannot assign to read only property 'property1' of object '#<Object>'

// 提示 object2 已经变成只读的 immutable 对象了。

console.log(object2.property1);
// 打印出来 property1 的值依旧是 42 。
```

可以看到 JavaScript 中的 `Object.freeze()` 方法可以把一个对象冻结了。


曾经有一份 [PEP351](https://www.python.org/dev/peps/pep-0351/) 提案想要支持 Python Object 可以被手动冻结，但是因为价值观不符和的原因被 Guido Rejected 了。然而 Ruby 和 JavaScript 都有类似的 freeze object 的方法，我是否也能够在 Python 上自己实现一个类似的方法，将一个可变对象手动变成不可变对象呢。。

``` python
# 示例实现
a = [1, 2, 3]

freeze(a) # or a.__freeze__

a.append(4)
# FrozenError (can't modify frozen List)
```

---

``` Python
class ImmutablePoint(object):
    """An immutable class with 2 attributes 'x', 'y'."""

    __slots__ = ['x', 'y']

    def __setattr__(self, *args):
        raise TypeError("Can not modify immutable instance")

    __delattr__ = __setattr__

    def __init__(self, x, y):
        # We can no longer use self.value = value to store the instance data
        # so we must explicitly call the superclass
        super(ImmutablePoint, self).__setattr__('x', x)
        super(ImmutablePoint, self).__setattr__('y', y)
```
