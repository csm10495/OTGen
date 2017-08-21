'''
Brief:
    File to make an Oregon Trail game save
    
License:
    MIT License
    
Author(s):
    Charles Machalow
'''

from ctypes import *
from pprint import pprint

try:
    input = raw_input
except:
    pass

TEMPERATURE_STRING = {
    0 : 'Very Cold',
    1 : 'Cold',
    2 : 'Cool',
    3 : 'Warm',
    4 : '@W have reached @N',
    5 : '',
}

OCCUPATION = {
    0 : 'Banker',
    1 : 'Blacksmith',
    2 : 'Carpenter',
    3 : 'Doctor',
    4 : 'Farmer',
    5 : 'Merchant',
    6 : 'Saddlemaker',
    7 : 'Teacher',
}

RATIONS = {
    0 : 'Filling',
    1 : 'Meager',
    2 : 'Bare-Bones'
}

PACE = {
    0 : 'Steady',
    1 : 'Strenuous',
    2 : 'Grueling',
}

STATUS = {
    0 : 'Default',
    1 : 'Exhaustion',
    2 : 'Typhoid',
    3 : 'Cholera',
    4 : 'Measles',
    5 : 'Dysentery',
    6 : 'Fever',
    7 : 'Broken Leg',
    8 : 'Broken Arm',
    9 : 'Snakebite',
    15 : 'Deceased',
}

class SaveFileStructure(Structure):
    _pack_ = 1
    _fields_ = [
        ('Company',           c_char * 4),   # MECC
        ('Reserved1',         c_uint8),
        ('GameTitle',         c_char * 28),  # The Oregon Trail for Windows
        ('Reserved2',         c_int8 * 36),
        ('SaveFileVersion',   c_char * 3),   # 1.0
        ('Reserved3',         c_int8 * 10),
        ('TemperatureString', c_uint8),      # Enum for string under thermometer
        ('Unknown1',          c_uint8),
        ('Unknown2',          c_uint8),
        ('Reserved4_1',       c_int8 * 7),
        ('DistanceTraveled',  c_int16),
        ('Reserved4_2',       c_int8 * 41),
        ('Unknown3',          c_uint8),
        ('Reserved5',         c_int8 * 2),
        ('DistanceToLandmark',c_int16),
        ('Reserved5_0_1',     c_int8 * 4),
        ('Rations',           c_int16),
        ('Pace',              c_uint8),
        ('Reserved5_1',       c_int8 * 3),
        ('Oxen',              c_int16),      # Number of Oxen
        ('Reserved6',         c_int8 * 2),
        ('SetsOfClothing',    c_int16),      # Number of Sets of Clothing
        ('Bullets',           c_int16),      # Number of Bullets
        ('SpareWagonWheels',  c_int16),      # Number of Spare Wagon Wheels
        ('SpareWagonAxels',   c_int16),      # Number of Spare Wagon Axels
        ('SpareWagonTongues', c_int16),      # Number of Spare Wagon Tongues
        ('NonPerishableFood', c_int16),      # Pounds of Non-Perishable Food
        ('PerishableFood',    c_int16),      # Pounds of Perishable Food
        ('MoneyInCents',      c_int32),      # Money in Cents
        ('OccupationValue',   c_uint16),     # Job Enumeration
        ('OccupationTitle',   c_char * 18),  # Job Title
        ('Leader',            c_char * 14),
        ('Reserved7',         c_int8),
        ('PartyMember1',      c_char * 14),
        ('Reserved8',         c_int8),
        ('PartyMember2',      c_char * 14),
        ('Reserved9',         c_int8),
        ('PartyMember3',      c_char * 14),
        ('Reserved10',        c_int8),
        ('PartyMember4',      c_char * 14),
        ('Reserved11',        c_int8),
        ('Reserved12',        c_int8 * 11),
        ('LeaderStatus',      c_int16),
        ('PartyMember1Status',c_int16),
        ('PartyMember2Status',c_int16),
        ('PartyMember3Status',c_int16),
        ('PartyMember4Status',c_int16),
        ('Reserved13',        c_int8 * 4),
        ('DateString',        c_char * 18),
        ('PlaceholderYear',   c_int16),      # Year that doesn't have an effect
        ('Year',              c_int16),      # Year
        ('MonthOfYear',       c_int16),      # Month Of The Year
        ('DayOfMonth',        c_int16),      # Day Of The Month
    ]
    
    DEFAULTS = {
        'Company' : "MECC",
        'GameTitle' : "The Oregon Trail for Windows",
        'SaveFileVersion' : "1.0",
    }

    STR_HELPER = {
        'TemperatureString' : TEMPERATURE_STRING,
        'OccupationValue': OCCUPATION,
        'Pace': PACE,
        'Rations': RATIONS,
        'LeaderStatus': STATUS,
        'PartyMember1Status': STATUS,
        'PartyMember2Status': STATUS,
        'PartyMember3Status': STATUS,
        'PartyMember4Status': STATUS,
    }

    def __str__(self):
        retStr = ''
        for fieldName, _ in self._fields_:
            #if fieldName.startswith('Reserved'):
            #    continue
            attr =  getattr(self, fieldName)
            if fieldName in self.STR_HELPER:
                attr = "%s (%s)" % (attr, self.STR_HELPER[fieldName].get(attr, 'Unknown'))

            try:
                retStr += "%-20s: 0x%X (%d)\n" % (fieldName, attr, attr)
            except:
                retStr += "%-20s: %s\n" % (fieldName, attr[:])
        return retStr

    @classmethod
    def fromFile(cls, file):
        with open(file, 'rb') as f:
            b = f.read()

        return cls.from_buffer(bytearray(b))
    
    def save(self):
        with open('save.gam', 'wb') as f:
            f.write(bytearray(self))
            
    @classmethod
    def makeSave(cls):
        s = cls()
        for i in s._fields_:
            name = i[0]
            typ = i[1]
            if name.startswith('Reserved') or name.startswith('Unknown'):
                continue
            if name in cls.DEFAULTS:
                val = cls.DEFAULTS[name]
            else:    
                if name in cls.STR_HELPER:
                    pprint(cls.STR_HELPER[name])
                    
                if typ != c_char:
                    print ("Max value is %d" % ((2 ** (sizeof(typ) * 8 - 1)) - 1))
                    
                val = ''
                while val == '':
                    val = input(name + ": ")
            
            try:
                setattr(s, name, val.encode())
            except:
                setattr(s, name, int(val))
                
        print ('Done')
        print (s)

        with open('save.gam', 'wb') as f:
            f.write(bytearray(s))
            
        print ("Wrote save file to save.gam")