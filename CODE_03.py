import pandas as pd
import numpy as np
import win32com.client
from qgis.core import *
import qgis.utils
from qgis.PyQt.QtCore import QVariant

#CRIANDO LISTAS PARA ARMAZENAR DADOS DE NÍVEL D'ÁGUA, AREA INUNDADA E RUGOSIDADE DE MANNING SIMULADAS
WSE_list=[]
area_list=[]
chan_list=[]
grass_list=[]
urban_list=[]

#INSERINDO DIRETORIO DE SHAPEFILE DE AREA MAX INUNDADA (ARQUIVO ATUALIZADO EM CADA ITERACAO)
fn=r'C:\Users\Rodrigo\Desktop\HECRAS\ESTUDO_RIO_DOCE\MODELO_ARTIGO\RAS 1D\C_PENA\Inundation Boundary (Max Value_0).shp'

    RC=win32com.client.Dispatch("RAS507.HECRASCONTROLLER")

for k in range(1000):
       
    RC.Project_Open(r"C:\Users\Rodrigo\Desktop\HECRAS\ESTUDO_RIO_DOCE\MODELO_ARTIGO\RAS 1D\C_PENA.prj") #DIRETORIO DO ARQUIVO DE PROJETO (PRJ)
    
    RC.ShowRAS() #ABRINDO INTERFACE DO HEC-RAS
    #IDENTIFICANDO GEOMETRIAS: RIVER, REACH, NODES
    river=RC.Geometry_GetRivers()[1][0]
    reach=RC.Geometry_GetReaches(1)[2][0]
    nodes=RC.Geometry_GetNodes(1,1)[3]
    nodes=list(nodes)
    
    
    #GERACAO DE VALORES UNIFORMEMENTE DISTRIBUIDOS. OBS: DISTRIBUICAO PODE SER FACILMENTE ALTERADA.
    Mann_chan=round(np.random.uniform(0.03,0.04),4)
    Mann_grass=round(np.random.uniform(0.03,0.05),4)
    Mann_urban=round(np.random.uniform(0.08,0.14),4)
    #SALVANDO VALORES GERADOS PARA ANALISE FUTURA
    chan_list.append(Mann_chan)
    grass_list.append(Mann_grass)
    urban_list.append(Mann_urban)
    
    #DEFININDO SECOES EM QUE SE CONSIDEROU CLASSE DE USO URBANO E CLASSE DE USO DE PASTAGEM
    urban=list(range(41,64))
    land=[ind for ind in range(91) if ind not in ignore]
    #VARIANDO COEFICIENTE DE RUGOSIDADE 
    for i in (land):
        Var_Mann=RC.Geometry_SetMann_LChR(river,reach,nodes[i],Mann_grass,Mann_chan,Mann_grass)
    for i in (urban):
        Var_Mann=RC.Geometry_SetMann_LChR(river,reach,nodes[i],Mann_grass,Mann_chan,Mann_urban)
    #EXECUTANDO SIMULACAO AUTOMATICAMENTE
    RC.Compute_CurrentPlan(None,None)
    #SALVANDO PROJETO
    RC.Project_Save()
    #CRIANDO LISTA PARA ARMAZENAR WSE DE TODAS AS SECOES TRANSVERSAIS EM CADA ITERACAO 
    water_list=[]
    for i in range(len(nodes)):
        water=RC.Output_NodeOutput(1,1,i+1,None,1,2)[0]
        water_list.append(water)
    #ARMAZENANDO WSE DA ITERACAO NA LISTA DE LISTAS WSE_LIST
    WSE_list.append(water_list)
    #FECHANDO A INTERFACE DO HEC-RAS
    RC.QuitRAS()
    #EXTRAINDO AREA MAXIMA INUNDADA POR MEIO DO PYQGIS
    layer=QgsVectorLayer(fn,'','ogr')
    area=layer.getFeature(0)[3]
    area_list.append(area)
