__author__ = 'Bersik'

from spyne.model.complex import ComplexModel
from spyne.model.primitive import String
from spyne.model.primitive import UnsignedInt, Int
from spyne.model.complex import XmlAttribute


class Student(ComplexModel):
    __namespace__ = 'students'

    name = String
    surname = String
    age = UnsignedInt
    group = String
    hostel = UnsignedInt
    room = UnsignedInt
    idn = XmlAttribute(Int)
