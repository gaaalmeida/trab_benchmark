from math import pow


def bytesToGb(value):
    return value / pow(10,9)

def bytesToGb1024(value):
    return value / pow(1024,3)

def bytesToMb(value):
    return value / pow(10,6)

def megabytesToGb(value):
    return value / pow(10,3)

def megabytesToGb1024(value):
    return value / 1024