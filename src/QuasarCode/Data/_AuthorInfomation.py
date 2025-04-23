from ..Tools._Struct import Struct
from ..Tools._autoproperty import NullableTypedAutoProperty
from ..Tools._typeshield import TypeShield
from ._PersonInfomation import PersonInfomation

class AuthorInfomation(Struct):
    given_name    = NullableTypedAutoProperty[str](TypeShield[str](str))
    family_name   = NullableTypedAutoProperty[str](TypeShield[str](str))
    email_address = NullableTypedAutoProperty[str](TypeShield[str](str))
    website_url   = NullableTypedAutoProperty[str](TypeShield[str](str))
    #TODO: update the type checks for email addresses and URLs

    @staticmethod
    def from_person(person: PersonInfomation):
        return AuthorInfomation(
            given_name = person.given_name,
            family_name = person.family_name,
            email_address = person.email_addresses[0],
            website_url = person.website_url
        )
