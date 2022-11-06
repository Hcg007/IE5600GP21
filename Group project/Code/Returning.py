"""
Created on Fri Nov  4 18:53:57 2022
@author: ql
"""

class Returnin():
    def __init__(self,info):
        self.InventoryInfo = info.InventoryInfo
        self.Returnsupplierkeys = info.Returnsupplierkeys
        self.ReturnwarehouseKeys = info.ReturnwarehouseKeys
        self.Returnwarehouse = info.Returnwarehouse
        self.Returnsupplier = info.Returnsupplier
        
  
    def return_auditinventory(self):
        
        if 'Returningnumbers' in self.ReturnwarehouseKeys:
            pass
        else:
            print('unvalid returning order')
            return
        for i in self.Returnwarehouse:
            for j in self.InventoryInfo:
                if i['ItemNumber'] == j['ItemNumber']:
                    break
            else:
                print('unvalid returning order')
                return
        else:
            print('Approved order')
                
    def return_auditsupplier(self):

        if 'Returningnumbers' in self.Returnsupplierkeys:
            pass
        else:
            print('unvalid returning order')
            return
        for i in self.Returnsupplier:
            for j in self.InventoryInfo:
                if i['ItemNumber'] == j['ItemNumber']:
                    break
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
                    Max = 300
                    CI1 = int(i['CurrentInventory'])
                    CI2 = int(j['Returningnumbers'])
                    CI = CI1 + CI2
                    if CI > Max:
                        print('The maximum storage CurrentInventorycapacity of {} is exceeded' . format(i['ItemNumber']))
                        i['CurrentInventory'] = str(CI)
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

        return self.Returnwarehouse, self.InventoryInfo
        
     
    def return_shangjia(self):
        number=[]
        for i in self.Returnsupplier:
            for j in self.InventoryInfo:
                if i['ItemNumber']==j['ItemNumber']:
                    CI1 = int(j['CurrentInventory'])
                    CI2 = int(i['Returningnumbers'])
                    if CI2 > CI1:
                        print('The number of {} returns exceeds the inventory' . format(i['ItemNumber']))
                        i['CurrentInventory'] = str(0)
                        continue
                    else:
                        CI = CI1 - CI2
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
        
    
    def num_data(self):
          print('***********************Returning management system***********************')
          print('1.Return goods back to inventory')
          print('2.Return goods to supplier')
          print('3.Show return inventory reason')
          print('4.Show return supplier reason')
          print('5.Log out of the system')
          return input('Please input the function number：')
      
        
    def run(self):
        while (True):

            num_data = self.num_data()

            if num_data == '1':
                self.return_auditinventory()
                self.return_cangku()

            elif num_data == '2':
                self.return_auditsupplier()
                self.return_shangjia()

            elif num_data == '3':
                self.show_reasoninventory()

            elif num_data == '4':
                self.show_reasonsupplier()
           
            elif num_data == '5':
                quit = input('Do you want to log out? YES or NO？')
                if quit == 'YES':
                    break
                elif quit == 'NO':
                    self.num_data()
                else:
                    print('error message')
            else:
                pass

    


    

    








