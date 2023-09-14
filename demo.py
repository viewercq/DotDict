# -*- coding: utf-8 -*-
from yy import DotDict

dd = DotDict({'init': 0})
print('1 dd.init:', dd.init)
dd.list = [111, 222]
dd.dict = {'a': 1, 'b': {'bb': 'bbb'}}
dd.string = '....'
dd.int = 2
print('2 dd.list[0]:', dd.list[0])  # 111
print('3 iter list:')
for v in dd.list:  #
    print('\t', v)
print('4 dd.dict.a:', dd.dict.a)  # 1
print('5 dd.dict.b.bb:', dd.dict.b.bb)  # bbb
dd.dict.b.bb = b'new'
print('6 dd.dict.b.bb:', dd.dict.b.bb)  # b'new'
print('7 iter dict:', )
for k, v in dd.dict.items():
    print('\t', k, v)
print('8 dd.string:', dd.string)  # ....
print('9 dd.int:', dd.int)  # 2
dd.int += 2
print('10 dd.int:', dd.int)  # 4

print('11 序列化json字符串:', dd.json())  # json格式的dd
print('12 序列化json文件: ', dd.json('dd.json'))  # dd.json, 将json格式的dd保存到文件dd.json

print('13 序列化yml字符串:', dd.yaml())  # yaml格式的dd
print('14 序列化yml文件', dd.yaml('dd.yml'))  # dd.yml, 将yaml格式的dd保存到文件dd.yml

try:
    dd.a.b = 3  # 'NoneType' object has no attribute 'b'
    print('15 因为上一行异常不会打印', dd.a.b)  # 异常
except Exception as e:
    print('%s when support_chain_set is False' % e)

dd.support_chain_set = True  # 支持任意长的链式赋值
dd.a.b.c.d.e.f = 3
print('16 dd.a.b.c.d.e.f:', dd.a.b.c.d.e.f)  # 3
print('17 dd.a.b.c.d.e:', dd.a.b.c.d.e)  # {'f': 3}
print('18 dd.deepcopy().json():', dd.deepcopy().json())

d1 = DotDict({
    'name': 'd1',
    'count': 1,
})
dicts = [{
    'name': 'd2',
    'count': 2,
}, {
    'name': 'd3',
    'count': 3,
}, {
    'name': 'd4',
    'count': 4,
}]
d1.merge(dicts, replace='sum')  # d1通过sum的方式合并dicts
print('19 d1.count:', d1.count)  # 10
