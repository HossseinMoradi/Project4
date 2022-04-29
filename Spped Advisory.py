import math
import ast
from math import e
from decimal import *
import time
import random



getcontext().prec = 28


# first we have defined functions to access signals and vehicles data

def toList(NestedTuple):
    return list(map(toList, NestedTuple)) if isinstance(NestedTuple, (list, tuple)) else NestedTuple

# we want to access vehicles information. In the first part of the below function, we determine the pieces of data that are collected. In the secoond part we determine that which types of vehicles are CV/special (i.e, sending information) 
def GetVissimDataVehicles():
    global vehsAttributes
    global vehsAttNames
    vehsAttributesNames = ['No', 'VehType\No', 'Pos', 'VehType\No', 'Lane\Link','DesSpeed', 'Speed', 'DistanceToSigHead','InQueue']
    vehsAttributes = toList(Vissim.Net.Vehicles.GetMultipleAttributes(vehsAttributesNames))
    vehsAttNames = {}
    cnt = 0
    for att in vehsAttributesNames:
        vehsAttNames.update({att: cnt})
        cnt += 1
    global vehTypesEquipped
    global vehTypesSpecial
    vehTypesAttributes = Vissim.Net.VehicleTypes.GetMultipleAttributes(['No', 'IsCV', 'IsSpecial'])
    vehTypesEquipped = [x[0] for x in vehTypesAttributes if x[1] == True]
    vehTypesSpecial = [x[0] for x in vehTypesAttributes if x[2] == True]



