class BaseInformationSystem():
    def __init__(self):
        # 原始信息读取
        self.InventoryInfo = self.ReadCsv("../Forms/Template/InventoryForm.csv")
        self.SupplierInfo = self.ReadCsv("../Forms/Template/SupplierForm.csv")
        self.InboundInfo = self.ReadCsv("../Forms/Template/InboundForm.csv")
        self.OutboundInfo = self.ReadCsv("../Forms/Template/OutboundForm.csv")
        self.PurchaseInfo = self.ReadCsv("../Forms/Template/PurchaseForm.csv")
        # 只提取索引
        self.InventoryInfoKeys = self.ReadCsvKeys("../Forms/Template/InventoryForm.csv")
        self.SupplierInfoKeys = self.ReadCsvKeys("../Forms/Template/SupplierForm.csv")
        self.InboundInfoKeys = self.ReadCsvKeys("../Forms/Template/InboundForm.csv")
        self.OutboundInfoKeys = self.ReadCsvKeys("../Forms/Template/OutboundForm.csv")
        self.PurchaseInfoKeys = self.ReadCsvKeys("../Forms/Template/PurchaseForm.csv")

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

    def search(self, query):
        pass

    def get(self, id):
        pass

    def add(self, data):
        pass

    def update(self, id, data):
        print("update")
        pass

    def delete(self, id):
        print("delete")
        pass

    def get_all(self):
        pass


class Order():
    def __init__(self):
        self.OrderSaveRoot = "../Forms/Template/Orders/"
        self.OriginalOrderInfo = self.ReadCsv("../Forms/Template/InventoryForm.csv")
        self.SupermarketInfo = self.ReadCsv("../Forms/Template/SupermarketForm.csv")
        self.OrderInfo = []
        self.Order = {"ID": "", "SupermarketName": "", "SupermarketNumber": "", "ItemNumber": "", "ItemName": '', "Specification": "",
                      "OrderNumber": "", "OrderDate": "", "Contact": "", "ContactNumber": ""}
        self.OrderTime = None

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

    def GenerateOrder(self):
        import random
        import datetime
        total_id = random.randint(1, 100)
        suppermarket_id = random.randint(1, len(self.SupermarketInfo))
        self.Ordertime = datetime.datetime.now()
        self.Order["OrderDate"] = self.Ordertime.strftime('%Y-%m-%d')
        self.Order["SupermarketName"] = self.SupermarketInfo[suppermarket_id - 1]["SupermarketName"]
        self.Order["SupermarketNumber"] = self.SupermarketInfo[suppermarket_id - 1]["SupermarketNumber"]
        self.Order["ContactNumber"] = self.SupermarketInfo[suppermarket_id - 1]["ContactNumber"]
        self.Order["Contact"] = self.SupermarketInfo[suppermarket_id - 1]["Contact"]
        for i in range(1, total_id + 1):
            self.Order["ID"] = str(i)
            goodID = random.randint(1, len(self.OriginalOrderInfo))
            self.Order["ItemNumber"] = self.OriginalOrderInfo[goodID - 1]["ItemNumber"]
            self.Order["ItemName"] = self.OriginalOrderInfo[goodID - 1]["ItemName"]
            self.Order["Specification"] = self.OriginalOrderInfo[goodID - 1]["Specification"]
            #单个订单的货品数量不大于当前库存
            maxNum = int(self.OriginalOrderInfo[goodID - 1]["CurrentInventory"])
            self.Order["ItemNumber"] = str(random.randint(1, maxNum))

            self.OrderInfo.append(self.Order.copy())

    def ClearAllinRoot(self):
        import os
        for i in os.listdir(self.OrderSaveRoot):
            os.remove(self.OrderSaveRoot + i)

    def Delay(self, seconds):
        import time
        time.sleep(seconds)

    def ReadCsvKeys(self, csvpath):
        with open(csvpath, 'r') as f:
            keys = f.readline().split(',')
            for i in range(len(keys)):
                keys[i] = keys[i].replace(' ', '')
                keys[i] = keys[i].replace('\n', '')
        return keys

    def OrderGenerate(self, OrderInfo):
        OrderInfo = dict(zip(self.Order, OrderInfo))
        return OrderInfo

    def OrderSave(self):
        import datetime
        # save
        ordertime = "{}{}{}{}{}{}".format(self.Ordertime.year, self.Ordertime.month, self.Ordertime.day,
                                          self.Ordertime.hour, self.Ordertime.minute, self.Ordertime.second)
        suffix = "Order"+str(ordertime) + ".csv"
        path = self.OrderSaveRoot + suffix
        self.SaveCsv(self.OrderInfo, path)

    def SaveCsv(self, Data, csvpath):
        with open(csvpath, 'w') as f:
            keys = Data[0].keys()
            f.write(','.join(keys))
            f.write('\n')
            for i in Data:
                f.write(','.join(i.values()))
                f.write('\n')


if __name__ == '__main__':
    info=BaseInformationSystem()
    order = Order()
    print("""ClearAllinRoot()会清空根目录所有文件，请新建文件夹以保存订单""")
    print("Press 1 to generate order")
    print(order.Order["SupermarketName"])
    choice = input()
    if choice == "1":

        order.ClearAllinRoot()
        for i in range(5):
            order.GenerateOrder()
            print("Order {} generated".format(i + 1))
            order.Delay(2)#重名会覆盖
            order.OrderSave()
            print("Order {} saved".format(i + 1))
    else:
        print("Invalid input")
