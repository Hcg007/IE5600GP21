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
        
    #This function is used to convert the automatic replenish system output to formal purchase list
        
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
        
    #This function is used to approve the newly created orders,
    #we assume that once the order been approved, it will be sent to supplier
        
        purchase_lst=self.ReadCsv('../Forms/Template/PurchaseForm.csv')
        new_num=len(new_purchase_lst)
        print('{} new orders have been created.'.format(new_num))
        approve=input("approve the order(Yes/No):")
        if approve=='Yes':
            for new_order in new_purchase_lst:
                for order in purchase_lst:
                    if new_order['ItemName']==order['ItemName'] and new_order['Specification']==order['Specification'] and new_order['PurchaseDate']==order['PurchaseDate']:
                        order['Status']='Approve'
            print('Approve Successfully!')
                        
            self.SaveCsv(purchase_lst,'../Forms/Template/PurchaseForm.csv')
            
                                            
        
    def QueryOrder(self):
        
    #This function is used to upload the status of purchasing order and query the order, 
    #when calling this function, the system will check the inbound list and upload the order status,
    #we assume that the order is finished when the warehouse checked and inbound the items
        
        purchase_lst=self.ReadCsv('../Forms/Template/PurchaseForm.csv')
        inbound=self.ReadCsv('../Forms/Template/PurchaseForm.csv')
        m=0
        for order in purchase_lst:
            for item in inbound:
                if order['OrderNumber']==item['ID']:
                    order['Status']='Finish'
                    m+=1
        self.SaveCsv(purchase_lst,'../Forms/Template/PurchaseForm.csv')
        print('Update successfully! {} orders have been finished.'.format(m))
        
        queryorder=input('Enter the order number to query:')
        if int(queryorder) > len(purchase_lst):
            print('Order does not exist!')
        else:    
            for order in purchase_lst:
                if queryorder != order['OrderNumber']:
                    continue
                else:
                    print(order)
        
         
        
    def EditOrder(self):
        
    #This function is used to edit the order information, such as quantity 
        
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
        
    #If the goods cannot arrive the warehouse on time, the order will be canceled,
    #and the automatic replenish system will generate a new order list next time
        
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
        # renumber the list
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
            print("{} fail to renumber".format(csvpath))
        

    def PurchaseFunc(self, info, op):
        
        #This module provides functions to deal with purchasing orders, when administrator enter this module, 
        #this system will automatically check the new orders that have been created by the automatic replenish sysytem,
        #and add the new orders to the csv file
        
        print('***********************Purchasing Order management system***********************')
                    
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
            print('='*60)
            print('1.Approve Order')
            print('2.Update and Query Order')
            print('3.Edit Order')
            print('4.Cancel Order')
            print('5.Log out of the system')
            operation = input('Please input the function number：')
            
            if operation == '1':
                self.ApproveOrder(new_purchase_lst)
                
            elif operation == '2':
                self.QueryOrder()
                           
            elif operation == '3':
                self.EditOrder()
                
            elif operation == '4':
                self.CancelOrder()
            
            elif operation == '5':
    
                break
            
            else:
                print('Invalid Select!')
    
        info.PurchaseInfo=purchase_lst
        print('Exit successfully!')
            
            

    

       

            
        
        

   
   
   
   

                

    
    
            
    

                    
        
        
                
                
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
