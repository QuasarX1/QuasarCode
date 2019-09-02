from QuasarCode.Tools.validators import isURI, isURL, isURIScheme, isURIAuthority, isURIPath, isURIQuery, isURIFragment

class URI(object):
    """
    A Universal Resourse Indicator

    For detailed infomation visit https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
    """

    class Scheme(object):
        def __init__(self, value):
            self.value = value

        def isValid(self):
            return isURIScheme(str(self))

        def isSecure(self):
            return self.value == "https:"
        
        def __str__(self):
            return self.value

    class Authority(object):
        def __init__(self, value):
            atSplit = value.split("@")
            self.userinfo = atSplit[0] if len(atSplit) > 1 else ""

            colonSplit = value.split(":")
            self.host = colonSplit[1 if len(atSplit) > 1 else 0]

            self.port = int(colonSplit[2 if len(atSplit) > 1 else 1]) if len(colonSplit) > 2 or (len(colonSplit) > 1 and len(atSplit) == 1) else None

        def isValid(self):
            return isURIAuthority(str(self))

        def __str__(self):
            return (self.userinfo + "@") if self.userinfo != "" else "" + self.host + (":" + str(self.port)) if self.port is not None else ""

    class Path(object):
        def __init__(self, value):
            self.value = value

        def isValid(self):
            return isURIPath(str(self))

        def __str__(self):
            return self.value

    class Query(object):
        def __init__(self, value):
            self.value = value

        def isValid(self):
            return isURIQuery(str(self))

        def __str__(self):
            return self.value

    class Fragment(object):
        def __init__(self, value):
            self.value = value

        def isValid(self):
            return isURIFragment(str(self))

        def __str__(self):
            return self.value

    def __init__(self, scheme, authority = URI.Authority(""), path = URI.Path("/"), query = URI.Query(""), fragment = URI.Fragment("")):
        self.scheme = scheme if isinstance(scheme, URI.Scheme) else URI.Scheme(scheme)
        self.authority = authority if isinstance(authority, URI.Authority) else URI.Authority(authority)
        self.path = path if isinstance(path, URI.Path) else URI.Path(path)
        self.query = query if isinstance(query, URI.Query) else URI.Query(query)
        self.fragment = fragment if isinstance(fragment, URI.Fragment) else URI.Fragment(fragment)

    def isValidURI(self):
        return isURI(str(self))

    def isValidURL(self):
        return isURL(str(self))

    def isValid(self):
        return self.isValidURI()

    def __str__(self):
        return str(self.scheme) + str(self.authority) + str(self.path) + str(self.query) + str(self.fragment)

    @staticmethod
    def fromString(string):
        pass

class URL(URI):
    def __init__(self, secure = True, authority = URI.Authority(""), path = URI.Path("/"), query = URI.Query(""), fragment = URI.Fragment("")):
        super().__init__("https:" if secure else "http:", authority, path, query, fragment)

    def isValid(self):
        return self.isValidURL()