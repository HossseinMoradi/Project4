import math

def toList(NestedTuple):
    return list(map(toList, NestedTuple)) if isinstance(NestedTuple, (list, tuple)) else NestedTuple

def Init():
    global minSpeed
    global MaxSpeed
    global vehTypesEquipped
    global LinkA
    global LinkB
    global LinkC
    global LinkD
    global GV
    global EV
    global GVCAV
    global ECAV
    global HCAV
    global SignalA
    global signalB
    global SignalC
    global SignalD
    global vehsAttributes
    global vehsAttNames
    global linkAttributes
    global linAttNames
    global signalAttributes
    global SigAttNames
    minSpeed = CurrentScript.AttValue('minSpeed')
    MaxSpeed = CurrentScript.AttValue('MaxSpeed')
    vehsAttributes = []
    vehsAttNames = []
    linkAttributes = []
    linAttNames = []
    signalAttributes = []
    SigAttNames = []
    
    vehTypesAttributes = Vissim.Net.VehicleTypes.GetMultipleAttributes(['No', 'ReceiveSignalInformation','GV','EV','GVCAV','ECAV','HCAV'])
    vehTypesEquipped = [x[0] for x in vehTypesAttributes if x[1] == True]
    GV = [x[0] for x in vehTypesAttributes if x[2] == True]
    EV = [x[0] for x in vehTypesAttributes if x[3] == True]
    GVCAV = [x[0] for x in vehTypesAttributes if x[4] == True]
    ECAV = [x[0] for x in vehTypesAttributes if x[5] == True]
    HCAV = [x[0] for x in vehTypesAttributes if x[6] == True]
    
    LinkTypesAttributes = Vissim.Net.Links.GetMultipleAttributes(['No', 'linkA', 'linkB', 'linkC', 'linkD'])
    LinkA = [x[0] for x in LinkTypesAttributes if x[1] == True]
    LinkB = [x[0] for x in LinkTypesAttributes if x[2] == True]
    LinkC = [x[0] for x in LinkTypesAttributes if x[3] == True]
    LinkD = [x[0] for x in LinkTypesAttributes if x[4] == True]
    
    sigTypesAttributes =  Vissim.Net.SignalControllers.ItemByKey(1).SGs.GetMultipleAttributes(['No', 'SignalA', 'SignalB', 'SignalC', 'SignalD', 'TimeUntilNextGreen','TimeUntilNextRed'])
    SignalA = [x[0] for x in sigTypesAttributes if x[1] == True]
    SignalB = [x[0] for x in sigTypesAttributes if x[2] == True]
    SignalC = [x[0] for x in sigTypesAttributes if x[3] == True]
    SignalD = [x[0] for x in sigTypesAttributes if x[4] == True]
    
    

def GetVissimDataVehicles():
    global vehsAttributes
    global vehsAttNames
    vehsAttributesNames = ['No', 'VehType\No','Speed' , 'DesSpeed', 'OrgDesSpeed', 'DistanceToSigHead', 'SpeedMaxForGreenStart', 'SpeedMinForGreenEnd', 'Acceleration', 'Lane\Link']
    vehsAttributes = toList(Vissim.Net.Vehicles.GetMultipleAttributes(vehsAttributesNames))
    vehsAttNames = {}
    cnt = 0
    for att in vehsAttributesNames:
        vehsAttNames.update({att: cnt})
        cnt += 1

def GetSignalsData():
    global signalAttributes
    global SigAttNames
    SignalAttributesNames = ['No','Name','Type','TimeUntilNextGreen','TimeUntilNextRed', 'SignalA', 'SignalB', 'SignalC', 'SignalD']
    SignalAttributes = toList(Vissim.Net.SignalControllers.ItemByKey(1).SGs.GetMultipleAttributes(SignalAttributesNames))
    SigAttNames = {}
    ctt = 0
    for ftt in SignalAttributesNames:
        SigAttNames.update({ftt: ctt})
        ctt += 1


