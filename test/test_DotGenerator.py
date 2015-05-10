from DotGenerator import *

import sys

dot = DotGenerator()
dot.setDrawInheritances(True)
dot.setDrawAssociations(True)
dot.setShowPrivMethods(True)
dot.setShowProtMethods(True)
dot.setShowPubMethods(True)

c1 = UmlClass()
c1.fqn = "NS1::AClass"
c1.addField("aa", "int", private)
c1.addField("bb", "void*", private)
c1.addField("cc", "NS1::BClass", private)
c1.addField("dd", "void", private)
c1.addField("publicField1", "CClass", public)
c1.addField("publicField2", "none", public)

c1.addMethod("void", "privateMethod1", "(asdds, dss*)", private)
c1.addMethod("BClass", "privateMethod2", "(asdf)", private)
c1.addMethod("void", "publicMethod1", "(asdds, dss*)", public)
c1.addMethod("BClass", "publicMethod2", "(asdf)", public)
dot.addClass(c1)

c2 = UmlClass()
c2.fqn = "NS1::BClass"
c2.parents.append(c1.fqn)
dot.addClass(c2)

c3 = UmlClass()
c3.fqn = "CClass"
dot.addClass(c3)

outputDotFile = ['uml2.dot', sys.argv[1]][len(sys.argv) == 2]

with open(outputDotFile, "w") as dotfile:
    dotfile.write(dot.generate())
