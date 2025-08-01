from __future__ import annotations

import pytest

import narwhals as nw
from tests.utils import DASK_VERSION, Constructor, assert_equal_data


def test_expr_binary(constructor: Constructor) -> None:
    if "dask" in str(constructor) and DASK_VERSION < (2024, 10):
        pytest.skip()
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8.0, 9.0]}
    df_raw = constructor(data)
    result = nw.from_native(df_raw).with_columns(
        a=(1 + 3 * nw.col("a")) * (1 / nw.col("a")),
        b=nw.col("z") / (2 - nw.col("b")),
        c=nw.col("a") + nw.col("b") / 2,
        d=nw.col("a") - nw.col("b"),
        e=((nw.col("a") > nw.col("b")) & (nw.col("a") >= nw.col("z"))).cast(nw.Int64),
        f=(
            (nw.col("a") < nw.col("b"))
            | (nw.col("a") <= nw.col("z"))
            | (nw.col("a") == 1)
        ).cast(nw.Int64),
        g=nw.col("a") != 1,
        h=(False & (nw.col("a") != 1)),
        i=(False | (nw.col("a") != 1)),
        j=2 ** nw.col("a"),
        k=2 // nw.col("a"),
        l=nw.col("a") // 2,
        m=nw.col("a") ** 2,
    )
    expected = {
        "a": [4, 3.333333, 3.5],
        "b": [-3.5, -4.0, -2.25],
        "z": [7.0, 8.0, 9.0],
        "c": [3, 5, 5],
        "d": [-3, -1, -4],
        "e": [0, 0, 0],
        "f": [1, 1, 1],
        "g": [False, True, True],
        "h": [False, False, False],
        "i": [False, True, True],
        "j": [2, 8, 4],
        "k": [2, 0, 1],
        "l": [0, 1, 1],
        "m": [1, 9, 4],
    }
    assert_equal_data(result, expected)


def test_expr_binary_method(constructor: Constructor) -> None:
    if "dask" in str(constructor) and DASK_VERSION < (2024, 10):
        pytest.skip()
    data = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8.0, 9.0]}
    df_raw = constructor(data)
    result = nw.from_native(df_raw).with_columns(
        a=nw.lit(1).add(nw.lit(3).mul(nw.col("a"))).mul(nw.lit(1).truediv(nw.col("a"))),
        b=nw.col("z").truediv(nw.lit(2).sub(nw.col("b"))),
        c=nw.col("a").add(nw.col("b").truediv(2)),
        d=nw.col("a").sub(nw.col("b")),
        e=((nw.col("a").gt(nw.col("b"))).and_(nw.col("a").ge(nw.col("z")))).cast(
            nw.Int64
        ),
        f=(
            (nw.col("a").lt(nw.col("b")))
            .or_(nw.col("a").le(nw.col("z")))
            .or_(nw.col("a").eq(1))
        ).cast(nw.Int64),
        g=nw.col("a").ne(1),
        h=(nw.lit(value=False).and_(nw.col("a").ne(1))),
        i=(nw.lit(value=False).or_(nw.col("a").ne(1))),
        j=nw.lit(2).pow(nw.col("a")),
        k=nw.lit(2).floordiv(nw.col("a")),
        l=nw.col("a").floordiv(2),
        m=nw.col("a").pow(2),
    )
    expected = {
        "a": [4, 3.333333, 3.5],
        "b": [-3.5, -4.0, -2.25],
        "z": [7.0, 8.0, 9.0],
        "c": [3, 5, 5],
        "d": [-3, -1, -4],
        "e": [0, 0, 0],
        "f": [1, 1, 1],
        "g": [False, True, True],
        "h": [False, False, False],
        "i": [False, True, True],
        "j": [2, 8, 4],
        "k": [2, 0, 1],
        "l": [0, 1, 1],
        "m": [1, 9, 4],
    }
    assert_equal_data(result, expected)
