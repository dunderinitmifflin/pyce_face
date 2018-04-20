from tkinter import *


class LoanCalculator:
    """
        This class defines the laon calculator.
    """
    def __init__(self):
        window = Tk()
        window.title("Loan Calculator")

        Label(window, text="Annual Interest Rate").grid(row=1, column=1, sticky=W)
        Label(window, text="Number of Years").grid(row=2, column=1, sticky=W)
        Label(window, text="Loan Amount").grid(row=3, column=1, sticky=W)
        Label(window, text="Monthly Payment").grid(row=4, column=1, sticky=W)
        Label(window, text="Total Payment").grid(row=5, column=1, sticky=W)

        self.annualInterestRateVar = StringVar()
        Entry(window, textvariable=self.annualInterestRateVar, justify=RIGHT).grid(row=1, column=2)

        self.numberOfYearsVar = StringVar()
        Entry(window, textvariable=self.numberOfYearsVar, justify=RIGHT).grid(row=2, column=2)

        self.loanAmountVar = StringVar()
        Entry(window, textvariable=self.loanAmountVar, justify=RIGHT).grid(row=3, column=2)

        self.monthlyPaymentVar = StringVar()
        Label(window, textvariable=self.monthlyPaymentVar).grid(row=4, column=2, sticky=E)

        self.totalPaymentVar = StringVar()
        Label(window, textvariable=self.totalPaymentVar).grid(row=5, column=2, sticky=E)

        Button(window, text="Compute Payment", command=self.computePayment).grid(row=6, column=2, sticky=E)

        window.mainloop()

    def computePayment(self):
        monthlyPayment = self.getMonthlyPayment(float(self.loanAmountVar.get()),
                                                float(self.annualInterestRateVar.get()) / 12,
                                                int(self.numberOfYearsVar.get()))
        totalPayment = monthlyPayment * 12 * int(self.numberOfYearsVar.get())
        self.monthlyPaymentVar.set(format(monthlyPayment, "10.2f"))
        self.totalPaymentVar.set(format(totalPayment, "10.2f"))

    def getMonthlyPayment(self, loanAmount, monthlyInterestRate, numberOfYears):
        monthlyPayment = loanAmount * monthlyInterestRate / (1 - 1/(1+monthlyInterestRate)**(numberOfYears * 12))
        return monthlyPayment

LoanCalculator()
