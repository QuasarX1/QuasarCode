from ..Tools._Struct import Struct
from ..Tools._autoproperty import NullableTypedAutoProperty
from ..Tools._typeshield import TypeShield, NestedTypeShield

from typing import Sequence

class PersonInfomation(Struct):
    given_name      = NullableTypedAutoProperty[str](TypeShield[str](str))
    family_name     = NullableTypedAutoProperty[str](TypeShield[str](str))
    email_addresses = NullableTypedAutoProperty[Sequence[str]](NestedTypeShield[Sequence[str]](str))
    website_url     = NullableTypedAutoProperty[str](TypeShield[str](str))
    #TODO: update the type checks for email addresses and URLs
