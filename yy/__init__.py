# -*- coding: utf-8 -*-
import orjson
import json
import yaml
import copy as deepcopy
from collections.abc import Iterable
from datetime import datetime

__title__ = 'DotDict'
__version__ = '1.0'
__author__ = 'viewercq'
__license__ = 'MIT'
__all__ = ['DotDict']


def to_json(dt, filename=None, hide_keys=[], pretty=False):
    try:
        if len(hide_keys):
            dt = dt.deepcopy()
            for k in hide_keys:
                dt.pop(k, None)
        if isinstance(dt, dict) or isinstance(dt, list):
            try:
                ret = decode_bytes(orjson.dumps(dt, option=orjson.OPT_INDENT_2)) if pretty else decode_bytes(orjson.dumps(dt))
            except Exception as e:
                ret = json.dumps(dt, indent=4, sort_keys=False, ensure_ascii=False, default=to_str) if pretty else json.dumps(dt, sort_keys=False, ensure_ascii=False, default=to_str)
        if filename:
            with open(filename, 'w+', encoding='utf-8') as f:
                for l in ret.splitlines():
                    f.writelines(l + '\n')
            return filename
        else:
            return ret
    except Exception as e:
        print('[ERROR]to_json(%s) failed because of exception\n%s' % (dt, e))
        return None


def to_pretty_json(dt, filename=None, hide_keys=[]):
    return to_json(dt, filename=filename, hide_keys=hide_keys, pretty=True)


def to_str(obj):
    t = type(obj)
    if t in [set]:
        obj = list(obj)
    if t in [dict, list, tuple]:
        try:
            return decode_bytes(orjson.dumps(obj))
        except:
            return str(obj)
    elif t in [int, float, str]:
        return obj
    elif t in [datetime]:
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return str(obj)


def decode_bytes(bs, encodings=['utf8', 'gbk']):
    if bs is None:
        return ''
    if isinstance(bs, str):
        return bs
    for encoding in encodings:
        try:
            if encoding == 'bytes':
                return bs
            elif encoding == 'base64':
                return base64.b64encode(bs).decode('utf-8')
            else:
                return bs.decode(encoding)
        except Exception as e:
            err = u'decode bytes[%s] by %s failed because %s %s' % (bs, encoding, type(e), e)
            log_error(err)
    return bs.decode('utf8', 'ignore')


def to_yaml(dt, filename=None):
    try:
        if isinstance(dt, dict):
            dt = dict(dt)
        if filename:
            with open(filename, 'w+', encoding='utf-8') as f:
                f.write(u'---\n')
                yaml.safe_dump(dt, f, indent=2, encoding='utf-8', allow_unicode=True, default_flow_style=False)
            return filename
        else:
            return u'---\n%s' % yaml.safe_dump(dt, indent=2, allow_unicode=True, default_flow_style=False)
    except Exception as e:
        print('[ERROR]util.to_yaml(%s) failed because of exception\n%s' % (dt, e))
        return ''


def merge_lists(*lists, replace=True, unique=False):
    if replace is False:
        return lists[0]
    result = None
    for l in lists:
        if isinstance(l, Iterable):
            if result is None:
                result = l if isinstance(l, list) else list(l)
            else:
                for v in l:
                    if v not in result:
                        result.append(v)
        elif l and l not in result:
            result.append(l)
    if unique:
        return unique_list(result)
    return result if result else []


def unique_list(l):
    return list(set(l)) if l else []


def iterable(o):
    if isinstance(o, str) or isinstance(o, bytes):
        return False
    return isinstance(o, Iterable)


def merge_dicts(*dicts, replace=True):
    result = None
    if isinstance(dicts[0], list):
        dicts = dicts[0]
    for d in dicts:
        if isinstance(d, dict):
            if result is not None:
                for k, v in d.items():
                    if k in result:
                        v0 = result[k]
                        if isinstance(v, list) and isinstance(v0, list):
                            merge_lists(v0, v, replace=replace)
                        elif isinstance(v, dict) and isinstance(v0, dict):
                            merge_dicts(v0, v, replace=replace)
                        elif replace is True:
                            if v:
                                result[k] = DotDict(v) if type(v) == dict else v
                            else:
                                pass
                        elif replace == 'sum':
                            result[k] = v0 + v
                    else:
                        result[k] = DotDict(v) if type(v) == dict else v
            else:
                result = d
    return DotDict(result) if isinstance(result, dict) else result


class DotDict(dict):
    support_chain_set = None

    def __getattr__(self, key):
        val = self.get(key)
        if self.support_chain_set is True and val is None:
            return self.__update__(key, self.get_chain_set_instance())
        t = type(val)
        if t not in [dict, list] and not key.startswith('__'):
            return val
        if key.startswith('__'):
            return dict.__getattr__(self, key)
        if t is dict:
            return self.__update__(key, DotDict(val))
        elif t is list:
            return self.__update__(key, list(map(lambda x: DotDict(x) if type(x) is dict else x, val)))
        else:
            return val

    def __setattr__(self, *args):
        if args[0] in ['support_chain_set']:
            dict.__setattr__(self, *args)
            return
        dict.__setitem__(self, *args)

    def __update__(self, key, value):
        self[key] = value
        return self[key]

    def deepcopy(self):
        return DotDict(deepcopy.deepcopy(self.back2dict()))

    def json(self, file=None):
        return to_pretty_json(self, file)

    def yaml(self, file=None):
        return to_yaml(self.back2dict(), file)

    def back2dict(self):
        d = dict(self)
        for k, v in self.items():
            t = type(v)
            if t is DotDict:
                d[k] = v.back2dict()
            elif t is list:
                d[k] = [x.back2dict() if type(x) is DotDict else x for x in v]
        return d

    def merge(self, *args, replace=False):
        if isinstance(args[0], list):
            return merge_dicts(merge_lists([self], args[0]), replace=replace)
        return merge_dicts(self, *args, replace=replace)

    @staticmethod
    def get_chain_set_instance():
        val = DotDict()
        val.support_chain_set = True
        return val

    __delattr__ = dict.__delitem__
