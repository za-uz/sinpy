from pycurl import Curl
import datetime

MWM = 14
TX_SIZE = 8019
HASH_SIZE = 243

class Quatrits:
    
    def __init__(self, numtrits, data=None):
        if data == None:
            self.data = bytearray((numtrits - 1) // 4 + 1)
        else:
            self.data = bytearray(data)
        self.numtrits = numtrits

        if numtrits % 4 == 0:
            pass
        elif numtrits % 4 == 1:
            self.data[-1] = (self.data[-1] & 0b11000000) | 0b00101010   # set out of bound trits to -2
        elif numtrits % 4 == 2:
            self.data[-1] = (self.data[-1] & 0b11110000) | 0b00001010   # --"--
        elif numtrits % 4 == 3:
            self.data[-1] = (self.data[-1] & 0b11111100) | 0b00000010


    def __bytes__(self):
        return bytes(self.data)

    def __getitem__(self, key):
        if type(key) == int:
            if key < 0 or key >= self.numtrits:
                raise IndexError('Quatrits index out of range')
            result = 0
            if key % 4 == 0:
                result = (self.data[key // 4] & 0b11000000) >> 6
            elif key % 4 == 1:
                result = (self.data[key // 4] & 0b00110000) >> 4
            elif key % 4 == 2:
                result = (self.data[key // 4] & 0b00001100) >> 2
            elif key % 4 == 3:
                result = (self.data[key // 4] & 0b00000011)
            if result > 1:
                return result - 4
            return result
        elif type(key) == slice:
            start = key.start if key.start != None else 0
            stop = key.stop if key.stop != None else len(self)
            if key.step != None:
                raise NotImplementedError('step slicing not implemented')
            new_quatrits = Quatrits(stop - start)
            for i,j in zip(range(start, stop), range(len(new_quatrits))):
                new_quatrits[j] = self[i]
            return new_quatrits
        else:
            raise TypeError('Quatrit indices must be integers or slices, not %s' % type(key).__name__)


    def __setitem__(self, key, value):
        if type(key) == int:
            if key < 0 or key >= self.numtrits:
                raise IndexError('Quatrits index out of range')
            if value < 0:
                value += 4
            if key % 4 == 0:
                self.data[key // 4] &= 0b00111111
                self.data[key // 4] |= (value << 6)
            elif key % 4 == 1:
                self.data[key // 4] &= 0b11001111
                self.data[key // 4] |= (value << 4)
            elif key % 4 == 2:
                self.data[key // 4] &= 0b11110011
                self.data[key // 4] |= (value << 2)
            elif key % 4 == 3:
                self.data[key // 4] &= 0b11111100
                self.data[key // 4] |= (value)
        elif type(key) == slice:
            start = key.start if key.start != None else 0
            stop = key.stop if key.stop != None else len(self)
            if key.step != None:
                raise NotImplementedError('step slicing not implemented')
            for i,v in zip(range(start, stop), value):
                self[i] = v
        else:
            raise TypeError('Quatrit indices must be integers or slices, not %s' % type(key).__name__)
    
    def __len__(self):
        return self.numtrits

    @classmethod
    def fromlist(cls, l):
        new_quatrits = cls(len(l))
        for i in range(len(l)):
            new_quatrits[i] = l[i]
        return new_quatrits

    def __int__(self):
        result = 0
        for i in range(0, len(self)):
            result += self[i] * 3**i
        return result

def curlhash(quatrits):
    curl = Curl()
    curl.absorb(list(quatrits))
    tx_hash = []
    curl.squeeze(tx_hash)
    return Quatrits.fromlist(tx_hash)

def pow_done(tx_hash):
    for i in range(HASH_SIZE - MWM, HASH_SIZE):
        if tx_hash[i] != 0:
            return False
    return True

def timestamp_ok(tx):
    timestamp = int(tx[7857:7857+27])
    if timestamp / 1000 <= datetime.datetime.now().timestamp() + (60*60*2):
        return True
    return False

