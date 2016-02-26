from math import *
from tkinter import *
from tkinter import ttk

#First we need a formula to calculate the standard normal cumulative distribution function. The code for this function 
#is copyed from http://www.espenhaug.com/black_scholes.html
def CND(X):

    (a1,a2,a3,a4,a5) = (0.31938153, -0.356563782, 1.781477937,
                        -1.821255978, 1.330274429)
    L = abs(X)
    K = 1.0 / (1.0 + 0.2316419 * L)
    w = 1.0 - 1.0 / sqrt(2*pi)*exp(-L*L/2.) * (a1*K + a2*K*K + a3*pow(K,3) +
    a4*pow(K,4) + a5*pow(K,5))
    if X<0:

        w = 1.0-w

    return w

#Formula for calculating N(d1)
def d1(S,X,v,r,T):
            
    return (log(S/X)+(r+v*v/2)*T)/(v*sqrt(T))

#Formula for calculating N(d2)
def d2(S,X,v,r,T):

    return d1(S,X,v,r,T)-(v*sqrt(T))

#Formula's for calculating N'(d1) and N'(d2) to simplify some of the
#calculations later
def dNd1(S,X,v,r,T):

    dNd1 = (1.0/sqrt(2*pi))*exp(-(d1(S,X,v,r,T)*d1(S,X,v,r,T))/2)
    return (dNd1)

def dNd2(S,X,v,r,T):

    dNd2 = (1.0/sqrt(2*pi))*exp(-(d2(S,X,v,r,T)*d2(S,X,v,r,T))/2)
    return (dNd2)

#Formula for calculating the Black Scholes Option value
def BSM(Flag,S,X,v,r,T):
    
    if Flag=='c':
        call = S*CND(d1(S,X,v,r,T))-X*exp(-r*T)*CND(d2(S,X,v,r,T))
        return (call)
    if Flag=='p': 
        put = X*exp(-r*T)*CND(-d2(S,X,v,r,T))-S*CND(-d1(S,X,v,r,T))
        return (put)

#Formula for calculation the Intrensic Value of the option
def IV(Flag,S,X):

    if Flag=='c':
        IV = S-X
        if IV>0:
            return (IV)
        else:
            return (0)
    if Flag=='p':
        IV = X-S
        if IV>0:
            return (IV)
        else:
            return (0)

#Formula for calculation the Time Value of the option
def TV(Flag,S,X,v,r,T):

    if Flag=='c':
        TV = BSM('c',S,X,v,r,T)-IV('c',S,X)
        return (TV)
    if Flag=='p':
        TV = BSM('p',S,X,v,r,T)-IV('p',S,X)
        return (TV)

#Formula's for calculating the "Greeks"
def delta(Flag,S,X,v,r,T):

    if Flag=='c':
        return (CND(d1(S,X,v,r,T)))
    if Flag=='p':
        return (CND(d1(S,X,v,r,T))-1)


def vega(S,X,v,r,T):

    vega = (S*sqrt(T)*(exp((-0.5*d1(S,X,v,r,T)**2)))/(sqrt(2*pi)))
    return (vega/100)


def gamma(S,X,v,r,T):

    gamma = (X*exp(-r*T)*dNd2(S,X,v,r,T))/(S*S*v*sqrt(T))
    return (gamma)
            

def theta(Flag,S,X,v,r,T):

    if Flag=='c':
        theta = -X*exp(-r*T)* (r * CND(d2(S,X,v,r,T)) + ((v * dNd2(S, X, v, r, T))/(2.0 * sqrt(T))))
        return (theta/365.0)
    if Flag=='p':
        theta = X*exp(-r*T)* (r * CND(-d2(S,X,v,r,T)) - ((v * dNd2(S, X, v, r, T))/(2.0 * sqrt(T))))
        return (theta/365.0)


