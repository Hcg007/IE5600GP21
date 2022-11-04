# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 22:48:33 2022

@author: Loris
"""
import datetime
from BaseInformationSystem import Order
     
class OrderProcessing:
    
    def __init__(self):
        self.rush_order_num = 1
        self.replenish_num = {}
        self.orders = {} 
        self.orders_tomorrow = {}
        self.initialize()
        
    def initialize(self):
        order = Order()
        order.ClearAllinRoot()
        for i in range(3):         
            order.GenerateOrderbyDays(3)
            order.Delay(1)
            
        order.AggregatedOrderinDict()           
        keys = []
        for i in order.OrdersInfo:
            keys.append(i)
        order_1 = order.OrdersInfo[keys[1]]
        order_2 = order.OrdersInfo[keys[2]]
        for i in order_1:
            if i['OrderNumber'] in self.orders:
                self.orders[i['OrderNumber']]['Product'].update({int(i['ItemNumber'][4:6]): int(i['OrderAmount'])})
            else:
                delivery_dt = i['EstDeliverDate']
                delivery_time = datetime.datetime(day = int(delivery_dt[8:10]), month = int(delivery_dt[5:7]), year = int(delivery_dt[:4]), hour = int(delivery_dt[10:12]))                 
                self.orders.update({i['OrderNumber']:{'Branch_num': i['SupermarketNumber'], 'Delivery_dt': delivery_time, 'Product': {int(i['ItemNumber'][4:6]): int(i['OrderAmount'])}, 'State': 'Pending', 'Type': 'normal'}})
        for i in order_2:
            if i['OrderNumber'] in self.orders_tomorrow:
                self.orders_tomorrow[i['OrderNumber']]['Product'].update({int(i['ItemNumber'][4:6]): int(i['OrderAmount'])})
            else:
                delivery_dt = i['EstDeliverDate']
                delivery_time = datetime.datetime(day = int(delivery_dt[8:10]), month = int(delivery_dt[5:7]), year = int(delivery_dt[:4]), hour = int(delivery_dt[10:12]))                 
                self.orders_tomorrow.update({i['OrderNumber']:{'Branch_num': i['SupermarketNumber'], 'Delivery_dt': delivery_time, 'Product': {int(i['ItemNumber'][4:6]): int(i['OrderAmount'])}, 'State': 'Pending', 'Type': 'normal'}})
             
    def RushOrder(self, warehouse):
        input_validation = True
        product_info = {}
        bn = input('If you need place a rush order, please enter your branch number: ')
        delivery_dt = input('Enter your preferred delivery date and time (dd/mm/yy xx): ') 
        delivery_dt = datetime.datetime(day = int(delivery_dt[:2]), month = int(delivery_dt[3:5]), year = int('20'+delivery_dt[6:8]), hour = int(delivery_dt[9:11]))       
        while int(delivery_dt.hour) < 9 or int(delivery_dt.hour) > 17:
            print('Not Avaiable (Outside Warehouse Operating Hours)')
            delivery_dt = input('Please enter your preferred delivery date and time again (dd/mm/yy xx): ') 
            delivery_dt = datetime.datetime(day = int(delivery_dt[:2]), month = int(delivery_dt[3:5]), year = int('20'+delivery_dt[6:8]), hour = int(delivery_dt[9:11]))       
        while input_validation:          
            c = input('Enter the category number: ')
            c = int(c[4:6])
            if c not in range(100):  
                print('Invalid category, please input again!')
                continue                         
            else:
                while input_validation:
                    num = int(input('Enter the needed quantity: '))
                    if num > int(warehouse.InventoryInfo[c]['CurrentInventory']):   
                        cancel = input('Lack of stock! Only {} are left. Do you want to cancel this order? (Y/N): '.format(warehouse.InventoryInfo[c]['CurrentInventory']))
                        if cancel == 'Y':
                            input_validation = False
                        else:
                            continue
                    else:
                        product_info.update({c: num})
                        if_more = input('Do you need anything else? (Y/N): ')
                        if if_more == 'Y':
                            break
                        
                        else:                                            
                            self.orders.update({'R{}'.format(self.rush_order_num): {'Branch_num': bn, 'Delivery_dt': delivery_dt, 'Product': product_info, 'State': 'Pending', 'Type': 'rush'}})                                          
                            self.rush_order_num += 1
                            print('Your order is placed successfully!')
                            input_validation = False
                            
                  
    def _SortOrder(self):
        self.sorted_orders = {}
        for i in range(9, 18, 1):
            self.sorted_orders.update({i:{}})
            for j in self.orders.values():
                if int(j['Delivery_dt'].hour) == i:
                    if j['Branch_num'] not in self.sorted_orders[i]:
                        self.sorted_orders[i].update({j['Branch_num']: j['Product']}) 
                    else:
                        for k1 in j['Product']:
                            for k2 in self.sorted_orders[i][j['Branch_num']]:
                                if k1 == k2:
                                    self.sorted_orders[i][j['Branch_num']][k2] += j['Product'][k1]
            
    def ProcessOrder(self, warehouse):
        confirm = input("Do you want to process today's orders? (Y/N): ")
        if confirm == 'Y':
            for i in self.orders:
                for j in self.orders[i]['Product']:
                    warehouse.InventoryInfo[j]['CurrentInventory'] = int(warehouse.InventoryInfo[j]['CurrentInventory']) - self.orders[i]['Product'][j]
                self.orders[i]['State'] = 'Processed'
            print('All the orders have been delivered successfully.')
        
    def ShowSchedule(self):
        self._SortOrder()
        hour = int(input('Please input the specific time of the delivery schedule (XX): '))
        if self.sorted_orders[hour] == {}:
            print('There is no delivery task at this hour.')
        else:
            print("\nThe delivery schedule at {} o'clock is shown below:".format(hour))
            for i in self.sorted_orders[hour]:
                print('\nSupermarket number: {}'.format(i))
                print('\nItem number          Quantity')
                for j in self.sorted_orders[hour][i]:
                    print('{}               {}'.format('F000' + str(j).zfill(2), self.sorted_orders[hour][i][j]))
            print('Please deliver the corresponding products in time!')  
     
    
    def GeneratePurchasingOrder(self, warehouse):
        simu_inventory = warehouse.InventoryInfo             
        for i in self.orders_tomorrow:
            for j in self.orders_tomorrow[i]['Product']:
                simu_inventory[j]['CurrentInventory'] = int(simu_inventory[j]['CurrentInventory']) - self.orders_tomorrow[i]['Product'][j]               
        for i in simu_inventory:    
            if int(i['CurrentInventory']) <= int(i['SafetyInventory']):
                self.replenish_num.update({i['ItemNumber']: int(i['MaxInventory']) - int(warehouse.InventoryInfo[int(i['ID'])-1]['CurrentInventory'])})
                    
        return self.replenish_num
        

                  


  
 
                
        
