# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 23:23:53 2022

@author: Loris
"""
from OrderProcessing import OrderProcessing
from BaseInformationSystem import BaseInformationSystem
from purchasing_code import PurchasingOrder
from inventory_management import InventoryManagement
from supplier_license import SupplierSystem
from Returning import returnin

if __name__ == '__main__':
    info = BaseInformationSystem()
    
    op = OrderProcessing(info) 
    op.Simulation(info)
    
    purchase_fuc=PurchasingOrder()
    purchase_fuc.PurchaseFunc(info, op)
    
    inventory = InventoryManagement()
    inventory.purchase_inbound(info)
    inventory.inbound_inventory(info)
    inventory.outbound_inventory(info)
    inventory.order_outbound(info)

    supplier_check=SupplierSystem()
    supplier_check.supplier_function()
    returning=returnin()
    returning.run()
    
    