def ChangeSpeed():
    GetVissimDataVehicles()
    GetSignalsData()

    if len(vehsAttributes) > 1:
        for vehAttributes in vehsAttributes:
            if vehAttributes[vehsAttNames['VehType\No']] in vehTypesEquipped:
                No = vehAttributes[vehsAttNames['VehType\No']]
                DesSpeed = vehAttributes[vehsAttNames['DesSpeed']]
                OrgDesSpeed = vehAttributes[vehsAttNames['OrgDesSpeed']]
                Speed = vehAttributes[vehsAttNames['Speed']]
                DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                SpeedMaxForGreenStart = vehAttributes[vehsAttNames['SpeedMaxForGreenStart']]
                SpeedMinForGreenEnd = vehAttributes[vehsAttNames['SpeedMinForGreenEnd']]
                Link= vehAttributes[vehsAttNames['Lane\Link']]
                if OrgDesSpeed == None:
                    OrgDesSpeed = DesSpeed
                    vehAttributes[vehsAttNames['OrgDesSpeed']] = DesSpeed
                
                if DistanceToSigHead <= 0:
                    vehAttributes[vehsAttNames['DesSpeed']] = OrgDesSpeed
                    continue
                i=0
                v1=0
                vstar=[]
                while v1<= (MaxSpeed/3.6) - (minSpeed/3.6):
                    v1 = v1+(minSpeed/3.6)
                    vstar.append(v1)

                vv=[]
                for i in vstar:
                    vv.append(Speed)
                i=0
                a1=[]
                a=0
                while i < len(vv):
                    if vv[i] == vstar[i]:
                        a=0
                    if vv[i] != vstar[i]:
                        a = 4*(1-pow((vv[i]/vstar[i]),4))
                    a1.append(a)
                    i+=1
                i=0
                while i<len(vv):
                    if a1[i]> 4:
                        a1[i] = 4
                    if a1[i]<-4:
                        a1[i] = -4
                    i+=1
                t11=[]
                i=0
                t=0
                while i<len(vv):
                    if a1[i]==0:
                        t=0
                    else:
                        t=(vstar[i]-vv[i])/a1[i]
                    t11.append(t)
                    i+=1

                x3=[]
                x1=0
                t=0
                i=0
                t22=[]
                m=0
                while i<len(vv):
                    x1 = 0.5 * a1[i] * t11[i] * t11[i] + vv[i] * t11[i]
                    
                    if x1 == DistanceToSigHead:
                        t=t11[i]
                    elif DistanceToSigHead < x1:
                        if a1[i] != 0:
                            t = (-vv[i]+math.sqrt(vv[i]*vv[i]+2*a1[i]*DistanceToSigHead))/a1[i]
                        else:
                            t = DistanceToSigHead/vv[i]
                    else:
                        x2=DistanceToSigHead-x1
                        t= t11[i] + x2/vstar[i]
                    t22.append(t)
                    i+=1

                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)

                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)

                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)

                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)

                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LinkNo')==5:
                    i=0
                    Time=[]
                    while i < len(t22):
                        uu = t22[i]                    
                        if uu>= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('TimeUntilNextGreen') and uu <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('TimeUntilNextRed'):
                            Time.append(t22[i])
                        i+=1
                    if len(Time)==0:
                        Time.append(60)                        
                    VVP=[]
                    AAP=[]
                    i=0
                    while i< len(vv):
                        VP=[]
                        AP=[]
                        j=0
                        vvv=0
                        aaa = 0
                        while j < t22[i]:
                            while j <= t11[i]:
                                vvv = a1[i] * j + vv[i]
                                VP.append(vvv)
                                aaa = a1[i]
                                AP.append(aaa)
                                j+=1
                            vvv = vstar[i]
                            VP.append(vvv)
                            aaa=0
                            AP.append(aaa)
                            j+=1
                        try:
                            if j>=Time[0] and j<=Time[-1]:
                                VVP.append(VP)
                                AAP.append(AP)
                        except: 
                            VVP =[[vv[i]]]
                            AAP = [[0]]
                        i+=1
                    
                    F=[]
                    f=0
                    for z in VVP:
                        for n in AAP:
                            y=0
                            i=0
                            while i < len(z):
                                y = y + z[i]
                                i+=1
                                if y < DistanceToSigHead:
                                    continue
                                else:
                                    break
                            
                            j=0
                            if No == 101:
                                while j < i:
                                    f = f + (0.003 * ( 1256 * n[j] + 1.3 * z[j] * z[j])* ( 1256 * n[j] + 1.3 * z[j] * z[j]) +  z[j] * (1.3 * z[j] * z[j] + 0.006 * 1256 + 9.8) + 0.95 * 1256 * n[j] * z[j])
                                    j+=1
                                F.append(f)

                            else:
                                while j < i:
                                    f=f+(max((0.444 + 0.09 * z[j] * (0.333 + 0.00108 * z[j] * z[j] * 1256 * n[j]) + 0.04 * 1256 * z[j] * n[j] * n[j]), 0.444))
                                    j+=1
                                F.append(f)

                    try:
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('Time1',F[0])
                    except:
                        F.append (0)


                    FF=[]
                    kk=0
                    fff=0
                    while kk< len(F):
                        fff=fff+F[kk]
                        kk+=1
                    FF.append(fff)


                    
                    try:
                        desSpeed=VVP[F.index(min(FF))][-1]
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('Time2',desSpeed)
                        
                    except:
                        desSpeed= vehAttributes[vehsAttNames['Speed']]
                    
                    optimalSpeed=0
                
                    if SpeedMinForGreenEnd < desSpeed:
                        optimalSpeed = desSpeed
                    else:
                        optimalSpeed = SpeedMinForGreenEnd
                    
                    if optimalSpeed < SpeedMaxForGreenStart:
                        optimalSpeed = optimalSpeed
                    else:
                        optimalSpeed = SpeedMaxForGreenStart
                    if SpeedMinForGreenEnd > SpeedMaxForGreenStart:
                        optimalSpeed = OrgDesSpeed
                    

                    
                        
                    vehAttributes[vehsAttNames['DesSpeed']] = optimalSpeed

                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LinkNo')==7:
                    i=0
                    Time=[]
                    while i < len(t22):
                        uu = t22[i]                    
                        if uu>= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('TimeUntilNextGreen') and uu <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('TimeUntilNextRed'):
                            Time.append(t22[i])
                        i+=1
                    if len(Time)==0:
                        Time.append(60)                        
                    VVP=[]
                    AAP=[]
                    i=0
                    while i< len(vv):
                        VP=[]
                        AP=[]
                        j=0
                        vvv=0
                        aaa = 0
                        while j < t22[i]:
                            while j <= t11[i]:
                                vvv = a1[i] * j + vv[i]
                                VP.append(vvv)
                                aaa = a1[i]
                                AP.append(aaa)
                                j+=1
                            vvv = vstar[i]
                            VP.append(vvv)
                            aaa=0
                            AP.append(aaa)
                            j+=1
                        try:
                            if j>=Time[0] and j<=Time[-1]:
                                VVP.append(VP)
                                AAP.append(AP)
                        except: 
                            VVP =[[vv[i]]]
                            AAP = [[0]]
                        i+=1
                    
                    F=[]
                    f=0
                    for z in VVP:
                        for n in AAP:
                            y=0
                            i=0
                            while i < len(z):
                                y = y + z[i]
                                i+=1
                                if y < DistanceToSigHead:
                                    continue
                                else:
                                    break
                            
                            j=0
                            if No == 101:
                                while j < i:
                                    f = f + (0.003 * ( 1256 * n[j] + 1.3 * z[j] * z[j])* ( 1256 * n[j] + 1.3 * z[j] * z[j]) +  z[j] * (1.3 * z[j] * z[j] + 0.006 * 1256 + 9.8) + 0.95 * 1256 * n[j] * z[j])
                                    j+=1
                                F.append(f)

                            else:
                                while j < i:
                                    f=f+(max((0.444 + 0.09 * z[j] * (0.333 + 0.00108 * z[j] * z[j] * 1256 * n[j]) + 0.04 * 1256 * z[j] * n[j] * n[j]), 0.444))
                                    j+=1
                                F.append(f)

                    try:
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('Time1',F[0])
                    except:
                        F.append (0)

                    FF=[]
                    kk=0
                    fff=0
                    while kk< len(F):
                        fff=fff+F[kk]
                        kk+=1
                    FF.append(fff)


                    
                    try:
                        desSpeed=VVP[F.index(min(FF))][-1]
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('Time2',desSpeed)
                        
                    except:
                        desSpeed= vehAttributes[vehsAttNames['Speed']]
                    
                    optimalSpeed=0
                
                    if SpeedMinForGreenEnd < desSpeed:
                        optimalSpeed = desSpeed
                    else:
                        optimalSpeed = SpeedMinForGreenEnd
                    
                    if optimalSpeed < SpeedMaxForGreenStart:
                        optimalSpeed = optimalSpeed
                    else:
                        optimalSpeed = SpeedMaxForGreenStart
                    if SpeedMinForGreenEnd > SpeedMaxForGreenStart:
                        optimalSpeed = OrgDesSpeed
                    

                    
                        
                    vehAttributes[vehsAttNames['DesSpeed']] = optimalSpeed


                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LinkNo')==1:
                    i=0
                    Time=[]
                    while i < len(t22):
                        uu = t22[i]                    
                        if uu>= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('TimeUntilNextGreen') and uu <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('TimeUntilNextRed'):
                            Time.append(t22[i])
                        i+=1
                    if len(Time)==0:
                        Time.append(60)                        
                    VVP=[]
                    AAP=[]
                    i=0
                    while i< len(vv):
                        VP=[]
                        AP=[]
                        j=0
                        vvv=0
                        aaa = 0
                        while j < t22[i]:
                            while j <= t11[i]:
                                vvv = a1[i] * j + vv[i]
                                VP.append(vvv)
                                aaa = a1[i]
                                AP.append(aaa)
                                j+=1
                            vvv = vstar[i]
                            VP.append(vvv)
                            aaa=0
                            AP.append(aaa)
                            j+=1
                        try:
                            if j>=Time[0] and j<=Time[-1]:
                                VVP.append(VP)
                                AAP.append(AP)
                        except: 
                            VVP =[[vv[i]]]
                            AAP = [[0]]
                        i+=1
                    
                    F=[]
                    f=0
                    for z in VVP:
                        for n in AAP:
                            y=0
                            i=0
                            while i < len(z):
                                y = y + z[i]
                                i+=1
                                if y < DistanceToSigHead:
                                    continue
                                else:
                                    break
                            
                            j=0
                            if No == 101:
                                while j < i:
                                    f = f + (0.003 * ( 1256 * n[j] + 1.3 * z[j] * z[j])* ( 1256 * n[j] + 1.3 * z[j] * z[j]) +  z[j] * (1.3 * z[j] * z[j] + 0.006 * 1256 + 9.8) + 0.95 * 1256 * n[j] * z[j])
                                    j+=1
                                F.append(f)

                            else:
                                while j < i:
                                    f=f+(max((0.444 + 0.09 * z[j] * (0.333 + 0.00108 * z[j] * z[j] * 1256 * n[j]) + 0.04 * 1256 * z[j] * n[j] * n[j]), 0.444))
                                    j+=1
                                F.append(f)

                    try:
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('Time1',F[0])
                    except:
                        F.append (0)

                    FF=[]
                    kk=0
                    fff=0
                    while kk< len(F):
                        fff=fff+F[kk]
                        kk+=1
                    FF.append(fff)


                    
                    try:
                        desSpeed=VVP[F.index(min(FF))][-1]
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('Time2',desSpeed)
                        
                    except:
                        desSpeed= vehAttributes[vehsAttNames['Speed']]
                    
                    optimalSpeed=0
                
                    if SpeedMinForGreenEnd < desSpeed:
                        optimalSpeed = desSpeed
                    else:
                        optimalSpeed = SpeedMinForGreenEnd
                    
                    if optimalSpeed < SpeedMaxForGreenStart:
                        optimalSpeed = optimalSpeed
                    else:
                        optimalSpeed = SpeedMaxForGreenStart
                    if SpeedMinForGreenEnd > SpeedMaxForGreenStart:
                        optimalSpeed = OrgDesSpeed
                    

                    
                        
                    vehAttributes[vehsAttNames['DesSpeed']] = optimalSpeed





                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LinkNo')==3:
                    i=0
                    Time=[]
                    while i < len(t22):
                        uu = t22[i]                    
                        if uu>= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('TimeUntilNextGreen') and uu <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('TimeUntilNextRed'):
                            Time.append(t22[i])
                        i+=1
                    if len(Time)==0:
                        Time.append(60)                        
                    VVP=[]
                    AAP=[]
                    i=0
                    while i< len(vv):
                        VP=[]
                        AP=[]
                        j=0
                        vvv=0
                        aaa = 0
                        while j < t22[i]:
                            while j <= t11[i]:
                                vvv = a1[i] * j + vv[i]
                                VP.append(vvv)
                                aaa = a1[i]
                                AP.append(aaa)
                                j+=1
                            vvv = vstar[i]
                            VP.append(vvv)
                            aaa=0
                            AP.append(aaa)
                            j+=1
                        try:
                            if j>=Time[0] and j<=Time[-1]:
                                VVP.append(VP)
                                AAP.append(AP)
                        except: 
                            VVP =[[vv[i]]]
                            AAP = [[0]]
                        i+=1
                    
                    F=[]
                    f=0
                    for z in VVP:
                        for n in AAP:
                            y=0
                            i=0
                            while i < len(z):
                                y = y + z[i]
                                i+=1
                                if y < DistanceToSigHead:
                                    continue
                                else:
                                    break
                            
                            j=0
                            if No == 101:
                                while j < i:
                                    f = f + (0.003 * ( 1256 * n[j] + 1.3 * z[j] * z[j])* ( 1256 * n[j] + 1.3 * z[j] * z[j]) +  z[j] * (1.3 * z[j] * z[j] + 0.006 * 1256 + 9.8) + 0.95 * 1256 * n[j] * z[j])
                                    j+=1
                                F.append(f)

                            else:
                                while j < i:
                                    f=f+(max((0.444 + 0.09 * z[j] * (0.333 + 0.00108 * z[j] * z[j] * 1256 * n[j]) + 0.04 * 1256 * z[j] * n[j] * n[j]), 0.444))
                                    j+=1
                                F.append(f)

                    try:
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('Time1',F[0])
                    except:
                        F.append (0)

                    FF=[]
                    kk=0
                    fff=0
                    while kk< len(F):
                        fff=fff+F[kk]
                        kk+=1
                    FF.append(fff)


                    
                    try:
                        desSpeed=VVP[F.index(min(FF))][-1]
                        
                        
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('Time2',desSpeed)
                        
                    except:
                        desSpeed= vehAttributes[vehsAttNames['Speed']]
                    
                    optimalSpeed=0
                
                    if SpeedMinForGreenEnd < desSpeed:
                        optimalSpeed = desSpeed
                    else:
                        optimalSpeed = SpeedMinForGreenEnd
                    
                    if optimalSpeed < SpeedMaxForGreenStart:
                        optimalSpeed = optimalSpeed
                    else:
                        optimalSpeed = SpeedMaxForGreenStart
                    if SpeedMinForGreenEnd > SpeedMaxForGreenStart:
                        optimalSpeed = OrgDesSpeed
                    

                    
                        
                    vehAttributes[vehsAttNames['DesSpeed']] = optimalSpeed



        vehicleNumDesiredSpeeds = [[x[vehsAttNames['DesSpeed']], x[vehsAttNames['OrgDesSpeed']]] for x in vehsAttributes]
        Vissim.Net.Vehicles.SetMultipleAttributes(('DesSpeed', 'OrgDesSpeed'), vehicleNumDesiredSpeeds)
                

                    
                    