def Signal():
    #we define a user attributre to access SimSec
    Vissim.Net.SignalControllers.ItemByKey(1).SetAttValue('SimSec',Vissim.Net.Simulation.SimulationSecond)
    Seconds = Vissim.Net.SignalControllers.ItemByKey(1).AttValue('CycSec')
    SimSec = Vissim.Net.SignalControllers.ItemByKey(1).AttValue('SimSec')
    CLength = 60
    GetVissimDataVehicles()
    deltaT=1
    #we should correlate deltaT with the simulation resolution. In other words, number of simulation per second should be one here. 
    Starting_time=0
    Ending_time=1000
    
    TimeNo=[]
    i=Starting_time
    k=0
    while i< Ending_time:
        TimeNo.append(k)
        k+=1
        i=i+deltaT


     # Here we define the following attributes: TimeUntilNextGreen, TimeUntilNextRed, CycleDuration
    
    for i in TimeNo:
        if SimSec > (i)*deltaT and SimSec <= (i+1)*deltaT:
            # this is anexample of a case where green time durations and cycles are varying at each time step
            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('SigState')=='RED':
                if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart'):
                    G1=random.randint(10,17)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenTimeDuration', G1)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('TimeUntilNextGreen', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart')-SimSec)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('TimeUntilNextRed', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('TimeUntilNextGreen')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenTimeDuration'))                    
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart') < SimSec :
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('TimeUntilNextGreen', Vissim.Net.SignalControllers.ItemByKey(1).AttValue('CycleDuration')+ Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart')-SimSec)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('TimeUntilNextRed', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('TimeUntilNextGreen')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenTimeDuration'))                    
                    
            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('SigState')=='GREEN': 
                G1=max(random.randint(10,17),SimSec-Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart'))
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenTimeDuration', G1)
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('TimeUntilNextGreen', -1)
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('TimeUntilNextRed', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd')-SimSec)                    
                   


            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('SigState')=='RED':
                if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenStart'):               
                    G2=random.randint(10,17)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('GreenTimeDuration', G2)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('TimeUntilNextGreen', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenStart')-SimSec)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('TimeUntilNextRed', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('TimeUntilNextGreen')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenTimeDuration'))                    

                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenStart') < SimSec :
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('TimeUntilNextGreen', Vissim.Net.SignalControllers.ItemByKey(1).AttValue('CycleDuration')+ Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenStart')-SimSec)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('TimeUntilNextRed', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('TimeUntilNextGreen')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenTimeDuration'))                    


            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('SigState')=='GREEN':
                G2=max(random.randint(10,17),SimSec-Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenStart'))
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('GreenTimeDuration', G2)
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('TimeUntilNextGreen', -1)
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('TimeUntilNextRed', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd')-SimSec)   

            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('SigState')=='RED':
                if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenStart'):
                    G3=random.randint(10,17)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('GreenTimeDuration', G3)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('TimeUntilNextGreen', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenStart')-SimSec)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('TimeUntilNextRed', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('TimeUntilNextGreen')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenTimeDuration'))                    

                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenStart') < SimSec :
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('TimeUntilNextGreen', Vissim.Net.SignalControllers.ItemByKey(1).AttValue('CycleDuration')+ Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenStart')-SimSec)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('TimeUntilNextRed', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('TimeUntilNextGreen')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenTimeDuration'))                    



            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('SigState')=='GREEN':
                G3=max(random.randint(10,17),SimSec-Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenStart'))
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('GreenTimeDuration', G3)
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('TimeUntilNextGreen', -1)
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('TimeUntilNextRed', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd')-SimSec) 

            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('SigState')=='RED':
                if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenStart'):
                    G4=random.randint(10,17)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('GreenTimeDuration', G4)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('TimeUntilNextGreen', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenStart')-SimSec)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('TimeUntilNextRed', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('TimeUntilNextGreen')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenTimeDuration'))                    

                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenStart') < SimSec :
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('TimeUntilNextGreen', Vissim.Net.SignalControllers.ItemByKey(1).AttValue('CycleDuration')+ Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenStart')-SimSec)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('TimeUntilNextRed', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('TimeUntilNextGreen')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenTimeDuration'))                    



            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('SigState')=='GREEN':
                G4=max(random.randint(10,17),SimSec-Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenStart'))
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('GreenTimeDuration', G4)
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('TimeUntilNextGreen', -1)
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('TimeUntilNextRed', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd')-SimSec) 


            Vissim.Net.SignalControllers.ItemByKey(1).SetAttValue('CycleDuration',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenTimeDuration')+8)
            Vissim.Net.SignalControllers.ItemByKey(1).SetAttValue('CycleEnd',Vissim.Net.SignalControllers.ItemByKey(1).AttValue('CycleStart')+Vissim.Net.SignalControllers.ItemByKey(1).AttValue('CycleDuration'))
            
            
            
            

    if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd'):
        if SimSec <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd')+2:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenStart', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd')+2)
            Vissim.Net.SignalControllers.ItemByKey(1).SetAttValue('CycleStart', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart')-2)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenEnd', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart') + Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenTimeDuration'))
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd') + 2)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenStart') + Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenTimeDuration'))
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd') + 2)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenStart') + Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenTimeDuration'))
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd') + 2)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenStart') + Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenTimeDuration'))




    # you have to make a use of simsec to define variable cycle time
    # To this end, we firs, define three attributes in the current signal controller with the names of CycleStart, CycleEnd, CycleDuration. 

    
    SimSec = Vissim.Net.SignalControllers.ItemByKey(1).AttValue('SimSec')
    #we determine Initial values OF CYCLE START
    if SimSec<=1:
        Vissim.Net.SignalControllers.ItemByKey(1).SetAttValue('CycleStart', 0)



    # When we start the simulation, we determine that the signals are operating upon com script.
    if SimSec<=1:

        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('ContrByCOM', True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('ContrByCOM', True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('ContrByCOM', True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('ContrByCOM', True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenStart',2)



    if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart') - 1:
        if SimSec <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')
        if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd') - 1:
            if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd') + 1:
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

    if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenStart') - 1:
        if SimSec <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')

        if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd') - 1:
            if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd') + 1:
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

    if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenStart') - 1:
        if SimSec <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

        if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd') - 1:
            if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd') + 1:
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

    if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenStart') - 1:
        if SimSec <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')

        if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')




def ChangeSpeed():

    GetVissimDataVehicles() 
    MinSpeed=5
    MaxSpeed=76

    if len(vehsAttributes) > 1: 
        for vehAttributes in vehsAttributes:
            if vehAttributes[vehsAttNames['VehType\\No']] in vehTypesEquipped: 
                # set easier variables of the current vehicle:
                DesSpeed = vehAttributes[vehsAttNames['DesSpeed']]
                Speed = vehAttributes[vehsAttNames['Speed']]
                DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                # if the vehicle does not have a upcoming signal: set original desired speed
                if DistanceToSigHead <= 0:
                    vehAttributes[vehsAttNames['DesSpeed']] = MaxSpeed
                    continue # jump to next vehicle
                elif vehAttributes[vehsAttNames['Lane\Link']] == '1':
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('TimeUntilNextGreen')==-1:
                        vehAttributes[vehsAttNames['DesSpeed']] = MaxSpeed
                            
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('TimeUntilNextGreen')!=-1:
                        vehAttributes[vehsAttNames['DesSpeed']] = MinSpeed
                        
        vehicleNumDesiredSpeeds = [[x[vehsAttNames['DesSpeed']], x[vehsAttNames['Speed']]] for x in vehsAttributes]
        Vissim.Net.Vehicles.SetMultipleAttributes(('DesSpeed', 'Speed'), vehicleNumDesiredSpeeds)
        
