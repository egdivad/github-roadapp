# https://stackoverflow.com/questions/4028267/how-to-render-latex-markup-using-python

import matplotlib.pyplot as plt
a = '\\frac{a}{b}'  #notice escaped slash
plt.plot()
plt.text(0.5, 0.5,'$%s$'%a)
plt.show()

a = r'\frac{a}{b}'
ax = plt.axes([0,0,0.3,0.3]) #left,bottom,width,height
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')
plt.text(0.4,0.4,'$%s$' %a,size=50,color="green")
plt.show()
