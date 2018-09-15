from sqlalchemy import inspect

def get_dict(obj):
    return { c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs }

def get_dict_array(obj):
    res = []
    for o in obj:
        res.append(get_dict(o))
    return res