# https://github.com/amjith/fuzzyfinder

"""
Copyright (c) 2015, Amjith Ramanujam All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of fuzzyfinder nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import re


def fuzzyfinder(input, collection, accessor=lambda x: x):
    """
    Args:
        input (str): A partial string which is typically entered by a user.
        collection (iterable): A collection of strings which will be filtered
                               based on the `input`.
    Returns:
        suggestions (generator): A generator object that produces a list of
            suggestions narrowed down from `collection` using the `input`.
    """
    suggestions = []
    input = str(input) if not isinstance(input, str) else input
    pat = '.*?'.join(map(re.escape, input))
    regex = re.compile(pat)
    for item in collection:
        start = 0
        search_str = accessor(item)
        while True:
            r = regex.search(search_str)
            if r:
                suggestions.append((len(r.group()), start + r.start(), accessor(item), item))
                start = r.start() + 1
                search_str = search_str[start:]
            else:
                break

    # sorted_suggestions = sorted(suggestions)
    # for suggestion in sorted_suggestions:
    #     print suggestion[:-1]

    return (z[-1] for z in sorted(suggestions))
