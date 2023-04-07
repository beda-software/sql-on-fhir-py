import pytest

from macro import convert


@pytest.mark.parametrize(
    "sql,dialect,expected",
    [
        (
            """
select
({$ .name[0].family }) as family,
({age .birthDate}) as age,
({$ .gender}) as gender
from patient
limit 10
""",
            "postgres",
            """
select
resource#>>'{name,0,family}' as family,
date_part('year', age(current_timestamp,(resource#>>'{birthDate}')::timestamp)) as age,
resource#>>'{gender}' as gender
from patient
limit 10
""",
        ),
        (
            """
select
({$ .name[0].family }) as family,
({age .birthDate}) as age,
({$ .gender}) as gender
from patient
limit 10
""",
            "duckdb",
            """
select
name[1].family as family,
datediff('year', birthDate::date, current_date ) as age,
gender as gender
from patient
limit 10
""",
        ),
    ],
)
def test_convertor(sql, dialect, expected):
    assert convert(sql, dialect) == expected
