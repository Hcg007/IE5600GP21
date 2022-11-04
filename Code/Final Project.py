
from BaseInformationSystem import BaseInformationSystem
class returnin(BaseInformationSystem):
    def __init__(self):
        BaseInformationSystem.__init__(self)
        
    def csv2Dict(self, csv):
        with open(csv, 'r') as f:
            infoList=[]
            keys = f.readline().split(',')
            for i in range(len(keys)):
                keys[i] = keys[i].replace(' ', '')
                keys[i] = keys[i].replace('\n', '')
            for i in f:
                infoList.append(i.split(','))
            for i in range(len(infoList)):
                for j in range(len(infoList[i])):
                    infoList[i][j] = infoList[i][j].replace(' ', '')
                    infoList[i][j] = infoList[i][j].replace('\n', '')

            for i in range(len(infoList)):
                infoList[i] = dict(zip(keys, infoList[i]))

        return infoList
    
    def ReadCsvKeys(self, csvpath):
            with open(csvpath, 'r') as f:
                keys = f.readline().split(',')
                for i in range(len(keys)):
                    keys[i] = keys[i].replace(' ', '')
                    keys[i] = keys[i].replace('\n', '')
            return keys
    
    
    def return_auditinventory(self):
        for i in range(len(self.ReturnwarehouseKeys)-1):
            if i in self.InventoryInfoKeys:
                pass
            else:
                print('unvalid returning order')
                return
        else:
            print('Approved order')
                
    def return_auditsupplier(self):
        for i in range(len(self.Returnsupplierkeys)-1):
            if i in self.InventoryInfoKeys:
                pass
            else:
                print('unvalid returning order')
                return
        else:
            print('Approved order')
    
    def return_cangku(self):
        number=[]
        for j in self.Returnwarehouse:
            for i in self.InventoryInfo:
                if i['ItemNumber'] == j['ItemNumber']:
                    Max = int(i['MaxInventory'])
                    CI1 = int(i['CurrentInventory'])
                    CI2 = int(j['CurrentInventory'])
                    CI = CI1 + CI2
                    if CI > Max:
                        print('The maximum storage capacity of {} is exceeded' . format(i['ItemNumber']))
                        continue
                    else:
                        i['CurrentInventory'] = str(CI)
                        number.append(j)
                        break
                        
            else:
                for i in self.Returnwarehouse:
                    number.append(i)
                    i.pop('backreason')
                    self.InventoryInfo.append(i)
       
        for n in number:
            if n in self.Returnwarehouse:
                self.Returnwarehouse.remove(n)
        else:
            pass
            
        print('='*100)         
        print('left in inventory: \n',self.InventoryInfo)
        return self.outputcsb(self.InventoryInfo)
        
     
    def return_shangjia(self):
        number=[]
        for i in self.Returnsupplier:
            for j in self.InventoryInfo:
                if i['ItemNumber']==j['ItemNumber']:
                    CI1 = int(i['CurrentInventory'])
                    CI2 = int(j['CurrentInventory'])
                    if CI1 > CI2:
                        print('The number of {} returns exceeds the inventory' . format(i['ItemNumber']))
                        continue
                    else:
                        CI = CI2 - CI1
                        j['CurrentInventory'] = str(CI)
                        number.append(i)
                        break
            else:
                print('The items {} do not exist in the warehouse' . format(i['ItemNumber']))
                   
        for n in number:
            if n in self.Returnsupplier:
                self.Returnsupplier.remove(n)
        else:
            pass
        print('='*100) 
        print('left in inventory: \n', self.InventoryInfo)
        return self.InventoryInfo, self.Returnsupplier
    
    def show_reasoninventory(self):
        reason=[]
        reasontable = dict()
        for i in self.Returnwarehouse:
            reason.append(i['backreason'])
        for i in reason:
            if i in reasontable:
                reasontable[i] += 1
            else:
                reasontable[i] = 1
        print('The reason returning to inventory:\n', reasontable)
        
    def show_reasonsupplier(self):
        reason=[]
        reasontable = dict()
        for i in self.Returnsupplier:
            reason.append(i['backreason'])
        for i in reason:
            if i in reasontable:
                reasontable[i] += 1
            else:
                reasontable[i] = 1
        print('The reason returning to inventory:\n', reasontable)
    
    
   

            
    
if __name__ == '__main__':
    s=returnin()
    s.return_cangku()

    








