#decode password
def cesarDecriptor(pw, num):
    rpw = ''
    for l in pw:
        rpw += chr(ord(l)-num) 
    return rpw

def cesarEncriptor(pw, num):
    rpw = ''
    for l in pw:
        rpw += chr(ord(l)+num) 
    return rpw