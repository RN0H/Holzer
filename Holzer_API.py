
import matplotlib.pyplot as plt

from tkinter import*
import tkinter as tk
import numpy as np

class Holzer:
    def __init__ (self,master):
            self.J_K = StringVar()
            self.master = master
            self.master.title('Holzer')
            self.master.geometry('400x300')
            freqfinder=PhotoImage(file='freqfinder.png')
            self.master.iconphoto(False,freqfinder)



            e1 = Entry(self.master,textvariable=self.J_K)
            b1 = Button(self.master,text='calculate',command=self.values)
            b2 = Button(self.master,text='quit',command=self.master.destroy)

            l1 = Label(self.master,text='[J1,K1,J2,..]')
            l2 = Label(self.master,text='J = kgm^2\n K = N-m/rad')
            l2.place(x=90,y=200)
            l1.place(x=120,y=50)
            e1.place(x=200,y=50)
            b1.place(x=175,y=100)
            b2.place(x=175,y=150)


    def values(self):                     #[J][O1]-[K]([O1]-[O2])=0
          self.stiffness = []  #[K]
          self.inertia = []    #[J]
          self.theta = []      #[O]
          self.wn = []
          self.s = [float(m) for m in (self.J_K.get()).split(',')]
          self.divide()


    def divide(self):
            if len(self.s)==2:
                   print('freq is',(self.s[1]/self.s[0])**0.5)
                   return
            for i in range(len(self.s)):
                 if i%2==0:
                      self.inertia.append(self.s[i])
                 else:
                      self.stiffness.append(self.s[i])
            self.freq_range()

    def freq_range(self):

         if self.stiffness==[] or self.inertia==[]:
                  print('Insufficient data ')
                  return
         elif len(self.inertia)==1:
                   self.wn.append((self.stiffness[0]/self.inertia[0])**0.5)
                   return self.precise_freq()
         for wn in map(lambda i:i/10,range(0,10000)):
              self.theta=[]
              self.theta.append(1)
              for i in range(0,len(self.inertia)-1):
                     self.theta.append(self.theta[i]-((6.28*wn)**2*np.dot(np.array(self.inertia)[0:len(self.theta)],np.array(self.theta)))/(self.stiffness[i]))
              print(np.dot(self.inertia,self.theta),' - ',wn,' - ',self.theta)
              if int(np.dot(self.inertia,self.theta))==0:
                               self.wn.append(float(wn))
         print('frequency range is',self.wn)
         return self.precise_freq()

    def precise_freq(self):
         j=[]
         y=[]
         self.freqs=[]
         if len(self.wn)<=2:
                   self.freqs.append(self.wn)
                   print('precise frequency is',self.freqs)
                   self.plots()
         for i in range(0,len(self.wn)-1):
                    if self.wn[i+1]-self.wn[i]<2:
                            j.append(self.wn[i])
                            if i==len(self.wn)-1:
                                   self.freqs.append(np.average(j))
                                   print('precise frequency is',self.freqs)
                                   self.plots()

                    else:
                            j.append(self.wn[i])
                            y.append(j)
                            j=[]
         if j and self.wn[-1]-j[-1]<2:
               j.append(self.wn[-1])
         else:
               j = []
               j.append(self.wn[-1])
         y.append(j)
         for i in y:
              self.freqs.append(np.average(i))
         print('precise frequency is',self.freqs)
         self.plots()
    def plots(self):
        self.theta_hist=[]
        self.theta=[]
        self.freq_theta = []
        for wn in self.freqs:
            self.theta.append(1)
            for i in range(0,len(self.inertia)-1):
                    self.theta.append(self.theta[i]-((6.28*wn)**2*np.dot(np.array(self.inertia)[0:len(self.theta)],np.array(self.theta)))/(self.stiffness[i]))
            self.theta_hist.append(self.theta)
            self.theta=[]
        freq_theta = dict(zip(self.freqs,self.theta_hist))
        print('frequency:deflection',freq_theta)
        for i in range(len(list(freq_theta))):
                self.freq_theta.append(plt.plot(freq_theta[list(freq_theta)[i]],label=str(list(freq_theta)[i])+'Hz'))
        for i in self.freq_theta:
                 plt.legend()
                 plt.plot()
        plt.xlabel('Number of Discs')
        plt.ylabel('Deflection')
        plt.grid()
        plt.show()


root = tk.Tk()
Holzer(root)
root.mainloop()
