import re


def check(_str, _pattern):
    # _matching the strings
    if re.search(_pattern, _str):
        print("Valid String")
    else:
        print("Invalid String")


pattern = re.compile('^[čćžšđČĆŽŠĐA-Za-z0-9.,\\s]+$')
check('ab23 Ć 2c      ', pattern)
check('349Č:', pattern)
