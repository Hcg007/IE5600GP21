# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


class PurchasingOrder:
    
    import datetime
    status ='Create'
    purchase_date = datetime.datetime.now().strftime('%Y/%m/%d')

    
    def __init__(self):
        self.item_num=''
        self.quantity=''
        self.item_lst=self.ReadCsv('../Forms/Template/itemlist.csv')
        
        
        
    def CreateOrder(self,order_num,NewOrder):
        
        self.item_num=NewOrder[0]
        self.quantity=str(NewOrder[1])
        
        
        
        order_num=str(order_num)
        
        for item in self.item_lst:
            if self.item_num ==item['ItemNumber']:
                item_name=item['ItemName']
                specification=item['Specification']
                unit=item['Unit']
                unit_price=item['UnitPrice']
                total_price=str(int(unit_price)*int(self.quantity))
                supplier_num=item['SupplierNumber']
                supplier=item['SupplierName']
        
        
        
        self.new_order={'OrderNumber':order_num,'ItemNumber':self.item_num,'ItemName':item_name,
                   'Specification':specification,'Quantity':self.quantity,'Unit':unit,
                   'UnitPrice':unit_price,'TotalPrice':total_price,
                   'SupplierNumber':supplier_num,'Supplier':supplier,
                   'PurchaseDate':self.purchase_date,'Status':self.status
                   }

        return self.new_order

    
 
    def ApproveOrder(self,new_purchase_lst):
        
        purchase_lst=self.ReadCsv('../Forms/Template/PurchaseForm.csv')
        print('New Order=',new_purchase_lst)
        approve=input("approve the order(Yes/No):")
        if approve=='Yes':
            for new_order in new_purchase_lst:
                for order in purchase_lst:
                    if new_order['ItemName']==order['ItemName'] and new_order['Specification']==order['Specification'] and new_order['PurchaseDate']==order['PurchaseDate']:
                        order['Status']='Approve'
            print('Approve Successfully!')
                        
            self.SaveCsv(purchase_lst,'../Forms/Template/PurchaseForm.csv')
    
        
                                            
        
    def QueryOrder(self):
        purchase_lst=self.ReadCsv('../Forms/Template/PurchaseForm.csv')
        inbound=self.ReadCsv('../Forms/Template/PurchaseForm.csv')
        for order in purchase_lst:
            for item in inbound:
                if order['OrderNumber']==item['ID']:
                    order['Status']='Finish'
        self.SaveCsv(purchase_lst,'../Forms/Template/PurchaseForm.csv')                
        
        queryorder=input('Enter the order number:')
        if int(queryorder) > len(purchase_lst):
            print('Order does not exist!')
        else:    
            for order in purchase_lst:
                if queryorder != order['OrderNumber']:
                    continue
                else:
                    print(order)
        
            
        
        
    def EditOrder(self):
        purchase_lst=self.ReadCsv('../Forms/Template/PurchaseForm.csv')
        editorder=input('Enter the order number:')
        if int(editorder) > len(purchase_lst):
            print('Order does not exist!')
        else:
            for order in purchase_lst:
                if editorder == order['OrderNumber']:
                    print(order)
                    
                    edit=input('Which part to edit?')
                    for part in order.keys():
                        if edit == part:
                            order[part]=input('Edit to:')
                            print('Edit successfully!')
                        
            
        self.SaveCsv(purchase_lst,'../Forms/Template/PurchaseForm.csv')
    
    
    
                
    def CancelOrder(self):
        purchase_lst=self.ReadCsv('../Forms/Template/PurchaseForm.csv')
        cancelorder=input('Enter the order number:')
        for order in purchase_lst:
            if cancelorder == order['OrderNumber']:
                print(order)
                
                cancel=input('Comfirm your cancellation(Yes/No):')
                if cancel =='Yes':
                    order['Status']='Cancel'
                    print('Cancel is done!')
                    
        self.SaveCsv(purchase_lst,'../Forms/Template/PurchaseForm.csv')
                    
                    
                    
    def ReadCsv(self,csvpath):
        with open(csvpath, 'r') as f:
            infoList = []
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
    
    
    
    
    def SaveCsv(self,Data, csvpath):
            with open(csvpath, 'w') as f:
                keys = Data[0].keys()
                f.write(','.join(keys))
                f.write('\n')
                for i in Data:
                    f.write(','.join(i.values()))
                    f.write('\n')
                    
    
    
    def ReNumberAggregation(self,csvpath):

        try:
            csv = self.ReadCsv(csvpath)
            for i in range(1, len(csv)):
                if csv[i]["OrderNumber"] == "OrderNumber":
                    csv.remove(csv[i])
                else:
                    continue
            for i in range(len(csv)):
                csv[i]["OrderNumber"] = str(i + 1)
            self.SaveCsv(csv, csvpath)
        except:
            print("{}faliure".format(csvpath))
        
    
    def PurchaseFunc(self, info, op):
            
        print('*'*70)
        print('Welcome to Purchasing Order Management Module!')
        
        purchase_lst=info.PurchaseInfo
        new_purchase_lst=[]
        order_num=1
        
            
        order_dic=op.replenish_num
                    
        for order in order_dic.items():
            NewOrder=order
            new_purchase=self.CreateOrder(order_num,NewOrder)
            order_num += 1
            
            new_purchase_lst.append(new_purchase)
            
        for new_purchase in new_purchase_lst:
            purchase_lst.append(new_purchase)
              
        self.SaveCsv(purchase_lst,'../Forms/Template/PurchaseForm.csv')
        self.ReNumberAggregation('../Forms/Template/PurchaseForm.csv')
            
        
        while True:
            print('*'*70)
            operation=input('Please select the function:\n\tA = Approve order\n\tB = Query order\n\tC = Edit order\n\tD = Cancel order\n\tE = Return to desktop\n\n\tChoice=')
            if operation == 'A':
                self.ApproveOrder(new_purchase_lst)
                
            elif operation == 'B':
                self.QueryOrder()
                           
            elif operation == 'C':
                self.EditOrder()
                
            elif operation == 'D':
                self.CancelOrder()
            
            elif operation == 'E':
    
                break
            
            else:
                print('Invalid Select!')
    
        info.PurchaseInfo=purchase_lst
        print('Exit successfully!')
            
            

    

       

            
        
        

   
   
   
   

                

    
    
            
    

                    
        
        
                
                
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    