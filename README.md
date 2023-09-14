# DotDict
像JavaScript对象一样读写python字典数据

* 继承dict类，用于数据的获取和设置
* 使用.链式获取数据，简洁方便，容易理解

## 函数
* copy()

返回深度拷贝DotDict的副本

* json()

返回DotDict的json格式的字符串

* json(file)

将DotDict的json格式的字符串保存到文件file中，返回文件名
* yaml()

返回DotDict的yaml格式的字符串

* yaml(file)

将DotDict的yaml格式的字符串保存到文件file中，返回文件名

## 示例

```python
dd = util.DotDict()
dd.list = [111, 222]
dd.dict = {'a': 1, 'b': {'bb': 'bbb'}}
dd.string = '....'
dd.int = 2
print(dd.list[0])  # 111
print(dd.dict.a)  # 1
print(dd.dict.b.bb)  # bbb
print(dd.string)  # ....
print(dd.int)  # 2
print(dd.json())  # json格式的dd
print(dd.json('dd.json'))  # 将json格式的dd保存到文件dd.json
print(dd.yaml())  # yaml格式的dd
print(dd.yaml('dd.yml'))  # 将yaml格式的dd保存到文件dd.yml
```

* dd.json()

```json
{
    "list": [
        111,
        222
    ],
    "dict": {
        "a": 1,
        "b": {
            "bb": "bbb"
        }
    },
    "string": "....",
    "int": 2
}
```

* dd.yaml()

```yaml
dict:
    a: 1
    b:
        bb: bbb
int: 2
list:
- 111
- 222
string: '....'
```