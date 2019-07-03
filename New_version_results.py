# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 14:57:42 2019

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
bpi_MVID = pd.read_excel('Bradley_BPI_Three_Year_Active_Client_List.xlsx',sheet_name='Report 1',header=0)
bpi = bpi_MVID[['Reference Number','Finance Billing ID','Sold To','Practice Name']]
bpi = bpi.rename(index=str, columns={"Practice Name": "CLIENT_NAME_bpi", "Sold To": "SOLDTO_bpi", 
                                     "Finance Billing ID": "BILLING_ID_bpi", "Reference Number": "REFERENCE_NBR_bpi"})
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

### should not be matched but matched based on bpi
b_contract_vs_billing = pd.merge(bpi, fin, how='inner', left_on='REFERENCE_NBR_bpi', right_on='BILLINGID_fin')
b_contract_vs_soldto = pd.merge(bpi, fin, how='inner', left_on='REFERENCE_NBR_bpi', right_on='SOLDTO_fin')
b_billing_vs_soldto = pd.merge(bpi, fin, how='inner', left_on='BILLING_ID_bpi', right_on='SOLDTO_fin')

### join all the features together
fulltable_con = pd.merge(fin, ContractID_i, how='left', on=['SOLDTO_fin', 'CONTRACTID_fin', 'BILLINGID_fin', 'CLIENTNAME_fin'])
fulltable_bcb = pd.merge(fulltable_con, b_contract_vs_billing, how='left', on=['SOLDTO_fin', 'CONTRACTID_fin', 'BILLINGID_fin', 'CLIENTNAME_fin'])

### merge three columns into one
fulltable_bcb['SOLDTO_bpi_x'].fillna(fulltable_bcb['SOLDTO_bpi_y'], inplace = True)
fulltable_bcb = fulltable_bcb.drop('SOLDTO_bpi_y', axis=1)
fulltable_bcb['REFERENCE_NBR_bpi_x'].fillna(fulltable_bcb['REFERENCE_NBR_bpi_y'], inplace = True)
fulltable_bcb = fulltable_bcb.drop('REFERENCE_NBR_bpi_y', axis=1)
fulltable_bcb['BILLING_ID_bpi_x'].fillna(fulltable_bcb['BILLING_ID_bpi_y'], inplace = True)
fulltable_bcb = fulltable_bcb.drop('BILLING_ID_bpi_y', axis=1)
fulltable_bcb['CLIENT_NAME_bpi_x'].fillna(fulltable_bcb['CLIENT_NAME_bpi_y'], inplace = True)
fulltable_bcb = fulltable_bcb.drop('CLIENT_NAME_bpi_y', axis=1)

# join
fulltable_bcs = pd.merge(fulltable_bcb, b_contract_vs_soldto, how='left', on=['SOLDTO_fin', 'CONTRACTID_fin', 'BILLINGID_fin', 'CLIENTNAME_fin'])
fulltable_bbs = pd.merge(fulltable_bcs, b_billing_vs_soldto, how='left', on=['SOLDTO_fin', 'CONTRACTID_fin', 'BILLINGID_fin', 'CLIENTNAME_fin'])
fulltable_name = pd.merge(fulltable_bbs, name_i, how='left', on=['SOLDTO_fin', 'CONTRACTID_fin', 'BILLINGID_fin', 'CLIENTNAME_fin'])
### merge
fulltable_bcs['SOLDTO_bpi'].fillna(fulltable_bcs['SOLDTO_bpi_x'], inplace = True)
fulltable_bcs = fulltable_bcs.drop('SOLDTO_bpi_x', axis=1)
fulltable_bcs['REFERENCE_NBR_bpi'].fillna(fulltable_bcs['REFERENCE_NBR_bpi_x'], inplace = True)
fulltable_bcs = fulltable_bcs.drop('REFERENCE_NBR_bpi_x', axis=1)
fulltable_bcs['BILLING_ID_bpi'].fillna(fulltable_bcs['BILLING_ID_bpi_x'], inplace = True)
fulltable_bcs = fulltable_bcs.drop('BILLING_ID_bpi_x', axis=1)
fulltable_bcs['CLIENT_NAME_bpi'].fillna(fulltable_bcs['CLIENT_NAME_bpi_x'], inplace = True)
fulltable_bcs = fulltable_bcs.drop('CLIENT_NAME_bpi_x', axis=1)

# join
fulltable_bbs = pd.merge(fulltable_bcs, b_billing_vs_soldto, how='left', on=['SOLDTO_fin', 'CONTRACTID_fin', 'BILLINGID_fin', 'CLIENTNAME_fin'])
fulltable_name = pd.merge(fulltable_bbs, name_i, how='left', on=['SOLDTO_fin', 'CONTRACTID_fin', 'BILLINGID_fin', 'CLIENTNAME_fin'])

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
fulltable_fin.to_csv('New_version_full_table_fin.csv', encoding='utf-8')



