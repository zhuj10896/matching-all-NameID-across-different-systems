# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 14:09:00 2019

@author: jzhu
"""
### import packages
import pandas as pd
import numpy as np

### read the dataset and rename the colunms
fin_org = pd.read_excel('Client Identifiers.xlsx',sheet_name='Finance',header=0)
fin = fin_org.iloc[:,0:4]
fin = fin.rename(index=str, columns={"SOLDTO": "SOLDTO_fin", "CONTRACTID": "CONTRACTID_fin", 
                                     "BILLINGID": "BILLINGID_fin", "CLIENTNAME": "CLIENTNAME_fin"})
bpi = pd.read_excel('Client Identifiers.xlsx',sheet_name='BPI',header=0)
bpi = bpi.rename(index=str, columns={"CLIENT_NAME": "CLIENT_NAME_bpi", "SOLDTO": "SOLDTO_bpi", 
                                     "BILLING_ID": "BILLING_ID_bpi", "REFERENCE_NBR": "REFERENCE_NBR_bpi"})
bpi["SOLDTO_bpi"] = bpi["SOLDTO_bpi"].astype('Int32')
bpi["BILLING_ID_bpi"] = bpi["BILLING_ID_bpi"].astype('str')
fin["BILLINGID_fin"] = fin["BILLINGID_fin"].astype('str')

### find contract ID values, which are mathced with the other
ContractID_i = pd.merge(bpi, fin, how='inner', left_on='REFERENCE_NBR_bpi', right_on='CONTRACTID_fin')
### find billing_id values, which are mathced with the other
BillingID_i = pd.merge(bpi, fin, how='inner', left_on='BILLING_ID_bpi', right_on='BILLINGID_fin')
### find names, which are mathced with the other
name_i = pd.merge(bpi, fin, how='inner', left_on='CLIENT_NAME_bpi', right_on='CLIENTNAME_fin')
### find SOLDTO values, which are mathced with the other
Soldto_i = pd.merge(bpi, fin, how='inner', left_on='SOLDTO_bpi', right_on='SOLDTO_fin')  

### join all the features together
fulltable_con = pd.merge(fin, ContractID_i, how='left', on=['SOLDTO_fin', 'CONTRACTID_fin', 'BILLINGID_fin', 'CLIENTNAME_fin'])
fulltable_bill = pd.merge(fulltable_con, BillingID_i, how='left', on=['SOLDTO_fin', 'CONTRACTID_fin', 'BILLINGID_fin', 'CLIENTNAME_fin'])
fulltable_name = pd.merge(fulltable_bill, name_i, how='left', on=['SOLDTO_fin', 'CONTRACTID_fin', 'BILLINGID_fin', 'CLIENTNAME_fin'])

fulltable_name = fulltable_name[['SOLDTO_fin', 'SOLDTO_bpi', 'SOLDTO_bpi_x', 'SOLDTO_bpi_y',
                                 'CONTRACTID_fin', 'REFERENCE_NBR_bpi', 'REFERENCE_NBR_bpi_x', 'REFERENCE_NBR_bpi_y',
                                 'BILLINGID_fin', 'BILLING_ID_bpi', 'BILLING_ID_bpi_x', 'BILLING_ID_bpi_y',
                                 'CLIENTNAME_fin', 'CLIENT_NAME_bpi', 'CLIENT_NAME_bpi_x', 'CLIENT_NAME_bpi_y']]

### merge three columns into one
fulltable_name['SOLDTO_bpi'].fillna(fulltable_name['SOLDTO_bpi_x'], inplace = True)
fulltable_name['SOLDTO_bpi'].fillna(fulltable_name['SOLDTO_bpi_y'], inplace = True)
fulltable_name = fulltable_name.drop('SOLDTO_bpi_x', axis=1)
fulltable_name = fulltable_name.drop('SOLDTO_bpi_y', axis=1)

fulltable_name['REFERENCE_NBR_bpi'].fillna(fulltable_name['REFERENCE_NBR_bpi_x'], inplace = True)
fulltable_name['REFERENCE_NBR_bpi'].fillna(fulltable_name['REFERENCE_NBR_bpi_y'], inplace = True)
fulltable_name = fulltable_name.drop('REFERENCE_NBR_bpi_x', axis=1)
fulltable_name = fulltable_name.drop('REFERENCE_NBR_bpi_y', axis=1)

fulltable_name['BILLING_ID_bpi'].fillna(fulltable_name['BILLING_ID_bpi_x'], inplace = True)
fulltable_name['BILLING_ID_bpi'].fillna(fulltable_name['BILLING_ID_bpi_y'], inplace = True)
fulltable_name = fulltable_name.drop('BILLING_ID_bpi_x', axis=1)
fulltable_name = fulltable_name.drop('BILLING_ID_bpi_y', axis=1)

fulltable_name['CLIENT_NAME_bpi'].fillna(fulltable_name['CLIENT_NAME_bpi_x'], inplace = True)
fulltable_name['CLIENT_NAME_bpi'].fillna(fulltable_name['CLIENT_NAME_bpi_y'], inplace = True)
fulltable_name = fulltable_name.drop('CLIENT_NAME_bpi_x', axis=1)
fulltable_name = fulltable_name.drop('CLIENT_NAME_bpi_y', axis=1)

### fill nan with str
fulltable_name = fulltable_name.replace(np.nan, '', regex=True)

### conditions added
fulltable_name['soldto_fin = all_soldto_bpi'] = np.where(fulltable_name.SOLDTO_fin == fulltable_name.SOLDTO_bpi, True, False)
fulltable_name['contract_fin = all_contract_bpi'] = fulltable_name.apply(lambda x: x.CONTRACTID_fin == x.REFERENCE_NBR_bpi, axis=1)
fulltable_name['name_fin = all_name_bpi'] = fulltable_name.apply(lambda x: x['CLIENTNAME_fin'].strip().lower() in x['CLIENT_NAME_bpi'].strip().lower(), axis=1)
fulltable_name['billing_fin = all_billing_bpi'] = fulltable_name.apply(lambda x: x['BILLINGID_fin'].strip().lower() == x['BILLING_ID_bpi'].strip().lower(), axis=1)

fulltable_name = fulltable_name[['SOLDTO_fin', 'SOLDTO_bpi', 'soldto_fin = all_soldto_bpi',
                                 'CONTRACTID_fin', 'REFERENCE_NBR_bpi', 'contract_fin = all_contract_bpi',
                                 'BILLINGID_fin', 'BILLING_ID_bpi', 'billing_fin = all_billing_bpi',
                                 'CLIENTNAME_fin', 'CLIENT_NAME_bpi','name_fin = all_name_bpi']]

### save the table
fulltable_fin = fulltable_name
fulltable_fin.to_csv('full_table_fin.csv', encoding='utf-8')
