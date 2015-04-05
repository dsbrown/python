#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# This is my demonstratin code for classes. Classes let us easily link data to
# behavior. They are building blocks in our Python programs. With them, we
# develop more complex models. Classes are a way of grouping related bits of
# information together into a single unit (also known as an object), along with
# functions that can be called to manipulate that object (also known as
# methods). For example, if you want to track information about a reptile, you
# might want to record their name, color, location and other critical traits, 
# and be able to manipulate all of these as a single unit.

# Python has classic classes and NEW classes 
# Classic classes look like this:
#     class Reptile:
 
#  New Class look like this:
    
#     class Reptile(object):
    
# Subtile, but importaint because many behaviors only work with one class or the other
# so pay attention. I think you are safer using the new classes.

import random
CONNECTED = False

class Seceret(object): 
    @classmethod
    def number(cls, multiplier):
        # This method can be used as an instance or static method.
        if not multiplier:
            multiplier = 10
        return int(random.random() * multiplier ) 

class Reptile(object):
    #This is reptile class example'
    venom = False
    legs = 4
    no_inst = 0
    __color = ""

    def __init__(self,n):
        self.name=n
        Reptile.no_inst = Reptile.no_inst + 1 # Notice we are using the class name, not self this is a class object
        self.__seceret = Seceret.number(100) # Here, seceret the Classmethod, is being used as a static method

    def __repr__(self):
            return "%s is an uknown %s reptile from %s it has %s legs, its about %s cm or meters or miles i am not sure" \
                % (self.name, self.color, self.location, self.legs, self.size)

    # Classmethod is a function decorator specified by using @classmethod before
    # "def." It is a combination of an instance, and static, method. It can be
    # called either way. It is useful when you need to create a function that deals
    # with the class itself because it  gets the class object  to work on instead of
    # the instance. For example If we want to get the no of instances, all we have
    # to do is something like below:
    @classmethod
    def get_no_of_instance(cls_obj):
        return cls_obj.no_inst

    # Staticmethods are useful when there is some functionality that relates to the
    # class, but does not need the class or any instance(s) to do  work such as
    # setting environmental variables, changing an attribute in another class, etc.
    # Use of a static and classmethods allows for better code maintenance
    # like a classmethod it can be called on a class or instance

    @staticmethod
    def is_connected():
        return (CONNECTED == True)

    @staticmethod
    def connect():
        global CONNECTED
        CONNECTED = True

    def __str__(self):
        return self.__repr__()


    # Property
    # A property gets and sets a value. A property can be assigned like a variable.
    # This causes the setter method to be executed. In this example, we pass two
    # arguments to the property built-in. We specify getname as the getter, and
    # setname as the setter. Code statements can be used in getters and setters, for
    # example we capitalizing the string passed to setname. Later we will print the
    # value of the name property. This will invoke the getname method.
    #
    # OK I found a fixed a problem 
    # Python has classic classes and NEW classes sort of like Coke Classic and New Coke
    # Originally the code below didn't work - why because I created the class like this:
    #
    # class Reptile:
    #
    # Where I run into the error:
    # Properties do not work for classic classes, but you don't get a clear error
    # when you try this. Your get method will be called, so it appears to work, but
    # upon attribute assignment, a classic class instance will simply set the value
    # in its dict without calling the property's set method, and after that, the
    # property's get method won't be called either. (You could override setattr to
    # fix this, but it would be prohibitively expensive.)
    #
    # To fix this you need to make in a New Class which you create this way:
    #
    # class Reptile(object):
    #
    # Then magically the code below starts to work. 
    #
    # This sort of historical cruft sucks about phyton, ah well ...
    #

    def get_color(self):
        return self._color

    def set_color(self, value):
        # When property is set, capitalize it.
        self._color = value.capitalize()

    color = property(get_color, set_color)

    def eats(self):
        return "Eats any creature it can fit in its mouth"

#Some methods that set properties

    def set_oviparous(self, i):
        self.oviparous = i

    def set_size(self, i):
        self.size = i

    def set_location(self, i):
        self.location = i

    def set_venom(self, i):
        self.venom = i


class Lizard(Reptile):
 #This is snake class example'
    legs = 4
    eyelids = True
    scales = True

    def __repr__(self):
        if self.venom:
            return "The venomous lizard  %s is a %s %s, from %s it has %s legs, its about %s cm" \
                % (self.name, self.color, self.identify(), self.location, self.legs, self.size)
        elif self.sticky:
            return "The non-venomous lizard %s is a geko, or geko like lizard with %s color.  %s. It is from %s it has %s legs, its about %s cm" \
                % (self.name, self.color, self.identify().capitalize(), self.location, self.legs, self.size)
        else:
            return "The non-venomous lizard %s's coloration is %s.  %s. It is from %s it has %s legs, its about %s cm" \
                % (self.name, self.color, self.identify().capitalize(), self.location, self.legs, self.size)

    def __str__(self):
        return self.__repr__()
 
    def set_venom(self, i):
        self.venom = i

    def identify(self):
        if self.venom:
            return "beaded lizard or gila monster"
        else:
            return "well at least its not poisonous"

    def eats(self):
        return "Depends on the species, most are carniverious; but the galapagos iguana eats seaweed"

