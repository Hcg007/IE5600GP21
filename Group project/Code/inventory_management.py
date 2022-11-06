import os

class InventoryManagement():

    def __init__(self):
        pass

    def ReadCsv(self, csvpath):
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

    def SaveCsv(self, Data, csvpath):
        with open(csvpath, 'w') as f:
            keys = Data[0].keys()
            f.write(','.join(keys))
            f.write('\n')
            for i in Data:
                f.write(','.join(i.values()))
                f.write('\n')

    def ReadCsvKeys(self, csvpath):
        with open(csvpath, 'r') as f:
            keys = f.readline().split(',')
            for i in range(len(keys)):
                keys[i] = keys[i].replace(' ', '')
                keys[i] = keys[i].replace('\n', '')
        return keys



    def order_outbound(self, info):

        # 将order导入inbound并重新编辑物品序号
        num = 0
        porter = {}
        for dict in info.InventoryInfo:
            num += 1
            porter['ID'] = str(num)
            porter['ItemNumber'] = dict['ItemNumber']
            porter['ItemName'] = dict['ItemName']
            porter['Specification'] = dict['Specification']
            porter['Number'] = dict['ItemNumber']
            info.OutboundInfo.append(porter)



    def inbound_inventory(self, info):
        print('*'*20+'Inventory management module'+'*'*20+'\n')
        print('='*60)
        print('Warehouse staff operation:\n')
        print('Warehouse fills according to purchase list')
        for i in self.InboundInfo:
            for j in self.InventoryInfo:
                if i['ItemNumber'] == j['ItemNumber']:
                    j['CurrentInventory'] = str(int(j['CurrentInventory']) + 1)

                    
                    
    def outbound_inventory(self, info):
        print('='*60)
        print('Warehouse staff operation:\n')
        print('Goods leave from warehouse according to orders')
        print('='*60+'\n')
        print('*'*67)
        for i in self.OutboundInfo:
            for j in self.InventoryInfo:
                if i['ItemNumber'] == j['ItemNumber']:
                    j['CurrentInventory'] = str(int(j['CurrentInventory']) - 1)

                    
                    
    def purchase_inbound(self, info):
        num = 0
        porter = {}
        for dict in info.PurchaseInfo:
            num += 1
            porter['ID'] = str(num)
            porter['ItemNumber'] = dict['ItemNumber']
            porter['ItemName'] = dict['ItemName']
            porter['Specification'] = dict['Specification']
            porter['Quantity'] = dict['ItemNumber']
            porter['Unit'] = dict['Unit']
            porter['UnitPrice'] = dict['UnitPrice']
            porter['TotalPrice'] =dict['TotalPrice']
            info.InboundInfo.append(porter)






