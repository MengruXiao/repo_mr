import re
import sqlite3
import sys
from copy import deepcopy
from typing import Dict, List, Any, Union
from awsglue.utils import getResolvedOptions

_PAT = re.compile(r"{{[^{}]*}}")

_alias = {
    "CURRENT_TIME": "time('now')",  # 09:33:18
    "CURRENT_TIMESTAMP": "unixepoch('now')",  # 1675848798
    "CURRENT_DATE": "strftime('%Y%m%d', 'now')",  # 2023-02-08
    "CURRENT_DATETIME": "strftime('%Y%m%d%H%M%S', 'now')",  # 2023-02-08 09:33:18
}


def expression_parse(string) -> List[str]:
    exps = re.findall(_PAT, string)
    return exps


def run_query(query) -> Dict[str, Any]:
    with sqlite3.connect(":memory:") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            row = cursor.fetchone()
        except sqlite3.OperationalError as e:
            raise ValueError(f"Execute query failed: {query}, error: {e}")
        if row:
            return dict(row)
        return dict()


def expression_query(exp):
    function = exp.replace("{", "").replace("}", "").strip()
    function = _alias.get(function.upper(), function)
    try:
        query = f"SELECT {function} AS result"
        ret = run_query(query)
        if ret:
            return ret["result"]
        raise ValueError(f"Invalid expression: {exp}, result is None")
    except Exception:
        return exp


def render(string: str):
    """A string containing expressions can be dynamically rendered based on SQLite functions.
    To ensure proper evaluation, expressions must be encapsulated within double curly braces '{{}}'.

    # >>> render("s3://landing/appddm_{{date('now', 'localtime')}}/{{strftime('%Y%m%d','now', 'localtime')}}.xlsx")
    # 's3://landing/appddm_2023-02-08/20230208.xlsx'

    :param string:
    """
    exps = expression_parse(string)
    results = {exp: expression_query(exp) for exp in exps}
    for k, v in results.items():
        string = string.replace(k, str(v))
    return string


def render_args(kwargs: dict) -> dict:
    return dict([(k, render(v)) if type(v) == str else (k, v) for k, v in kwargs.items()])


def get_glue_args(
        positional: List[str], optional: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    This is a wrapper of the glue function getResolvedOptions to take care of the following case :
    * Handling optional arguments and/or mandatory arguments
    * Optional arguments with default value
    NOTE:
        * DO NOT USE '-' while defining args as the getResolvedOptions with replace them with '_'
        * All fields would be return as a string type with getResolvedOptions

    Arguments:
        positional {list} -- list of mandatory fields for the job
        optional {dict} -- dict for optional fields with their default value

    Returns:
        dict -- given args with default value of optional args not filled
    """
    # The glue args are available in sys.argv with an extra '--'
    optional_args = list(
        set([i[2:] for i in sys.argv]).intersection([i for i in optional])
    )

    args = getResolvedOptions(sys.argv, positional + optional_args)

    # Overwrite default value if optional args are provided
    optional_ = deepcopy(optional)
    optional_.update(args)
    return render_args(optional_)


args = get_glue_args(
    positional=[
        "query"
    ],
    optional={
        "ok": '2'
    }
)

res = args['query']
res2 = args['ok']

print(res)  # sd
print(res2) # 2





'''
    optional={
        "ok": '2'
    }
optional是字典类型，赋值时要注意"ok": '2'，而且optional是默认值，对ok参数赋予了默认值'2'，

在job details里

Job parameters 信息
Key
Custom parameter key
--query
Value - optional
Custom parameter value
sd

Custom parameter key
--ok
Custom parameter value # 这里对ok参数直接不填，他就会默认使用 "ok": '2',但是如果在这里填了东西，比如4，那么输出就会输出ok=4,以用户给的参数为主，不填参数值就按默认值来


'''








