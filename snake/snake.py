#!/usr/local/bin/python
# -*- coding: utf-8 -*-

###################################################################################
#
#                               Reptile Demonstration
#
###################################################################################                               


from class_snake import *

boa = Snake("Bubbles")
boa.set_oviparous(False)
boa.set_constriction(True)
boa.set_venom(False)
#boa.color = "yellow"
boa.color = "pink"
# This code demonstrates that you can pretty much assign any property you want to a class arbitrarly
# and then recall it. When you do it you are putting the value in the class instances __dict__ 
# Here, I also test for the foo atribute in the Snake class and print something if it is.
# If its not defined, I just ignore it; but I have to put it in a Try: Except: block to avoid it
# erroring out because I don't define it everywhere. If I did go to the trouble of giving every 
# snake a foo I wouldn't need the test. Is sort of lazy programming; but it demonstrates how
# to handle it. It might also be relevant based on null user input etc.
#
# This is all just to demonstrate the classic assignment of properities without a getter setter
# to see a real getter setter look at color

boa.foo = "bar"
boa.set_size(1.5)
boa.set_location("Equador")
print boa       # demonstrates the __repr__ method
print "Here we test the __str__ method which is the same as print: "
print str(boa)  # demonstrates the str method
print "Finally we test the arbitrarly property foo:"
print "Boa's foo is %s"%boa.foo
print

python = Snake("Poly")
python.set_oviparous(True)
python.set_constriction(True)
python.set_venom(False)
python.color = 'green'
python.set_size(1.8)
python.set_location("Burma")
print python
print "Here we demonstrate python.eats"
print python.eats()
print

rattle = Snake("Ratty")
rattle.set_oviparous(False)
rattle.set_constriction(False)
rattle.set_venom(True)
rattle.color = 'Tan'
rattle.set_size(1.8)
rattle.set_location("Arizona")
print rattle
print "The snake %s's secret number is: %s" % (rattle.name,rattle._Reptile__seceret)  # a munged class name to get at a secret vabiable
print

gecko = Lizard("sticky")
gecko.set_oviparous(True)
gecko.sticky = True
#gecko.set_venom(False)
gecko.color ='brown'
gecko.set_size(60)
gecko.set_location("Hawaii")
print gecko
print "Here we demonstrate gecko.eats"
print gecko.eats()  # a method that overrides the reptile method
print

gila = Lizard("Sunshine")
gila.set_oviparous(True)
gila.sticky = False
gila.set_venom(True)
gila.color = 'Beady colors'
gila.set_size(500)
gila.set_location("Arizona")
gila._Reptile__seceret = Seceret.number(1000)  # Here, seceret the Classmethod, is being used as a instance method
print gila
print

iguana = Iguana("Scruffy")
iguana.set_oviparous(True)
iguana.sticky = False
iguana.set_venom(False)
iguana.color = 'green'
iguana.set_size(1000)
iguana.set_location("Oaxaca Mexico")
iguana._Reptile__seceret = Seceret.number(10000)  # Here, seceret the Classmethod, is being used as a instance method
print "This is a demonstration (Lame) of super()"
print iguana
print

dino = Reptile("Oldguy")
dino.set_oviparous(True)
dino.color = 'drab'
dino.set_size(1000)
dino.set_location("the jurasic")
print dino
print "The snake %s's secret number is: %s" % (dino.name,dino._Reptile__seceret)  # a munged class name to get at a secret vabiable
print

print "Demonstrating classmethods and staticmethods"
print "There are %s instances of Reptile referenced from dino" % dino.get_no_of_instance()  #These parens are really very necessary
print "There are %s instances of Reptile referenced from Reptile" % dino.get_no_of_instance()
print "this shows that it doesn't matter if you use the class Reptile, or the instance dino you get access to the 'uber ditzel'"
print

print "Demonstration of issubclass, is Lizard a subclass of Reptile?:"
if issubclass(Lizard,Reptile):
    print "The Lizard is a reptile"

print "Demonstration of issubclass, is Reptile a subclass of Lizard?, should be null:"
if issubclass(Reptile, Lizard):
    print "All reptiles are Lizards, thats probably not true"
print

print "This is a demonstration of staticmethods, in this case we test the class property is_connected, then set it and test it again:"
print "The reptile is connected? %s" % Reptile.is_connected() # called through the class
Reptile.connect()
print "The reptile is connected? %s" % dino.is_connected()    # again but called through the instnace
print


