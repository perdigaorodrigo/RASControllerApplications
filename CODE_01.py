# -*- coding: utf-8 -*-
#Executando Simulação Básica com HEC-RASController
"""
Created on Tue Feb  2 22:12:05 2021

@author: Rodrigo
"""
#IMPORTANDO BIBLIOTECA
import win32com.client

#ATRIBUINDO FUNCOES DO HECRASCONTROLLER AO OBJETO RC
RC=win32com.client.Dispatch("RAS507.HECRASCONTROLLER")

#ABRINDO E FECHANDO JANELA
RC.ShowRAS()

RC.QuitRAS()

#ABRINDO PROJETO
RC.Project_Open(r"C:\Users\Rodrigo\Desktop\HECRAS\DADOS\RAS\1D_MODEL.prj")

#EXECUTANDO SIMULACAO DO PLANO ATUAL
Simulacao=RC.Compute_CurrentPlan(None,None,True)

#SALVANDO PROJETO
RC.Project_Save()

#FECHANDO JANELA
RC.QuitRAS()