def rho(Flag,S,X,v,r,T):

    if Flag=='c':
        rho = T*X*exp(-r*T)*CND(d2(S,X,v,r,T))
        return (rho/100)
    if Flag=='p':
        rho = T*X*exp(-r*T)*CND(-d2(S,X,v,r,T))
        return (rho/100)


def NewtonBSM(Flag,S,X,r,T,MV):
    tol = 1.0e-9

    if Flag=='c':
        vol = sqrt(2*pi / T) * MV / S
    if Flag=='p':
        vol = sqrt(2*pi / T) * ((S - X * exp(-r*T)+ MV) / S)

    for i in range(100):
        v_i = vol - (BSM(Flag, S, X, vol, r, T) - MV) / (vega(S, X, vol, r, T)*100)
        
        diff = abs(v_i - vol)
        if diff < tol:
            return v_i
        vol = v_i

        
def calculateall():

    try:
        S = float(stock.get())
    except:
        messagebox.showinfo("Stock Price", "No Stock Price given or wrong format")
    try:
        X = float(strike.get())
    except:
        messagebox.showinfo("Strike Price", "No Strike Price given or wrong format")
    try:
        v = float(vol.get())
    except:
        messagebox.showinfo("Std.dev", "No Standard Deviation given or wrong format")
    try:
        r = float(risk.get())
    except:
        messagebox.showinfo("risk free", "No risk free rate given or wrong format")
    try:
        T = float(time.get())/365
    except:
        messagebox.showinfo("Time", "No Time parameter given or wrong format")
    try:
        MVc = float(mvc.get())
    except:
        Exception

    try:
        MVp = float(mvp.get())
    except:
        Exception      

    callv.set(round(BSM('c',S,X,v,r,T), 4))
    putv.set(round(BSM('p',S,X,v,r,T), 4))
    IVc.set(round(IV('c',S,X), 4))
    IVp.set(round(IV('p',S,X), 4))
    TVc.set(round(TV('c',S,X,v,r,T), 4))
    TVp.set(round(TV('p',S,X,v,r,T), 4))
    deltaC.set(round(delta('c',S,X,v,r,T), 4))
    deltaP.set(round(delta('p',S,X,v,r,T), 4))
    vegaC.set(round(vega(S,X,v,r,T), 4))
    vegaP.set(round(vega(S,X,v,r,T), 4))
    thetaC.set(round(theta('c',S,X,v,r,T), 4))
    thetaP.set(round(theta('p',S,X,v,r,T), 4))
    rhoC.set(round(rho('c',S,X,v,r,T), 4))
    rhoP.set(round(rho('p',S,X,v,r,T), 4))
    gammaC.set(round(gamma(S,X,v,r,T), 4))
    gammaP.set(round(gamma(S,X,v,r,T), 4))
    try:
        impvC.set(round(NewtonBSM('c',S,X,r,T,MVc), 4))
    except:
        impvC.set(0)
    try:
        impvP.set(round(NewtonBSM('p',S,X,r,T,MVp), 4))
    except:
        impvP.set(0)
    
#GUI Part of the Program
root = Tk()
root.geometry('500x350')
root.title('BSM Option Pricing Calculator')

#Labels for the input parameters
label1 = ttk.Label(text="Stock Price").place(x=30, y=50)
label2 = ttk.Label(text="Strike Price").place(x=30, y=70)
label3 = ttk.Label(text="Standard Deviation").place(x=30, y=90)
label4 = ttk.Label(text="Risk Free Rate").place(x=30, y=110)
label5 = ttk.Label(text="Days to Expiration").place(x=30, y=130)

label16 = ttk.Label(text="Market Value").place(x=30, y=180)
label17 = ttk.Label(text="Call").place(x=140, y=160)
label18 = ttk.Label(text="Put").place(x=190, y=160)
label19 = ttk.Label(text="Implied Volatility").place(x=30, y=205)

