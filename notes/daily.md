## python3标准输入中EOF的判断

```python
while True:
    try:
        a = input()
    except:
        break
```



## python随机数

python没有内置随机数生成函数，需要`import random`

```python
import random

random(self)
#Get the next random number in the range [0.0, 1.0).[0到1之间的浮点数]

randint(self, a, b)
#Return random integer in range [a, b], including both end points.【a到b之间的整数，包括a和b】

seed(self, a = None)
#Initialize internal state from hashable object.
#None or no argument seeds from current time or from an operating
#system specific randomness source if available.
#If a is not None or an int or long, hash(a) is used instead.
#If a is an int or long, a is used directly.  Distinct values between
#0 and 27814431486575L inclusive are guaranteed to yield distinct
#internal states (this guarantee is specific to the default
#Wichmann-Hill generator).【默认使用当前时间或者其他随机源做种子，也可以指定为特定的数】


```

