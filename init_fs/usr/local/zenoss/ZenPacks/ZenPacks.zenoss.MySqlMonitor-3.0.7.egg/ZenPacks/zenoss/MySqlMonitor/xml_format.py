import sys

import xml.dom.minidom as minidom


def patch_minidom():
    ''' Because default version outputs to much whitespace '''

    def writexml_text(self, writer, indent='', addindent='', newl=''):
        text = self.data.strip()
        if text:
            minidom._write_data(writer, "%s%s%s" % (indent, text, newl))

    minidom.Text.writexml = writexml_text


def format_xml(filename):
    patch_minidom()
    xml = minidom.parse(filename)
    with open(filename, "wb") as f:
        f.write(xml.toprettyxml(indent='  '))


def main(args):
    if len(args) < 2:
        print 'Pass file name'
        return
    format_xml(args[1])

if __name__ == '__main__':
    main(sys.argv)