# Super 
# With the super() built-in, we can get the parent of a class. This gets the
# immediate ancestor. Here we call super() within the Iguana class, which
# references its parent class, Lizard. In this case its pretty much useless but
# we demonstrate how to do something like print, then execute the parent class

# super() lets you avoid referring to the base class explicitly, but the main
# advantage comes with multiple inheritance, where dangerious things can happen
# super() only works for new-style classes.


class Iguana(Lizard):
    def __repr__(self):
        print "Iguana's are considered good eats" 
        # Call name method from parent class.
        return super(Iguana,self).__repr__()

    def __str__(self):
        return self.__repr__()


class Snake(Reptile):
    #This is snake class example'
    legs = 0
    eyelids = False
    scales = True

  
    def __repr__(self):
        s =""

        try:
            self.foo
        except AttributeError or NameError:
            s = ""
        else:
            s = "Oh look this snake is a Foo! "

        if self.venom:
            return s+"The venomous snake %s is a %s %s, from %s it has %s legs and %s eyelids, its about %s meters" % (self.name, self.color, self.identify(), self.location, self.legs, self.eyelids, self.size)
        else:
            return s+"The non-venomous snake %s is a %s %s, from %s it has %s legs and %s eyelids, its about %s meters" % (self.name, self.color, self.identify(), self.location, self.legs, self.eyelids, self.size)

    def __str__(self):
        return self.__repr__()

   
    def set_constriction(self, i):
        self.constriction = i

 
    def identify(self):
        if self.constriction and self.oviparous:
            return "python"
        elif self.constriction and not self.oviparous: 
            return "boa constrictor" 
        elif self.venom:
            return "dangerious snake (watch out)"

boa = Snake("Bubbles")
boa.set_oviparous(False)
boa.set_constriction(True)
boa.set_venom(False)
#boa.color = "yellow"
boa.color = "pink"
# This code demonstrates that you can pretty much assign any property you want to a class arbitrary
# and then recall it. When you do it you are putting the value in the class instances __dict__ 
# Here, I also test for the foo atribute in the Snake class and print something if it is.
# If its not defined, I just ignore it; but I have to put it in a Try: Except: block to avoid it
# erroring out because I don't define it everywhere. If I did go to the trouble of giving every 
# snake a foo I wouldn't need the test. Is sort of lazy programming; but it demonstrates how
# to handle it.
#
# This is all just to demonstrate the classic assignment of properities without a getter setter
# to see a real getter setter look at color
#
boa.foo = "bar"
boa.set_size(1.5)
boa.set_location("Equador")
print boa       # demonstrates teh __repr__ method
print str(boa)  # demonstrates the str method
print "Boa's foo is %s"%boa.foo

python = Snake("Poly")
python.set_oviparous(True)
python.set_constriction(True)
python.set_venom(False)
python.color = 'green'
python.set_size(1.8)
python.set_location("Burma")
print python
print python.eats()

rattle = Snake("Ratty")
rattle.set_oviparous(False)
rattle.set_constriction(False)
rattle.set_venom(True)
rattle.color = 'Tan'
rattle.set_size(1.8)
rattle.set_location("Arizona")
print "The snake %s's secret number is: %s" % (rattle.name,rattle._Reptile__seceret)  # a munged class name to get at a secret vabiable
print rattle

gecko = Lizard("sticky")
gecko.set_oviparous(True)
gecko.sticky = True
#gecko.set_venom(False)
gecko.color ='brown'
gecko.set_size(60)
gecko.set_location("Hawaii")
print gecko
print gecko.eats()  # a method that overrides the reptile method

gila = Lizard("Sunshine")
gila.set_oviparous(True)
gila.sticky = False
gila.set_venom(True)
gila.color = 'Beady colors'
gila.set_size(500)
gila.set_location("Arizona")
gila._Reptile__seceret = Seceret.number(1000)  # Here, seceret the Classmethod, is being used as a instance method
print gila

iguana = Iguana("Scruffy")
iguana.set_oviparous(True)
iguana.sticky = False
iguana.set_venom(False)
iguana.color = 'green'
iguana.set_size(1000)
iguana.set_location("Oaxaca Mexico")
iguana._Reptile__seceret = Seceret.number(10000)  # Here, seceret the Classmethod, is being used as a instance method
print iguana

dino = Reptile("Oldguy")
dino.set_oviparous(True)
dino.color = 'drab'
dino.set_size(1000)
dino.set_location("the jurasic")
print "The snake %s's secret number is: %s" % (dino.name,dino._Reptile__seceret)  # a munged class name to get at a secret vabiable
print dino

# Demonstrating classmethods and staticmethods
print "There are %s instances of Reptile referenced from dino" % dino.get_no_of_instance()  #These parens are really very necessary
print "There are %s instances of Reptile referenced from Reptile" % dino.get_no_of_instance()
print "this shows that it doesn't matter if you use the class Reptile, or the instance dino you get access to the 'uber ditzel'"

if issubclass(Lizard,Reptile):
    print "The Lizard is a reptile"

if issubclass(Reptile, Lizard):
    print "All reptiles are Lizards, thats probably not true"

print "The reptile is connected? %s" % Reptile.is_connected() # called through the class
Reptile.connect()
print "The reptile is connected? %s" % dino.is_connected()    # again but called through the instnace



