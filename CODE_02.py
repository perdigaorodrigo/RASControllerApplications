# -*- coding: utf-8 -*-
#Executando simulação com variação automática do coef. Manning e leitura automática de resultados
"""
@author: Rodrigo Perdigão
"""
#IMPORTANDO BIBLIOTECAS
import win32com.client
import numpy as np
import pandas as pd

#ATRIBUINDO FUNCOES DO HECRASCONTROLLER AO OBJETO RC
RC=win32com.client.Dispatch("RAS507.HECRASCONTROLLER")

#ABRINDO E FECHANDO JANELA
RC.ShowRAS()

#ABRINDO PROJETO
RC.Project_Open(r"C:\Users\Rodrigo\Desktop\HECRAS\DADOS\RAS\1D_MODEL.prj")

#IDENTIFICANDO GEOMETRIA 

river=RC.Geometry_GetRivers()[1][0]
reach=RC.Geometry_GetReaches(1)[2][0]
nodes=RC.Geometry_GetNodes(1,1)[3]
nodes=list(nodes)

#VARIANDO DE PARÂMETRO DO MODELO (COEFICIENTE DE RUGOSIDADE)
Mann_chan=round(np.random.uniform(0.03,0.04),4)
Mann_bank=round(np.random.uniform(0.08,0.12),4)

for i in range(9):
    Var_Mann=RC.Geometry_SetMann_LChR(river,reach,nodes[i],Mann_bank,Mann_chan,Mann_bank)

#EXECUTANDO SIMULACAO DO PLANO ATUAL
Simulation=RC.Compute_CurrentPlan(None,None,True)

#EXTRAINDO RESULTADOS
water_list,flow_list,veloc_list =[],[],[]

for i in range(9):
    water=RC.Output_NodeOutput(1,1,i+1,None,1,2)[0]
    flow=RC.Output_NodeOutput(1,1,i+1,None,1,9)[0]
    veloc=RC.Output_NodeOutput(1,1,i+1,None,1,23)[0]
    water_list.append(water),flow_list.append(flow),veloc_list.append(veloc)
    
#ORGANIZANDO RESULTADOS (ELEVAÇÃO DA ÁGUA, VAZÕES, VELOCIDADES)
output={'Cross Sections':nodes,'Water Surface Elevation(m)':water_list,'Flow(m³/s)':flow_list,'Velocities(m/s)':veloc_list}
df=pd.DataFrame(output)
df.set_index('S.Transversais')

#SALVANDO PROJETO
RC.Project_Save()

#FECHANDO JANELA
RC.QuitRAS()




