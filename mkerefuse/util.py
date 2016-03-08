from lxml import html


class XPathObject(object):
    input_properties = {}
    """Dict of keys (property names) and XPaths (to read vals from)"""

    @classmethod
    def FromHTML(cls, html_contents):
        inst = cls()
        print("Reading through {b} bytes for {c} properties...".format(
            b=len(html_contents),
            c=len(cls.input_properties)))

        tree = html.fromstring(html_contents)

        for attr_name, xpath in cls.input_properties.items():
            print("Searching for '{n}': {x}".format(
                n=attr_name,
                x=xpath))
            elements = tree.xpath(xpath)

            if not len(elements):
                print("Failed to find '{n}': {x}".format(
                    n=attr_name,
                    x=xpath))
                continue

            setattr(
                inst,
                attr_name,
                elements[0].text)

        return inst

    def __repr__(self):
        return json.dumps(
            self.__dict__,
            indent=4,
            separators=(',', ': '))
