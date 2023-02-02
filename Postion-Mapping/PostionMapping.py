import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd


class financeGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        def clearData():

            bondPriceGUI.set("")
            stockPriceGUI.set("")
            callPriceGUI.set("")
            putPriceGUI.set("")
            futurePriceGUI.set("")

            kFutureGUI.set("")
            kCallGUI.set("")
            kPutGUI.set("")

            nStockGUI.set("")
            nFutureGUI.set("")
            nCallGUI.set("")
            nPutGUI.set("")
            nBondGUI.set("")

            # Create a blank graph
            self.figure = Figure(figsize=(5, 4), dpi=100)
            self.ax = self.figure.add_subplot(111)
            self.ax.set_xlim(-10, 120)
            self.ax.set_ylim(-20, 100)
            self.ax.set_xlabel("S(t)")
            self.ax.set_ylabel("$")
            self.ax.grid()
            self.ax.axhline(y=0, color='black', linewidth=1)
            self.ax.axvline(x=0, color='black', linewidth=1)
            self.ax.set_xticks(range(-10, 130, 10))
            self.ax.set_aspect('1.1')
            self.ax.set_yticks(range(-20, 110, 10))
            self.canvas = FigureCanvasTkAgg(self.figure, self)
            self.canvas.draw()
            self.canvas.get_tk_widget().place(x=350, y=100)

            # creating label at top of screen and placing it at x,y location
            self.titlePage = tk.Label(self, text="Postion Graph", font=20)
            self.titlePage.config(bg='white')
            self.titlePage.place(x=(550), y=100)

        #functions to calculate call profit and value
        def callProfit(k, n, p, st):
            try:
                if k < st:
                    callValue = n * (st - k)
                    profit = callValue - (p * n)
                else:
                    callValue = 0
                    profit = callValue - (p * n)

                return profit

            except:
                return
        def callVal(k, n, p, st):
            try:
                if k < st:
                    callValue = n * (st - k)
                    profit = callValue - (p * n)
                else:
                    callValue = 0

                return callValue

            except:
                print("N/A")

        #functions to calculate put profit and value
        def putProfit(k, n, p, st):
            if k > st:
                putValue = n * (k - st)
                profit = putValue - (p * n)

            else:
                putValue = 0
                profit = (putValue - (n * p))

            return profit
        def putVal(k, n, p, st):
            if k > st:
                putValue = n * (k - st)
                profit = putValue - (p * n)

            else:
                putValue = 0
                profit = (putValue - (n * p))

            return putValue

            # #for testing the output of the GUI
            # print(f"Stock: price-{type(stockPrice)}, n-{numStock}, k- 'N/A' ")
            # print(f"Bond: price-{bondPrice}, n-{numBond}, k- 'N/A' ")
            # print(f"Future: price-{futurePrice}, n-{numFuture}, k- {kFuture} ")
            # print(f"Call: price-{callPrice}, n-{numCall}, k- {kCall} ")
            # print(f"Put: price-{putPrice}, n-{numPut}, k- {kPut} ")

        #functions to calculate Stock value and profit
        def stockProfit(n, p, st):
            try:
                stockVal = n * (st)
                stockProfit = stockVal - (n * p)
            except:
                return

            return stockProfit
        def stockVal(n, p, st):
            try:
                stockVal = n * (st)
                stockProfit = stockVal - (n * p)
            except:
                print("N/A")

            return stockVal

        #functuons to calcualte bondVal and Bond profit
        def bondVal(n, p):
            try:
                bondvalue = (n * p)

            except:
                print("n/a")

            return bondvalue

        def calculatePostion():

            # global var/ creating list form 0-100 of potential states of ST
            StList = []
            dataDict = {"ST-DATA": StList}

            for i in range(0, 130, 10):
                StList.append(i)

            def get_float(value):
                try:
                    return float(value)
                except ValueError:
                    return 0

            bondPrice = get_float(self.bondInput.get())
            stockPrice = get_float(self.stockInput.get())
            callPrice = get_float(self.callInput.get())
            putPrice = get_float(self.putInput.get())
            numBond = get_float(self.bondNum.get())
            numStock = get_float(self.stockNum.get())
            numCall = get_float(self.callNum.get())
            numPut = get_float(self.putNum.get())
            kCall = get_float(self.callStrike.get())
            kPut = get_float(self.putStrike.get())


            callValue =[]
            putValue = []
            stockValue =[]
            bondValue =[]
            totalValue =[]

            callProf = []
            putProf = []
            stockProf = []
            bondProf = []
            totalProf = []


            for st in StList:
                #appending values into each list
                callValue.append(callVal(kCall,numCall,callPrice,st))
                putValue.append(putVal(kPut,numPut,callPrice,st))
                stockValue.append(stockVal(numStock,stockPrice,st))
                bondValue.append(bondVal(numBond,bondPrice))

                #appending profit into each list
                callProf.append(callProfit(kCall, numCall, callPrice, st))
                putProf.append(putProfit(kPut, numPut, callPrice, st))
                stockProf.append(stockProfit(numStock, stockPrice, st))
                bondProf.append(bondVal(numBond, bondPrice))


            #dictionaries to hold values
            valueDict = {"ST-DATA": StList, "Call-Data": callValue, "Put-Data": putValue,                                    "Stock-Data": stockValue,
                        "Bond-Data": bondValue}

            profitDict = {"ST-DATA": StList, "Call-Profit": callProf, "Put-Profit":                                        putProf,  "Stock-Profit": stockProf,
                        "Bond-Profit": bondValue}


            #dataframes of those two dictionaires
            valueDataFrame = pd.DataFrame(valueDict)
            profitDataFrame = pd.DataFrame(profitDict)

            rowValue = 0

            for st in StList:
                totalValue.append(valueDataFrame.loc[rowValue].sum()-st)
                rowValue+=1

            valueDict2 = {"ST-DATA": StList, "Call-Data": callValue, "Put-Data": putValue,                                    "Stock-Data":                          stockValue,
                        "Bond-Data": bondValue, "Total-Data": totalValue}



            rowProfit = 0
            for st in StList:
                totalProf.append(profitDataFrame.loc[rowProfit].sum() - st)
                rowProfit += 1

            profitDict2 = {"ST-DATA": StList, "Call-Profit": callProf, "Put-Profit": putProf,                                    "Stock-Profit": stockProf,
                          "Bond-Profit": bondValue,"Total-Profit": totalProf}

            print(pd.DataFrame(valueDict2), pd.DataFrame(profitDict2))

            yPoints = totalValue
            xPoints = StList

            xProfitPoints = StList
            yProfitPoints = totalProf


            # Create a graph with the ST value at t0 value
            self.figure = Figure(figsize=(5, 4), dpi=100)
            self.ax = self.figure.add_subplot(111)



            #adjusting my y axis based on input
            largestValue = max(totalValue)
            smallestValue = min(totalValue)




            self.ax.set_xlim(-10, 120)
            self.ax.set_ylim(-20, 100)
            self.ax.set_xlabel("S(t)")
            self.ax.set_ylabel("$")
            self.ax.grid()
            self.ax.axhline(y=0, color='black', linewidth=1)
            self.ax.axvline(x=0, color='black', linewidth=1)
            self.ax.set_xticks(range(-10, 130, 10))
            self.ax.set_aspect('1.1')
            self.ax.set_yticks(range(-20, 110, 10))
            self.canvas = FigureCanvasTkAgg(self.figure, self)
            self.canvas.draw()
            self.canvas.get_tk_widget().place(x=350, y=100)


            # creating label at top of screen and placing it at x,y location
            self.titlePage = tk.Label(self, text="Postion Graph", font=20)
            self.titlePage.config(bg='white')
            self.titlePage.place(x=(550), y=100)

            self.ax.plot(xPoints, yPoints, color = "orange" ,label = "Time T Value ")
            self.ax.plot(xProfitPoints, yProfitPoints, color="blue", label="Time T Profit ")
            self.ax.legend()




        #label at top
        self.topLabel = tk.Label(self, text= "Position Mapping")
        self.topLabel.config(bg = 'white', font=("Arial",16,"bold"))
        self.topLabel.place(x=300,y=8)

        #varibales to store data from input from user
        bondPriceGUI = tk.StringVar()
        stockPriceGUI = tk.StringVar()
        callPriceGUI = tk.StringVar()
        putPriceGUI = tk.StringVar()
        futurePriceGUI = tk.StringVar()

        kFutureGUI=tk.StringVar()
        kCallGUI = tk.StringVar()
        kPutGUI = tk.StringVar()

        nStockGUI = tk.StringVar()
        nFutureGUI = tk.StringVar()
        nCallGUI = tk.StringVar()
        nPutGUI = tk.StringVar()
        nBondGUI = tk.StringVar()

        #code to display title of screen and set gemomtry
        self.title("Postion Mapping")
        self.geometry("800x600")
        self.config(bg='white')

        #create and place labels for Europena options
        self.stockTitle = tk.Label(self, text = "Bond")
        self.stockTitle.config(bg = 'white', font=("Arial",10))
        self.stockTitle.place(x=7, y =150)

        self.bondTitle = tk.Label(self, text = "Stock")
        self.bondTitle.config(bg = 'white',font=("Arial",10))
        self.bondTitle.place(x=7, y= 220)

        self.callTitle = tk.Label(self, text="Call")
        self.callTitle.config(bg='white',font=("Arial",10))
        self.callTitle.place(x=7, y=290)

        self.putTitle = tk.Label(self, text="Put")
        self.putTitle.config(bg = 'white',font=("Arial",10))
        self.putTitle.place(x=7, y=360)


        #calculate button
        self.calButton = tk.Button(self, text = "Calculate",font=("Arial",12, "bold"), command =            calculatePostion)
        self.calButton.place(x = 150, y =450)

        #clear data button
        self.clearDataButton = tk.Button(self, text ="Clear",font=("Arial",12, "bold"), command =              clearData)
        self.clearDataButton.place(x = 165, y= 500)

        #creaing input fields for options
        self.bondInput = tk.Entry(self, width = 5, textvariable = bondPriceGUI)
        self.bondInput.place(y=150, x = 65 )
        self.stockInput = tk.Entry(self, width =5, textvariable = stockPriceGUI)
        self.stockInput.place(y=220, x=65)

        self.callInput = tk.Entry(self, width =5, textvariable = callPriceGUI)
        self.callInput.place(y=290, x=65)
        self.putInput = tk.Entry(self, width =5, textvariable = putPriceGUI)
        self.putInput.place(y=360, x=65)


        #label for colums
        self.numberLabel = tk.Label(self, text = "Number of Securities")
        self.numberLabel.place(x =140, y = 80)
        self.numberLabel.config(bg = 'white',font=("Arial",10, "bold"))

        self.numberLabel = tk.Label(self, text = "Price of Security")
        self.numberLabel.place(x =10, y = 80)
        self.numberLabel.config(bg = 'white',font=("Arial",10, "bold"))


        self.numberLabel = tk.Label(self, text = "Strike Price")
        self.numberLabel.place(x =300, y = 80)
        self.numberLabel.config(bg = 'white',font=("Arial",10, "bold"))


        #data entry for Number of each security
        self.bondNum = tk.Entry(self, width = 5, textvariable = nBondGUI)
        self.bondNum.place(y=150, x = 180 )
        self.stockNum = tk.Entry(self, width =5, textvariable = nStockGUI)
        self.stockNum.place(y=220, x=180)
        self.callNum = tk.Entry(self, width =5, textvariable = nCallGUI)
        self.callNum.place(y=290, x=180)
        self.putNum = tk.Entry(self, width =5, textvariable = nPutGUI)
        self.putNum.place(y=360, x=180)


        # Create a blank graph
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(-10, 120)
        self.ax.set_ylim(-20, 100)
        self.ax.set_xlabel("S(t)")
        self.ax.set_ylabel("$")
        self.ax.grid()
        self.ax.axhline(y=0, color='black', linewidth=1)
        self.ax.axvline(x=0, color='black', linewidth=1)
        self.ax.set_xticks(range(-10, 130, 10))
        self.ax.set_aspect('1.1')
        self.ax.set_yticks(range(-20, 110, 10))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x = 350, y =100)


        #data entry for Stike price
        self.bondStrike = tk.Label(self, text = "N/A", bg = "white").place(y=150, x = 320 )
        self.stockStrike = tk.Label(self, text = "N/A", bg = "white").place(y=220, x=320)
        self.callStrike = tk.Entry(self, width =5, textvariable = kCallGUI)
        self.callStrike.place(y=290, x=320)
        self.putStrike = tk.Entry(self, width =5, textvariable = kPutGUI)
        self.putStrike.place(y=360, x=320)

        # creating label at top of screen and placing it at x,y location
        self.titlePage = tk.Label(self, text="Postion Graph", font=20)
        self.titlePage.config(bg = 'white')
        self.titlePage.place(x=(550), y=100)


if __name__ == "__main__":
    gui = financeGUI()
    gui.mainloop()

