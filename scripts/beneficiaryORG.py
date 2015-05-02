import os
import csv
import pandas as pd
import numpy as np

file_list = []

def getFiles():
        for i in os.listdir('/home/cusp/kl1771/cms_files/'):
                if 'Beneficiary_Summary_File' in i:
                        file_list.append(i)
                else:
                        pass

        return file_list

def mergePatients(list):
        index = 0
        for file in list:
                if index == 0:
                        df_temp1 = pd.read_csv(list[index])
                        index += 1
                elif index == 1:
                        df_temp2 = pd.read_csv(list[index])
                        df = pd.concat([df_temp1, df_temp2])
                        index += 1
                else:
                        df_add = pd.read_csv(list[index])
                        df = pd.concat([df, df_add])
                        index += 1 
        return df

def compoundPatients(df):
        col_diag = ['SP_ALZHDMTA', 'SP_CHF', 'SP_CHRNKIDN', 'SP_CNCR', 'SP_COPD', 'SP_DEPRESSN', 'SP_DIABETES', 'SP_ISCHMCHT', 'SP_OSTEOPRS', 'SP_RA_OA', 'SP_STRKETIA']
        df_grouped = df.groupby(['DESYNPUF_ID'])[col_diag]
        df_agg = df_grouped.agg('median')
        df_agg.to_csv("beneficiary.csv") 

#f = {'SP_ALZHDMTA':['median'], 'SP_CHF': ['median'], 'SP_CHRNKIDN': ['median'], 'SP_CNCR': ['median'], 'SP_COPD': ['median'], 'SP_DEPRESSN': ['median'], 'SP_DIABETES': ['median'], 'SP_ISCHMCHT': ['median'], 'SP_OSTEOPRS': ['median'], 'SP_RA_OA': ['median'], 'SP_STRKETIA': ['median'], 'MEDREIMB_IP': ['sum'], 'MEDREIMB_OP': ['sum']}

        #df_ben_grouped = pd.DataFrame(df.groupby(['DESYNPUF_ID']).agg(f))
        #df_ben_grouped.columns = df_ben_grouped.columns.droplevel(1)
        #df_ben_grouped = df_ben_grouped[col_diag]
        #print df_ben_grouped
        #df_ben_grouped['percentile']  = pd.cut(df_ben_grouped['MEDREIMB_OP'] + df_ben_grouped['MEDREIMB_IP'], 100).labels
        #pd.DataFrame(df_ben_grouped).to_csv("testfile.csv")

if __name__=='__main__':
        files = getFiles()
        df = mergePatients(files)
        compoundPatients(df)
