# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 10:58:47 2022

@author: VULCAN
"""
import datetime
class SupplierSystem():
    
    def __init__(self):    
        csv="G:/桌面/IE5600 team project/SupplierForm.csv"
        K2=self.FormatList(csv)
        self.K3=self.CsvList2Dict(K2)
    def FormatList(self,csvpath):
        with open(csvpath, 'r') as f:
            List = []
            for i in f:
                List.append(i)
        for i in range(len(List)):
            List[i] = List[i].split(',')
        for j in List:
            for i in range(len(j)):
                j[i] = j[i].replace(' ', '')
                j[i] = j[i].replace('\n', '')
        return List
    
    def CsvList2Dict(self,List):
        keys = List[0]
        values = []
        for j in range(len(List[0])):
            value_list = []
            for i in range(1, len(List)):
                value_list.append(List[i][j])
            values.append(value_list)
        Dict = dict(zip(keys, values))

        return Dict
    
    def Addsupplier(self):
       
       ID=input('Please input the ID: ')
       t=True
       while t==True:
           for k in self.K3['ID']:
               if k==ID:
                   print('Already exist:')
                   ID=input('Reenter:')
                   t=True
               else:
                   t=False
           
       self.K3['ID'].append(ID)
       SupplierNumber=input('Please input the Supplier Number: ')
       self.K3['SupplierNumber'].append(SupplierNumber)
       Address=input('Please input the Address: ')
       self.K3['Address'].append(Address)
       Telphone=input('Please input the Telphone: ')
       y=True
       while y==True:
           try:
               if len(Telphone)!=8:
                  raise ValueError
               else:
                   y=False
           except ValueError:
               print('wrong value')
               Telphone=input('enter again:')
       
       self.K3['Telphone'].append(Telphone)
       EligibilityStartDate=input('Please input the Eligibility Start Date:(dd/mm/yyyy) ')
       a=True
       while a==True:
        try: 
         hour1=datetime.datetime.strptime(EligibilityStartDate,'%d/%m/%Y')
         a=False
        except ValueError:
            print('input again')
            EligibilityStartDate=input('Eligibility Start Date:')
       
       self.K3['EligibilityStartDate'].append(EligibilityStartDate)
       EligibilityExpiryDate=input('Please input the Eligibility Expiry Date:(dd/mm/yyyy) ')
       b=True
       while b==True:
        try: 
         hour2=datetime.datetime.strptime(EligibilityExpiryDate,'%d/%m/%Y')
         b=False
        except ValueError:
            print('input again')
            EligibilityExpiryDate=input('Eligibility Expiry Date:')
       
       self.K3['EligibilityExpiryDate'].append(EligibilityExpiryDate)
       return self.K3
        
    def ShowInfor(self):
       
       print('Supplier Information')
       print(self.K3)
       return self.K3
    def Updatesupplier(self):
        ID=input('Please input the ID: ')
        
        a=0
        for i in range(len(self.K3['ID'])):
            if self.K3['ID'][i]==ID:
                print('exist')
                self.K3['ID'][i]=input('new ID:')
                self.K3['SupplierNumber'][i]=input('new Supplier Number:')
                self.K3['Address'][i]=input('new Address:')  
                self.K3['Telphone'][i]=input('new Telphone (8 digits):')
                u=True
                while u==True:
                    try:
                        if len(self.K3['Telphone'][i])!=8:
                           raise ValueError
                        else:
                            u=False
                    except ValueError:
                        print('wrong value')
                        self.K3['Telphone'][i]=input('enter again:')
                self.K3['EligibilityStartDate'][i]=input('new Eligibility Start Date:(dd/mm/yyyy):')
                a=True
                while a==True:
                 try: 
                  hour1=datetime.datetime.strptime(self.K3['EligibilityStartDate'][i],'%d/%m/%Y')
                  a=False
                 except ValueError:
                     print('input again')
                     self.K3['EligibilityStartDate'][i]=input('new Eligibility Start Date:(dd/mm/yyyy):')
                
                
                self.K3['EligibilityExpiryDate'][i]=input('new Eligibility Expiry Date:(dd/mm/yyyy):')
                b=True
                while b==True:
                 try: 
                  hour2=datetime.datetime.strptime(self.K3['EligibilityExpiryDate'][i],'%d/%m/%Y')
                  b=False
                 except ValueError:
                     print('input again')
                     self.K3['EligibilityExpiryDate'][i]=input('new Eligibility Expiry Date:(dd/mm/yyyy):')
                
                a=a+1
        if a==0:
            print('no existence')
            return self.K3
    def  Deletesupplier(self):   
          ID=input('Please input the ID: ')
          a=0
          for i in range(len(self.K3['ID'])):
              if self.K3['ID'][i]==ID:
                  print('exist')
                  self.K3['ID'].pop(i)
                  self.K3['SupplierNumber'].pop(i)
                  self.K3['Address'].pop(i)
                  self.K3['Telphone'].pop(i)  
                  self.K3['EligibilityStartDate'].pop(i) 
                  self.K3['EligibilityExpiryDate'].pop(i)
            
                  a=a+1
          if a==0:
              print('no existence')
              return self.K3
    def Checkexpiretime(self):
           for i in range(len(self.K3['ID'])):
               if self.K3['EligibilityExpiryDate'][i] =='':
                   print(self.K3['ID'][i],'no expire time')
               else:
                   hour=datetime.datetime.strptime(self.K3['EligibilityExpiryDate'][i],'%d/%m/%Y')
                   now=datetime.datetime.now()
                   if hour<=now:
                      print(self.K3['ID'][i],'expired')
         
if __name__ == '__main__':         
    a=SupplierSystem()
    while True:
        print("\n\n\n-------------------------")
        print("#  System #")
        print("1. Show Information")
        print("2. Add supplier")
        print("3. Update supplier")
        print("4. Delete supplier")
        print("5. Check expire time")
        print("6. Drop out")
        print("-------------------------")
        selectFun=int(input("Please choose the function："))
        if selectFun==1:
           a.ShowInfor()
        elif selectFun==2:
           a.Addsupplier()
        elif selectFun==3:
           a.Updatesupplier()
        elif selectFun==4:
           a.Deletesupplier()
        elif selectFun==5:
           a.Checkexpiretime()
        
        else:
            
            break
    

    