#Labels for the outputs from calculations
Label6 = ttk.Label(text="Call").place(x=380, y=30)
Label7 = ttk.Label(text="Put").place(x=440, y=30)
Label8 = ttk.Label(text="Theoretical Value").place(x=240, y=50)
Label9 = ttk.Label(text="Intrensic Value").place(x=240, y=80)
Label10 = ttk.Label(text="Time Value").place(x=240, y=100)
Label11 = ttk.Label(text="Delta").place(x=240, y=130)
Label12 = ttk.Label(text="Vega 1%").place(x=240, y=150)
Label13 = ttk.Label(text="Gamma").place(x=240, y=170)
Label14 = ttk.Label(text="Theta/365").place(x=240, y=190)
Label15 = ttk.Label(text="Rho 1%").place(x=240, y=210)

#Strings to holdt the output from calculations
callv = StringVar()
putv = StringVar()
IVc = StringVar()
IVp = StringVar()
TVc = StringVar()
TVp = StringVar()
deltaC = StringVar()
deltaP = StringVar()
vegaC = StringVar()
vegaP = StringVar()
thetaC = StringVar()
thetaP = StringVar()
rhoC = StringVar()
rhoP = StringVar()
gammaC = StringVar()
gammaP = StringVar()
impvC = StringVar()
impvP = StringVar()

#Strings to hold the user inputs
stock = StringVar()
strike = StringVar()
vol = StringVar()
risk = StringVar()
time = StringVar()
mvc = StringVar()
mvp = StringVar()
        
#Entryboxes for the user inputs
entry1 = ttk.Entry(width=7, textvariable=stock).place(x=150, y=50)
entry2 = ttk.Entry(width=7, textvariable=strike).place(x=150, y=70)
entry3 = ttk.Entry(width=7, textvariable=vol).place(x=150, y=90)
entry4 = ttk.Entry(width=7, textvariable=risk).place(x=150, y=110)
entry5 = ttk.Entry(width=7, textvariable=time).place(x=150, y=130)
entry6 = ttk.Entry(width=6, textvariable=mvc).place(x=135, y=180)
entry7 = ttk.Entry(width=6, textvariable=mvp).place(x=185, y=180)

#Outpuy from calculations
output1 = ttk.Label(textvariable=callv, width=7, background="grey").place(x=370,y=50)
output2 = ttk.Label(textvariable=putv, width=7, background="grey").place(x=430,y=50)
output3 = ttk.Label(textvariable=IVc, width=7, background="grey").place(x=370,y=80)
output4 = ttk.Label(textvariable=IVp, width=7, background="grey").place(x=430,y=80)
output5 = ttk.Label(textvariable=TVc, width=7, background="grey").place(x=370,y=100)
output6 = ttk.Label(textvariable=TVp, width=7, background="grey").place(x=430,y=100)
output7 = ttk.Label(textvariable=deltaC, width=7, background="grey").place(x=370,y=130)
output8 = ttk.Label(textvariable=deltaP, width=7, background="grey").place(x=430,y=130)
output9 = ttk.Label(textvariable=vegaC, width=7, background="grey").place(x=370,y=150)
output10 = ttk.Label(textvariable=vegaP, width=7, background="grey").place(x=430,y=150)
output11 = ttk.Label(textvariable=gammaC, width=7, background="grey").place(x=370,y=170)
output12 = ttk.Label(textvariable=gammaP, width=7, background="grey").place(x=430,y=170)
output13 = ttk.Label(textvariable=thetaC, width=7, background="grey").place(x=370,y=190)
output14 = ttk.Label(textvariable=thetaP, width=7, background="grey").place(x=430,y=190)
output15 = ttk.Label(textvariable=rhoC, width=7, background="grey").place(x=370,y=210)
output16 = ttk.Label(textvariable=rhoP, width=7, background="grey").place(x=430,y=210)
output17 = ttk.Label(textvariable=impvC, width=6, background="grey").place(x=135,y=205)
output18 = ttk.Label(textvariable=impvP, width=6, background="grey").place(x=185,y=205)

#Calculate function and button
button1 = ttk.Button(text="Calculate", command=calculateall).place(x=50, y=260)

root.mainloop()
