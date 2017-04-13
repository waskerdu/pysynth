#music maker
import numpy as np
import wave,math
from collections import deque
import random

sRate=44100 #sample rate at 44.1 kHz
nSamplesTotal=0

def makeSinData(freq,leng):
    #global nSamplesTotal
    nSamples=sRate*leng
    #nSamplesTotal+=nSamples
    x=np.arange(nSamples)/float(sRate)
    vals = np.sin(2.0*math.pi*freq*x)
    #print vals
    #data = np.array(vals*32767, 'int16')#.tostring()
    #data = np.array(vals, 'int16')
    return vals

def makeNoteAdditive(freq,leng):
    global nSamplesTotal
    nSamples=sRate*leng
    nSamplesTotal+=nSamples
    samples = np.array([0]*nSamples, 'float32')
    for i in range(nSamples):
        samples[i]=(1.0-i/float(nSamples))#*math.sin(i*float(freq))
    vals=np.array([0]*nSamples,'float32')
    depth=5
    for i in range(depth):
        tempVals=makeSinData(freq*(i+1),leng)
        tempVals=tempVals/float(i+1)
        vals+=tempVals
    vals/=depth
    #vals+=makeSinData(freq,leng)
    '''vals+=makeSinData(freq*2,leng)
    vals+=makeSinData(freq*3,leng)
    vals+=makeSinData(freq*4,leng)
    vals+=makeSinData(freq*5,leng)
    vals+=makeSinData(freq*6,leng)'''
    #vals/=6
    vals*=samples
    print samples
    data = np.array(vals*32767, 'int16')
    return data.tostring()

def dequeGen(size):
    output=[]
    for i in range(size):
        newVal=random.random()-0.5
        newVal=np.clip(newVal,-0.5,0.5)
        output.append(newVal)
        #output.append(math.sin(i*3.14159)/10)
    print output
    return output

def makeNoteKS(freq,leng):
    leng=float(leng)
    global nSamplesTotal
    atten=0.996
    nSamples=int(sRate*leng)
    nSamplesTotal+=nSamples
    #init ring buffer
    buffSize=int(sRate/freq)
    x=np.arange(nSamples)/float(sRate)
    buff=deque(dequeGen(buffSize))
    #buff=deque([random.random() - 0.5 for i in range(buffSize)])
    #buff=deque([np.sin(2.0*math.pi*freq*i) for i in range(buffSize)])
    samples = np.array([0]*nSamples, 'float32')
    #perform ks algorithm
    for i in range(nSamples):
        samples[i]=buff[0]
        avg = atten*0.5*(buff[0] + buff[1])
        buff.append(avg)
        buff.popleft()        
    samples*=makeSinData(freq,leng)
    samples = np.array(samples*32767, 'int16')
    return samples.tostring()    

"""
pentatonic scale
C4     : 261.6
E-flat : 311.1
F      : 349.2
G      : 392.0
B-flat : 466.2

c3 to c5
C3	: 130.81	263.74
C#3/Db3 : 138.59	248.93
D3	: 146.83	234.96
D#3/Eb3 : 155.56	221.77
E3	: 164.81	209.33
F3	: 174.61	197.58
F#3/Gb3 : 185.00	186.49
G3	: 196.00	176.02
G#3/Ab3 : 207.65	166.14
A3	: 220.00	156.82
A#3/Bb3 : 233.08	148.02
B3	: 246.94	139.71
C4	: 261.63
C#4/Db4 : 277.18
D4	: 293.66
D#4/Eb4 : 311.13
E4	: 329.63
F4	: 349.23
F#4/Gb4 : 369.99
G4	: 392.00
G#4/Ab4 : 415.30
A4	: 440.00
A#4/Bb4 : 466.16
B4	: 493.88

"""

data="" 
data+=makeNoteAdditive(220,1)
#pentatonic blues ega bflat b dflat
'''data+=makeNoteKS(164.81,0.5)
data+=makeNoteKS(196.00,0.5)
data+=makeNoteKS(220.00,0.5)
data+=makeNoteKS(233.08,0.5)
data+=makeNoteKS(246.94,0.5)
data+=makeNoteKS(293.66,0.5)

data+=makeNoteKS(246.94,0.5)
data+=makeNoteKS(233.08,0.5)
data+=makeNoteKS(220.00,0.5)
data+=makeNoteKS(196.00,0.5)
data+=makeNoteKS(164.81,0.5)'''
'''data+=makeNoteKS(164.81,1.0)
data+=makeNoteKS(196.00,1.0)
data+=makeNoteKS(220.00,1.0)
data+=makeNoteKS(249.94,1.0)
data+=makeNoteKS(293.66,1.0)'''
'''data+=makeNoteKS(261.63,0.5)
data+=makeNoteKS(293.66,0.5)
data+=makeNoteKS(329.63,0.5)
data+=makeNoteKS(349.23,0.5)
data+=makeNoteKS(392.00,0.5)
data+=makeNoteKS(440.00,0.5)
data+=makeNoteKS(493.88,0.5)'''

'''data+=makeNoteKS(261.6,1)
data+=makeNoteKS(311.1,1)
data+=makeNoteKS(349.2,1)
data+=makeNoteKS(392.0,1)
data+=makeNoteKS(466.2,1)'''

data+=makeNoteAdditive(261.6,1)
data+=makeNoteAdditive(311.1,1)
data+=makeNoteAdditive(349.2,1)
data+=makeNoteAdditive(392.0,1)
data+=makeNoteAdditive(466.2,1)

file = wave.open('sine220.wav', 'wb')
file.setparams((1, 2, sRate, nSamplesTotal, 'NONE', 'uncompressed'))
file.writeframes(data)
file.close()