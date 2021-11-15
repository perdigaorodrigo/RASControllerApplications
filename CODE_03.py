#!/usr/bin/env python
# coding: utf-8

# In[59]:


import pandas as pd
import numpy as np
import win32com.client
from osgeo import gdal
import h5py
from qgis.core import *
import qgis.utils
from qgis.PyQt.QtCore import QVariant

WSE_list=[]
area_list=[]
chan_list=[]
grass_list=[]
urban_list=[]
fn=r'C:\Users\Rodrigo\Desktop\HECRAS\ESTUDO_RIO_DOCE\MODELO_ARTIGO\RAS 1D\C_PENA\Inundation Boundary (Max Value_0).shp'


# In[60]:


for k in range(1000):
    
    RC=win32com.client.Dispatch("RAS507.HECRASCONTROLLER")
    RC.Project_Open(r"C:\Users\Rodrigo\Desktop\HECRAS\ESTUDO_RIO_DOCE\MODELO_ARTIGO\RAS 1D\C_PENA.prj")
    RC.ShowRAS()
    
    Mann_chan=round(np.random.uniform(0.03,0.04),4)
    Mann_grass=round(np.random.uniform(0.03,0.05),4)
    Mann_urban=round(np.random.uniform(0.08,0.14),4)
    
    chan_list.append(Mann_chan)
    grass_list.append(Mann_grass)
    urban_list.append(Mann_urban)
    
    urban=list(range(41,64))
    land=[ind for ind in range(91) if ind not in ignore]

    for i in (land):
        Var_Mann=RC.Geometry_SetMann_LChR(river,reach,nodes[i],Mann_grass,Mann_chan,Mann_grass)
    for i in (urban):
        Var_Mann=RC.Geometry_SetMann_LChR(river,reach,nodes[i],Mann_grass,Mann_chan,Mann_urban)
   
    RC.Compute_CurrentPlan(None,None)
    RC.Project_Save()
    water_list=[]
    for i in range(len(nodes)):
        water=RC.Output_NodeOutput(1,1,i+1,None,1,2)[0]
        water_list.append(water)
    WSE_list.append(water_list)
    RC.QuitRAS()
        
    layer=QgsVectorLayer(fn,'','ogr')
    area=layer.getFeature(0)[3]
    area_list.append(area)
    RC.QuitRAS()
    print(area,k,Mann_chan,Mann_grass,Mann_urban)


# In[17]:


RC=win32com.client.Dispatch("RAS507.HECRASCONTROLLER")
RC.Project_Open(r"C:\Users\Rodrigo\Desktop\HECRAS\ESTUDO_RIO_DOCE\MODELO_ARTIGO\RAS 1D\C_PENA.prj")
RC.ShowRAS()
river=RC.Geometry_GetRivers()[1][0]
reach=RC.Geometry_GetReaches(1)[2][0]
nodes=RC.Geometry_GetNodes(1,1)[3]
nodes=list(nodes)


# In[43]:


RC=win32com.client.Dispatch("RAS507.HECRASCONTROLLER")
RC.Project_Open(r"C:\Users\Rodrigo\Desktop\HECRAS\ESTUDO_RIO_DOCE\MODELO_ARTIGO\RAS 1D\C_PENA.prj")
RC.ShowRAS()


# In[44]:


river=RC.Geometry_GetRivers()[1][0]
reach=RC.Geometry_GetReaches(1)[2][0]
nodes=RC.Geometry_GetNodes(1,1)[3]
nodes=list(nodes)


# In[45]:


Var_Mann=RC.Geometry_SetMann_LChR(river,reach,nodes[0],Mann_grass,Mann_chan,Mann_grass)


# In[46]:


for i in (land):
    Var_Mann=RC.Geometry_SetMann_LChR(river,reach,nodes[i],Mann_grass,Mann_chan,Mann_grass)
for i in (urban):
    Var_Mann=RC.Geometry_SetMann_LChR(river,reach,nodes[i],Mann_grass,Mann_chan,Mann_urban)


# In[50]:


RC.ShowRAS()


# In[51]:


RC.Output_NodeOutput(1,1,10,None,1,2)[0]


# In[57]:


area_list,WSE_list


# In[61]:


WSE_list,area_list


# In[73]:


df=pd.DataFrame({"WSE":WSE_list,"Area":area_list})


# In[75]:


df2=pd.DataFrame({"Channel":chan_list,"Grass":grass_list,"Urban":urban_list})


# In[68]:


len(chan_list)


# In[76]:


df.to_csv(r"C:\Users\Rodrigo\Desktop\HECRAS\ESTUDO_RIO_DOCE\MODELO_ARTIGO\RAS 1D\results.csv")


# In[77]:


df2.to_csv(r"C:\Users\Rodrigo\Desktop\HECRAS\ESTUDO_RIO_DOCE\MODELO_ARTIGO\RAS 1D\entry.csv")


# In[ ]:




