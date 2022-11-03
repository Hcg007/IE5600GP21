class BaseInformationSystem():
    def __init__(self):
        # 原始信息读取
        self.SaveRoot = "../Forms/Template/"
        self.InventoryInfo = self.ReadCsv("../Forms/Template/InventoryForm.csv")
        self.SupplierInfo = self.ReadCsv("../Forms/Template/SupplierForm.csv")
        self.InboundInfo = self.ReadCsv("../Forms/Template/InboundForm.csv")
        self.OutboundInfo = self.ReadCsv("../Forms/Template/OutboundForm.csv")
        self.PurchaseInfo = self.ReadCsv("../Forms/Template/PurchaseForm.csv")
        self.OrderAggregationInfo = None  # 当日订单汇总
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

    def AggregatedOrder(self):
        # 遍历根目录下文件夹
        import os
        OrderSaveRoot = self.SaveRoot + "Orders/"
        Orderlist = []
        Aggregationlist = []
        for root, dirs, files in os.walk(OrderSaveRoot, topdown=True):
            for file in files:
                path = os.path.join(root, file)
                # 将path的\替换为/
                path = path.replace('\\', '/')
                Orderlist.append(path)
        #print(Orderlist)
        for i in range(len(Orderlist)):
            csv = self.ReadCsv(Orderlist[i])
            Aggregationlist.append(OrderSaveRoot + Orderlist[i][25:35] + ".csv")

            with open(Aggregationlist[i], 'a') as f:
                keys = csv[0].keys()
                f.write(','.join(keys))
                f.write('\n')
                for j in csv:
                    f.write(','.join(j.values()))
                    f.write('\n')

        # 删除重复项
        Aggregationlist = list(set(Aggregationlist))
        # 将产生的汇总表重新编号
        for i in Aggregationlist:
            self.ReAggregation(i)#

    def ReAggregation(self, csvpath):  # 汇总表重新编号
        try:
            csv = self.ReadCsv(csvpath)
            for i in range(1,len(csv)):
                if csv[i]["OrderNumber"]=="OrderNumber":
                    csv[i]["OrderNumber"] = str(0)
                else:
                    continue
            for i in range(len(csv)):
                csv[i]["ID"] = str(i + 1)
            for i in csv:
                if i["OrderNumber"] == "0":
                    csv.remove(i)
            self.SaveCsv(csv, csvpath)
        except:
            print("{}失败".format(csvpath))

    def search(self, query):
        pass

    def get(self, id):
        pass

    def add(self):
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
        self.OrdersInfo={}
        self.Order = {"ID": "", "OrderNumber": "", "SupermarketName": "", "SupermarketNumber": "", "ItemNumber": "",
                      "ItemName": '', "Specification": "",
                      "OrderAmount": "", "OrderDate": "","EstDeliverDate":"", "Contact": "", "ContactNumber": ""}
        self.Ordertime = None
        self.TodayOrder = None

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
        # 生成单个订单
        import random
        import datetime
        self.OrderInfo = []
        total_id = random.randint(1, 100)
        suppermarket_id = random.randint(1, len(self.SupermarketInfo))
        self.Ordertime = datetime.datetime.now()
        self.Ordertime = self.Ordertime.replace(minute=0, second=0)
        self.Order["OrderDate"] = self.Ordertime.strftime('%Y-%m-%d')

        self.Order["EstDeliverDate"] = (self.Ordertime + datetime.timedelta(days=1,hours=random.randint(9,17))).strftime('%Y-%m-%d %H:%M:%S')
        #第字符10和11中间加空格
        self.Order["EstDeliverDate"] = self.Order["EstDeliverDate"][:10] + " " + self.Order["EstDeliverDate"][10:]
        self.Order["OrderNumber"] = self.Ordertime.strftime('%Y%m%d%H%M%S')
        self.Order["OrderNumber"] = str(self.Order["OrderNumber"])
        self.Order["SupermarketName"] = self.SupermarketInfo[suppermarket_id - 1]["SupermarketName"]
        self.Order["SupermarketNumber"] = self.SupermarketInfo[suppermarket_id - 1]["SupermarketNumber"]
        self.Order["ContactNumber"] = self.SupermarketInfo[suppermarket_id - 1]["ContactNumber"]
        self.Order["Contact"] = self.SupermarketInfo[suppermarket_id - 1]["Contact"]
        goodID_list = []
        for i in range(1, total_id + 1):
            self.Order["ID"] = str(i)
            goodID = random.randint(1, len(self.OriginalOrderInfo))
            # 检查是否重复
            while goodID in goodID_list:
                goodID = random.randint(1, len(self.OriginalOrderInfo))
            goodID_list.append(goodID)
            self.Order["ItemNumber"] = self.OriginalOrderInfo[goodID - 1]["ItemNumber"]
            self.Order["ItemName"] = self.OriginalOrderInfo[goodID - 1]["ItemName"]
            self.Order["Specification"] = self.OriginalOrderInfo[goodID - 1]["Specification"]
            # 单个订单的货品数量不大于当前库存
            maxNum = int(self.OriginalOrderInfo[goodID - 1]["CurrentInventory"])
            #均值30，方差为25的正态
            OrderAmount = max(int(random.normalvariate(30, 5)),maxNum)
            self.Order["OrderAmount"] = str(OrderAmount)
            self.OrderInfo.append(self.Order.copy())

        return self.OrderInfo

    def GenerateOrderbyDays(self,days):
        # 生成即日起days天的订单
        import datetime
        currentTime=datetime.datetime.now()
        for i in range(days):
            self.GenerateOrder()
            for j in range(len(self.OrderInfo)):
                self.Ordertime =currentTime + datetime.timedelta(days=i)
                self.OrderInfo[j]["OrderDate"]=self.Ordertime.strftime('%Y-%m-%d')
                self.OrderInfo[j]["OrderNumber"]=self.Ordertime.strftime('%Y%m%d%H%M%S')
            self.OrderSave()


    def AggregatedOrder(self):
        # 遍历根目录下文件夹,将同一天的订单合并
        import os
        #OrderSaveRoot = self.OrderSaveRoot
        Orderlist = []
        Aggregationlist = []
        for root, dirs, files in os.walk(self.OrderSaveRoot, topdown=True):
            for file in files:
                path = os.path.join(root, file)
                # 将path的\替换为/
                path = path.replace('\\', '/')
                Orderlist.append(path)
        # print(Orderlist)
        for i in range(len(Orderlist)):
            csv = self.ReadCsv(Orderlist[i])
            Aggregationlist.append(self.OrderSaveRoot + Orderlist[i][25:35] + ".csv")

            with open(Aggregationlist[i], 'a') as f:
                keys = csv[0].keys()
                f.write(','.join(keys))
                f.write('\n')
                for j in csv:
                    f.write(','.join(j.values()))
                    f.write('\n')

        # 删除重复项
        Aggregationlist = list(set(Aggregationlist))
        # 将产生的汇总表重新编号
        for i in Aggregationlist:
            self.ReNumberAggregation(i)

    def ReNumberAggregation(self, csvpath):
        # 汇总表重新编号
        try:
            csv = self.ReadCsv(csvpath)
            for i in range(1, len(csv)):
                if csv[i]["ID"] == "ID":
                    csv.remove(csv[i])
                else:
                    continue
            for i in range(len(csv)):
                csv[i]["ID"] = str(i + 1)
            self.SaveCsv(csv, csvpath)
        except:
            print("{}重新编号失败".format(csvpath))

    def AggregatedOrderinDict(self):
        # 生成每天的汇总订单
        # Orderdict的key是日期，value是订单列表，即{date1:[order1,order2],date2:[order3,order4]..}
        import os
        OrdersPath = []
        self.OrdersInfo={}
        for root, dirs, files in os.walk(self.OrderSaveRoot, topdown=True):
            for file in files:
                path = os.path.join(root, file)
                # 将path的\替换为/
                path = path.replace('\\', '/')
                OrdersPath.append(path)
        for i in range(len(OrdersPath)):
            csv=self.ReadCsv(OrdersPath[i])
            key=OrdersPath[i][25:35]
            #key一样的话，就合并
            if key in self.OrdersInfo.keys():
                self.OrdersInfo[key].extend(csv)
            else:
                self.OrdersInfo[key]=csv

        self.ReNumberOrderDict()

        return self.OrdersInfo

    def ReNumberOrderDict(self):
        # 重新编号
        for value in self.OrdersInfo.values():
            for i in range(len(value)):
                value[i]["ID"]=str(i+1)

    def ClearAllinRoot(self):
        import os
        import shutil
        # 删除文件夹下所有文件和文件夹
        if os.path.exists(self.OrderSaveRoot):
            shutil.rmtree(self.OrderSaveRoot)

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

    def OrderSave(self):
        ordertime = self.Ordertime.strftime('%Y%m%d%H%M%S')
        suffix = "Order" + str(ordertime) + ".csv"
        strdate = self.Ordertime.strftime('%Y-%m-%d')
        # 创建文件夹
        import os
        if not os.path.exists(self.OrderSaveRoot):
            os.mkdir(self.OrderSaveRoot)
        if not os.path.exists(self.OrderSaveRoot + strdate):
            os.mkdir(self.OrderSaveRoot + strdate)
        # 保存文件
        path = self.OrderSaveRoot + strdate + '/' + suffix
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
    info = BaseInformationSystem()
    generator = Order()
    generator.ClearAllinRoot()
    for i in range(3):
        #generator.GenerateOrder()
        generator.GenerateOrderbyDays(3)
        generator.Delay(1)

    generator.AggregatedOrderinDict()
    print("没报错?nb!")



