
from dataclasses import dataclass, field

import typing as t


@dataclass
class site_verify_query():
    secret: str
    response: str

# @dataclass
# class site_verify_response():
#     success: bool
#     challenge_ts: t.Optional[str]
#     hostname: t.Optional[str]
#     error_codes: t.Optional[str] = field(metadata=