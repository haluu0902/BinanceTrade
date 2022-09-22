
#from tkinter import Frame, Label, StringVar, Entry, Button, Canvas, Scrollbar, RAISED
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from src.APIController import Controller
from src.SendMessage import SendMessageTelegram
from threading import Thread
from time import sleep
from datetime import datetime
import sys, os, json

class Run():
    #bep20, polygon, avax, fantom, eth
    def __init__(self, frame):
        self.parent = frame
        self.status = False
        self.Run()
        self.parent.mainloop()
    def Run(self):
        self.parent.title("Binance Tool Trade")
        self.parent.wm_iconbitmap('./images/icon.ico')
        self.parent.resizable(0, 0)
        self.parent.call('tk', 'scaling', 1.5)
        self.frame1 = Frame(self.parent, relief=RAISED, borderwidth=1)
        self.frame1.grid(row=0, column=0, sticky="nsew")

        self.inputFolderLabel = Label(self.frame1, text="Import API:", anchor='w', width=20)
        self.inputFolderLabel.grid(row=0, column=0, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.folderPath = StringVar(value='')
        self.inputFolderPath= Entry(self.frame1, width=50,textvariable=self.folderPath)
        self.inputFolderPath.grid(row=0, column=2, columnspan=4, padx = 5, pady = 5, sticky="nsew")
        self.browseButton = Button(self.frame1, text="Import Address", command=self.SetAccount)
        self.browseButton.grid(row=0, column=6, padx = 5, pady = 5, sticky="nsew")

        self.frame2 = Frame(self.parent, relief=RAISED, borderwidth=1)
        self.frame2.grid(row=1, column=0, sticky="nsew")

        self.pairsLabel = Label(self.frame2, text="Pair:", anchor='w', width=10)
        self.pairsLabel.grid(row=0, column=0, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.optionsPair =[]
        self.clickedOne = StringVar()
        self.clickedOne.set("")
        self.dropMenuOne = ttk.Combobox(self.frame2, textvariable=self.clickedOne, values=self.optionsPair, width=20)
        self.dropMenuOne.grid(row=0, column=2, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.dropMenuOne.bind('<KeyRelease>', self.FindBox)

        self.amountLabel = Label(self.frame2, text="Select Amount:", anchor='w', width=20)
        self.amountLabel.grid(row=0, column=4, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.amount = StringVar(value="10")
        self.inputAmount= Entry(self.frame2,textvariable=self.amount, width=20)
        self.inputAmount.grid(row=0, column=6, columnspan=2, padx = 5, pady = 5, sticky="nsew")

        self.times = ['1m', '3m', '5m','15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
        self.buyPriceLabel = Label(self.frame2, text="Interval:", anchor='w', width=10)
        self.buyPriceLabel.grid(row=1, column=0, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.optionsTimesOne = self.times
        self.clickedTimesOne = StringVar()
        self.clickedTimesOne.set("1h")
        self.dropMenuTimesOne = ttk.Combobox(self.frame2, textvariable=self.clickedTimesOne, values=self.optionsTimesOne, width=20)
        self.dropMenuTimesOne.grid(row=1, column=2, columnspan=2, padx = 5, pady = 5, sticky="nsew")

        self.typeRun = IntVar()
        self.typeRun.set(1)
        self.typeLabel = Label(self.frame2, text="Price Order:", anchor='w', width=20)
        self.typeLabel.grid(row=1, column=4, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.typeToSend = Radiobutton(self.frame2, text="Buy", variable=self.typeRun, value=1, anchor='w',command="")
        self.typeToSend.grid(row=1, column=6, padx = 5, pady = 5, sticky="nsew")
        self.typeToReceive = Radiobutton(self.frame2, text="Sell", variable=self.typeRun, value=2, anchor='w',command="")
        self.typeToReceive.grid(row=1, column=7, columnspan=2, padx = 5, pady = 5, sticky="nsew")

        self.tpLabel = Label(self.frame2, text="Take Profit (%):", anchor='w', width=20)
        self.tpLabel.grid(row=2, column=0, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.tp = StringVar(value="0.1")
        self.inputTp= Entry(self.frame2,textvariable=self.tp)
        self.inputTp.grid(row=2, column=2, columnspan=2, padx = 5, pady = 5, sticky="nsew")

        self.slLabel = Label(self.frame2, text="Stop Loss (%):", anchor='w', width=20)
        self.slLabel.grid(row=2, column=4, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.sl = StringVar(value="0.1")
        self.inputSl= Entry(self.frame2,textvariable=self.sl)
        self.inputSl.grid(row=2, column=6, columnspan=2, padx = 5, pady = 5, sticky="nsew")

        self.totalOrderLabel = Label(self.frame2, text="Total Order:", anchor='w', width=20)
        self.totalOrderLabel.grid(row=3, column=0, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.totalOrder = IntVar(value=2)
        self.inputTotalOrder= Entry(self.frame2,textvariable=self.totalOrder)
        self.inputTotalOrder.grid(row=3, column=2, columnspan=2, padx = 5, pady = 5, sticky="nsew")

        self.telegramLabel = Label(self.frame2, text="Telegram ID:", anchor='w', width=20)
        self.telegramLabel.grid(row=3, column=4, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.telegramID = StringVar(value="1313596710")
        self.inputTelegramID= Entry(self.frame2,textvariable=self.telegramID)
        self.inputTelegramID.grid(row=3, column=6, columnspan=2, padx = 5, pady = 5, sticky="nsew")

        self.frame4 = Frame(self.parent, relief=RAISED, borderwidth=1)
        self.frame4.grid(row=2, column=0, sticky="nsew")

        self.buyPriceGetLabel = Label(self.frame4, text="Buy Price:", anchor='w', width=20)
        self.buyPriceGetLabel.grid(row=0, column=0, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.buyPriceValue = Label(self.frame4, text="0", anchor='w', width=20)
        self.buyPriceValue.grid(row=0, column=2, columnspan=2, padx = 5, pady = 5, sticky="nsew")

        self.sellPriceGetLabel = Label(self.frame4, text="Sell Price:", anchor='w', width=20)
        self.sellPriceGetLabel.grid(row=0, column=4, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.sellPriceValue = Label(self.frame4, text="0", anchor='w', width=20)
        self.sellPriceValue.grid(row=0, column=6, columnspan=2, padx = 5, pady = 5, sticky="nsew")

        self.quantityBuyLabel = Label(self.frame4, text="Quantity Buy:", anchor='w', width=20)
        self.quantityBuyLabel.grid(row=1, column=0, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.quantityBuy = Label(self.frame4, text="0", anchor='w', width=20)
        self.quantityBuy.grid(row=1, column=2, columnspan=2, padx = 5, pady = 5, sticky="nsew")

        self.quantitySellLabel = Label(self.frame4, text="Quantity Sell:", anchor='w', width=20)
        self.quantitySellLabel.grid(row=1, column=4, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        self.quantitySell = Label(self.frame4, text="0", anchor='w', width=20)
        self.quantitySell.grid(row=1, column=6, columnspan=2, padx = 5, pady = 5, sticky="nsew")
        

        self.frame3 = Frame(self.parent, relief=RAISED, borderwidth=1)
        self.frame3.grid(row=3, column=0, sticky="nsew")

        self.stopButton = Button(self.frame3, text="Stop", bg='#ff3131', width=15, command=self.Stop)
        self.stopButton.grid(row=0, column=0, padx = (380,5), pady = 5, sticky="nsew")

        self.startButton = Button(self.frame3, text="Start", bg='#5bc810', width=15, command=self.Start)
        self.startButton.grid(row=0, column=1, padx = 5, pady = 5, sticky="nsew")

        self.frame_5 = Frame(self.parent, relief=RAISED, borderwidth=1)
        self.frame_5.grid(row=4, column=0, columnspan=3, sticky="nsew")

        self.textarea = Text(self.frame_5, width=67, height=10)
        #self.textarea.grid(side=LEFT, padx=10, pady=10)
        self.textarea.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.textarea.tag_config('r', foreground="red")
        self.textarea.tag_config('g', foreground="green")
        self.textarea.tag_config('p', foreground="purple")

        scrollbar = Scrollbar(self.frame_5,command=self.textarea.yview)
        scrollbar.grid(row=0, column=3, sticky='nsew')
        self.textarea['yscrollcommand'] = scrollbar.set

    def FindBox(self, event):
        value = event.widget.get()

        if value == '':
            self.dropMenuOne['values'] = self.optionsPair
        else:
            data = []
            for item in self.optionsPair:
                if value.lower() in item.lower():
                    data.append(item)

            self.dropMenuOne['values'] = data

    def CheckFail(self):
        excType, excObj, excTb = sys.exc_info()
        fname = os.path.split(excTb.tb_frame.f_code.co_filename)[1]
        err = str(excType) + "---" + str(fname) + "---" +str(excTb.tb_lineno)
        status = str(err)
        print(status)

    def GetTime(self):
        return datetime.now().strftime("%H:%M:%S")

    def Update(self):
        while True:
            try:
                pair = self.clickedOne.get()
                #print(pair)
                amount = float(self.amount.get())
                interval = self.clickedTimesOne.get()
                tp = self.tp.get()
                sl = self.sl.get()
                typeRun = self.typeRun.get()
                if pair != "" and amount != 0 and interval != 0 and tp != 0 and sl != 0:
                    buyPrice, sellPrice = self.ctrl.GetPriceBuyAndSell(pair, interval)
                    if typeRun == 1:
                        priceToBuy = float(buyPrice)
                    else:
                        priceToBuy = float(sellPrice)
                    quantityBuy = round(amount/priceToBuy,8)
                    quantitySell = round(quantityBuy*99.85/100,8)
                    self.buyPriceValue["text"] = str(buyPrice)
                    self.sellPriceValue["text"] = str(sellPrice)
                    self.quantityBuy["text"] = str(quantityBuy)
                    self.quantitySell["text"] = str(quantitySell)
            except:
                print("Failed")
                self.CheckFail()
                pass
            sleep(2)

    def SetAccount(self):
        Thread(target=self.BrowseButtonAddress, daemon = True).start()

    def BrowseButtonAddress(self):
        urlFile = filedialog.askopenfilename(title="Import api account", filetypes=((".txt file", "*.txt"),))
        self.folderPath.set(urlFile)
        self.ctrl = Controller(urlFile)
        self.optionsPair = self.ctrl.GetAllPairs()
        self.dropMenuOne['values'] = self.optionsPair
        Thread(target=self.Update, daemon=True).start()

    def Start(self):
        Thread(target=self.Trade, daemon = True).start()

    def Trade(self):
        pair = self.clickedOne.get()
        amount = float(self.amount.get())
        interval = self.clickedTimesOne.get()
        tp = float(self.tp.get())
        sl = float(self.sl.get())
        typeRun = self.typeRun.get()
        totalOrder = self.totalOrder.get()
        with open("./Data/history.json", "r") as dt:
            history = json.load(dt)
        telegramID = self.telegramID.get()
        msg = SendMessageTelegram()
        mess = ""
        mess = self.GetTime() + ": Start Bot" + "\n"
        msg.SendMessage(telegramID, mess)
        self.textarea.insert(END, mess)
        self.textarea.see(END)
        self.status = True
        
        if pair != "" and amount != 0 and interval != 0 and tp != 0 and sl != 0:
            while self.status:
                buyPrice, sellPrice = self.ctrl.GetPriceBuyAndSell(pair, interval)
                if typeRun == 1:
                    priceToBuy = buyPrice
                else:
                    priceToBuy = sellPrice
                quantityBuy = round(amount/priceToBuy,8)
                if len(history) == 0:
                    order = self.ctrl.CreateOrder(pair, "BUY", quantityBuy, priceToBuy)
                    _status = order.get('status')
                    if _status == 'FILLED':
                        history.append(order)
                        mess = self.GetTime() + ": BUY successfully at %.2f"%(float(order["fills"][0]["price"])) + "\n"
                        self.textarea.insert(END, mess, "g")
                        self.textarea.see(END)
                        msg.SendMessage(telegramID, mess)
                        with open("./Data/history.json", "w+") as dta:
                            json.dump(history, dta)
                    elif _status == 'EXPIRED':
                        print("BUY FAILED")
                if len(history) > 0:
                    for h in history:
                        price = float(h["fills"][0]["price"])
                        if buyPrice > price and (buyPrice-price)/price*100 >= tp:
                            order = self.ctrl.CreateOrder(pair, "SELL", float(h["origQty"]), priceToBuy)
                            _status = order.get('status')
                            if _status == 'FILLED':
                                history.remove(h)
                                mess = self.GetTime() + ": SELL successfully at %.2f"%(float(order["fills"][0]["price"])) + "\n"
                                self.textarea.insert(END, mess, "r")
                                self.textarea.see(END)
                                msg.SendMessage(telegramID, mess)
                                with open("./Data/history.json", "w+") as dta:
                                    json.dump(history, dta)
                            elif _status == 'EXPIRED':
                                print("SELL FAILED")
                if len(history) > 0:
                    h = history[-1]
                    price = float(h["fills"][0]["price"])
                    if buyPrice < price and (price-buyPrice)/price*100 > sl and len(history) < totalOrder:
                        order = self.ctrl.CreateOrder(pair, "BUY", quantityBuy, priceToBuy)
                        _status = order.get('status')
                        if _status == 'FILLED':
                            history.append(order)
                            mess = self.GetTime() + ": BUY successfully at %.2f"%(float(order["fills"][0]["price"])) + "\n"
                            self.textarea.insert(END, mess, "g")
                            self.textarea.see(END)
                            msg.SendMessage(telegramID, mess)
                            with open("./Data/history.json", "w+") as dta:
                                json.dump(history, dta)
                        elif _status == 'EXPIRED':
                            print("BUY FAILED")
        mess = self.GetTime() + ": Stop Bot" + "\n"
        self.textarea.insert(END, mess)
        self.textarea.see(END)
        msg.SendMessage(telegramID, mess)

    def Stop(self):
        self.status = False
        order = []
        with open("./Data/history.json", "w+") as history:
            json.dump(order, history)