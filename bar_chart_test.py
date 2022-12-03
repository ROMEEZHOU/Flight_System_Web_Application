import matplotlib.pyplot as plt

x=['a','b','c','d']
y=[10,20,30,10]
plt.bar(x,y,width=0.5,bottom=0,align='edge',color='g',edgecolor ='r',linewidth=2)
plt.title("test",size=26)
plt.xlabel('letter',size=24)
plt.ylabel('value',size=24)

plt.savefig('test.png')