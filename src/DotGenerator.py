import hashlib
import logging
import cgi

class UmlAccess:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


public = UmlAccess('public', '+')
protected = UmlAccess('protected', '#')
private = UmlAccess('private', '-')


class UmlField:
    def __init__(self, name, type, access):
        self.name = name
        self.type = type
        self.access = access

    def html(self):
        return cgi.escape(self.access.symbol + ' ' + self.name + ": " + self.type)


class UmlMethod:
    def __init__(self, returnType, name, argumentTypes, access):
        self.returnType = returnType
        self.name = name
        self.argumentTypes = argumentTypes
        self.access = access

    def html(self):
        return cgi.escape(self.access.symbol + ' ' + self.name + self.argumentTypes + " : " + self.returnType)


class UmlClass:
    def __init__(self):
        self.fqn = None
        self.parents = []

        self.fields = {}
        self.fields[public] = []
        self.fields[protected] = []
        self.fields[private] = []

        self.methods = {}
        self.methods[public] = []
        self.methods[protected] = []
        self.methods[private] = []

    def addField(self, name, type, access):
        self.fields[access].append(UmlField(name, type, access))

    def addMethod(self, returnType, name, argumentTypes, access):
        self.methods[access].append(UmlMethod(returnType, name, argumentTypes, access))

    def addParentByFQN(self, fullyQualifiedClassName):
        self.parents.append(fullyQualifiedClassName)

    def getId(self):
        return "id" + str(hashlib.md5(self.fqn).hexdigest())


class DotGenerator:
    _showPrivMembers = False
    _showProtMembers = False
    _showPubMembers = False
    _drawAssociations = False
    _drawInheritances = False

    def __init__(self):
        self.classes = {}

    def addClass(self, aClass):
        self.classes[aClass.fqn] = aClass

    def _genFields(self, fields):
        ret = "<BR/>\n\t\t\t\t\t".join([field.html() for field in fields])
        return ret

    def _genMethods(self, methods):
        ret = "<BR/>\n\t\t\t\t\t".join([method.html() for method in methods])
        return ret

    def _genClass(self, aClass, withPublicMembers=False, withProtectedMembers=False, withPrivateMembers=False):
        # Tabs are used because the space characters are preserved in the output and
        # this alignment is only to make the dot file itself readable.
        c = "\t" + (aClass.getId()+" [ \n" +
            "\t\tlabel = <\n" +
            "\t\t\t<TABLE BORDER=\"0\" CELLSPACING=\"0\" CELLBORDER=\"1\">\n" +
            "\t\t\t\t<TR><TD>" + cgi.escape(aClass.fqn) + "</TD></TR>\n")

        if withPublicMembers:
            pubFields = self._genFields(aClass.fields[public])
            pubMethods = self._genMethods(aClass.methods[public])
        else:
            pubFields = ''
            pubMethods = ''

        if withProtectedMembers:
            protFields = self._genFields(aClass.fields[protected])
            protMethods = self._genMethods(aClass.methods[protected])
        else:
            protFields = ''
            protMethods = ''

        if withPrivateMembers:
            privateFields = self._genFields(aClass.fields[private])
            privateMethods = self._genMethods(aClass.methods[private])
        else:
            privateFields = ''
            privateMethods = ''

        fields = "<BR/>".join([pubFields, protFields, privateFields])
        methods = "<BR/>".join([pubMethods, protMethods, privateMethods])

        c += "\t\t\t\t<TR><TD ALIGN=\"LEFT\" BALIGN=\"LEFT\">\n\t\t\t\t\t" + \
            fields + "\n\t\t\t\t</TD></TR>\n"
        c += "\t\t\t\t<TR><TD ALIGN=\"LEFT\" BALIGN=\"LEFT\">\n\t\t\t\t\t" + \
            methods + "\n\t\t\t\t</TD></TR>\n"
        c += "\t\t\t</TABLE>> ]\n"
        return c

    def _genAssociations(self, aClass):
        edges = set()
        for access, fields in aClass.fields.iteritems():
            for field in fields:
                if field.type in self.classes:
                    c = self.classes[field.type]
                    edges.add(aClass.getId() + "->" + c.getId())
        edgesJoined = "\n".join(edges)
        return edgesJoined+"\n" if edgesJoined != "" else ""

    def _genInheritances(self, aClass):
        edges = ""
        for parent in aClass.parents:
            if parent in self.classes:
                c = self.classes[parent]
                edges += (aClass.getId() + "->" + c.getId() + "\n")
        return edges

    def setDrawInheritances(self, enable):
        self._drawInheritances = enable

    def setDrawAssociations(self, enable):
        self._drawAssociations = enable

    def setShowPrivMethods(self, enable):
        self._showPrivMembers = enable

    def setShowProtMethods(self, enable):
        self._showProtMembers = enable

    def setShowPubMethods(self, enable):
        self._showPubMembers = enable

    def generate(self):
        dotContent = ("digraph dependencies {\n" +
                      "  fontname = \"Bitstream Vera Sans\"\n" +
                      "  fontsize = 8" +
                      "  node [" +
                      "    fontname = \"Bitstream Vera Sans\"\n" +
                      "    fontsize = 8\n" +
                      "    shape = \"none\"\n" +
                      "  ]\n" +
                      "  edge [\n" +
                      "    fontname = \"Bitstream Vera Sans\"\n" +
                      "    fontsize = 8\n" +
                      "  ]\n"
                      )

        for key, value in self.classes.iteritems():
            dotContent += self._genClass(value, self._showPubMembers, self._showProtMembers, self._showPrivMembers)

        # associations
        if self._drawAssociations:
            associations = ""
            for key, aClass in self.classes.iteritems():
                associations += self._genAssociations(aClass)

            if associations != "":
                dotContent += ("\nedge [arrowhead = open]\n")
                dotContent += associations

        # inheritances
        if self._drawInheritances:
            inheritances = ""
            for key, aClass in self.classes.iteritems():
                inheritances += self._genInheritances(aClass)

            if inheritances != "":
                dotContent += ("\nedge [arrowhead = empty]\n")
                dotContent += inheritances

        dotContent += "}\n"
        return dotContent
