from microbit import *
from math import pow

display.off()  # pin 6  
pin=[pin16,pin15,pin14,pin13,pin12,pin8,pin3,pin4]


def ecrireSurLeBus(octet):
  for i in range(8):
    pin[i].write_digital((octet & (1<<i))>>i)

def envoyerCommande(commande):
    pin6.write_digital(0) #Rs
    pin7.write_digital(1) #E
    ecrireSurLeBus(commande) 
    sleep(1)
    pin7.write_digital(0) #E
    
def initEcran():
    envoyerCommande(0x0E) #display on and cursor blink for 0x0D and not for 0x0E/ 0b00001101/ 0b00001110
    envoyerCommande(0x01) #clear display
    envoyerCommande(0x38) #function set 8 BITs
    
def afficherCaractere(k):
    pin6.write_digital(1) #Rs
    pin7.write_digital(1) #E
    ecrireSurLeBus(ord(k)) # the function ord() returns the Unicode code from a given character
    sleep(1)
    pin7.write_digital(0) #E
    
def afficherMessage(texte):
    for i in range(0,len(texte)):
        envoyerCommande(texte[i])
        
def afficherValeurDe(nombre):
    envoyerCommande(ord(nombre))
    
def positionnerCurseur(ligne,colonne):
    l=[0x80,0xC0]
    cmd=l[ligne-1]+(colonne-1)
    envoyerCommande(cmd)
    
def mesureDistance():
    tension=pin0.read_analog()*3.3/1023.0
    distance=29.988*pow(tension,-1.173)
    return distance,tension

# the main 

while True:
    envoyerCommande(0x01) #clear display
    distance ,tension=mesureDistance()
    afficherMessage('Vout (V)   d(cm)')
    positionnerCurseur(2,1)
    afficherMessage(str(tension)+'   '+str(distance))
    sleep(1000)
