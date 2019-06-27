# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 13:43:20 2019

@author: jzhu
"""
### import packages
import pandas as pd

### read the dataset and rename the colunms
fin_org = pd.read_excel('Client Identifiers.xlsx',sheet_name='Finance',header=0)
fin = fin_org.iloc[:,0:4]
fin = fin.rename(index=str, columns={"SOLDTO": "SOLDTO_fin", "CONTRACTID": "CONTRACTID_fin", 
                                     "BILLINGID": "BILLINGID_fin", "CLIENTNAME": "CLIENTNAME_fin"})
bpi = pd.read_excel('Client Identifiers.xlsx',sheet_name='BPI',header=0)
bpi = bpi.rename(index=str, columns={"CLIENT_NAME": "CLIENT_NAME_bpi", "SOLDTO": "SOLDTO_bpi", 
                                     "BILLING_ID": "BILLING_ID_bpi", "REFERENCE_NBR": "REFERENCE_NBR_bpi"})
bpi["SOLDTO_bpi"] = bpi["SOLDTO_bpi"].astype('Int32')
### check the data type
fin.dtypes
bpi.dtypes

### check each features in two tables
u_billing_bpi = list(bpi.BILLING_ID_bpi.unique())
u_billing_fin = list(fin.BILLINGID_fin.unique())

u_soldto_bpi = list(bpi.SOLDTO_bpi.unique())
u_soldto_fin = list(fin.SOLDTO_fin.unique())

u_name_bpi = list(bpi.CLIENT_NAME_bpi.unique())
u_name_fin = list(fin.CLIENTNAME_fin.unique())

u_contract_bpi = list(bpi.REFERENCE_NBR_bpi.unique())
u_contract_fin = list(fin.CONTRACTID_fin.unique())

### general rules to follow for Contract_ID and SOLDTO:
# if contractID is 7 digits number or contractID is equal to the SOLDTO, it could be wrong in fin.
u_contract_num_bpi = []
for i in u_contract_bpi:
    if type(i) == int:
        u_contract_num_bpi.append(i)
    else:
        continue

u_contract_num_fin = []
for x in u_contract_fin:
    if type(x) == int and x > 99999:
        u_contract_num_fin.append(x)
    else:
        continue  
## u_contract_bpi_str = list(map(str, u_contract_bpi)) in case, need to change data type      
#if soldto is not all numbers, it could be wrong.
u_soldto_num_bpi = []
for j in u_soldto_bpi:
    if type(j) == str:
        u_soldto_num_bpi.append(j)
    else:
        continue

u_soldto_num_fin = []
for t in u_soldto_fin:
    if type(t) == str:
        u_soldto_num_fin.append(t)
    else:
        continue
    
### merge the two tables, which will show perfect matching values(all four features are matched)
perfect_value = fin.merge(bpi.rename(columns={'REFERENCE_NBR_bpi':'CONTRACTID_fin','BILLING_ID_bpi':'BILLINGID_fin',
                                              'CLIENT_NAME_bpi':'CLIENTNAME_fin', 'SOLDTO_bpi': 'SOLDTO_fin'}),how='inner')
### find contract ID values, which are mathced with the other
ContractID_i = pd.merge(bpi, fin, how='inner', left_on='REFERENCE_NBR_bpi', right_on='CONTRACTID_fin')
### find billing_id values, which are mathced with the other
BillingID_i = pd.merge(bpi, fin, how='inner', left_on='BILLING_ID_bpi', right_on='BILLINGID_fin')
### find names, which are mathced with the other
name_i = pd.merge(bpi, fin, how='inner', left_on='CLIENT_NAME_bpi', right_on='CLIENTNAME_fin')
### find SOLDTO values, which are mathced with the other
Soldto_i = pd.merge(bpi, fin, how='inner', left_on='SOLDTO_bpi', right_on='SOLDTO_fin')  


### find Two : contract ID and billing_id values, which are mathced with the other
Contract_and_Billing_i = pd.merge(bpi, fin, how='inner', left_on=['REFERENCE_NBR_bpi','BILLING_ID_bpi'], right_on=['CONTRACTID_fin','BILLINGID_fin'])
### find Two : contract ID and names, which are mathced with the other
Contract_and_name_i = pd.merge(bpi, fin, how='inner', left_on=['REFERENCE_NBR_bpi','CLIENT_NAME_bpi'], right_on=['CONTRACTID_fin','CLIENTNAME_fin'])
### find Two : contract ID and soldtoID, which are mathced with the other
Contract_and_soldto_i = pd.merge(bpi, fin, how='inner', left_on=['REFERENCE_NBR_bpi','SOLDTO_bpi'], right_on=['CONTRACTID_fin','SOLDTO_fin'])
### find Two : billing ID and names, which are mathced with the other
Billing_and_name_i = pd.merge(bpi, fin, how='inner', left_on=['BILLING_ID_bpi','CLIENT_NAME_bpi'], right_on=['BILLINGID_fin','CLIENTNAME_fin'])
### find Two : billing ID and soldtoid, which are mathced with the other
Billing_and_soldto_i = pd.merge(bpi, fin, how='inner', left_on=['BILLING_ID_bpi','SOLDTO_bpi'], right_on=['BILLINGID_fin','SOLDTO_fin'])
### find Two : names and soldtoid, which are mathced with the other
Name_and_soldto_i = pd.merge(bpi, fin, how='inner', left_on=['SOLDTO_bpi','CLIENT_NAME_bpi'], right_on=['SOLDTO_fin','CLIENTNAME_fin'])


### find Three : contract ID and billing_id values and names, which are mathced with the other
Contract_billing_name_i = pd.merge(bpi, fin, how='inner', left_on=['REFERENCE_NBR_bpi','BILLING_ID_bpi','CLIENT_NAME_bpi'],
                                   right_on=['CONTRACTID_fin','BILLINGID_fin','CLIENTNAME_fin'])
### find Three : contract ID and billing_id values and soldto, which are mathced with the other
Contract_billing_soldto_i = pd.merge(bpi, fin, how='inner', left_on=['REFERENCE_NBR_bpi','BILLING_ID_bpi','SOLDTO_bpi'],
                                   right_on=['CONTRACTID_fin','BILLINGID_fin','SOLDTO_fin'])
### find Three : contract ID and soldto and names, which are mathced with the other
Contract_name_soldto_i = pd.merge(bpi, fin, how='inner', left_on=['REFERENCE_NBR_bpi','REFERENCE_NBR_bpi','SOLDTO_bpi'],
                                   right_on=['CONTRACTID_fin','CLIENTNAME_fin','SOLDTO_fin'])
### find Three : soldto and names and billingID, which are mathced with the other
Soldto_billing_name_i = pd.merge(bpi, fin, how='inner', left_on=['SOLDTO_bpi','BILLING_ID_bpi','CLIENT_NAME_bpi'],
                                   right_on=['SOLDTO_fin','BILLINGID_fin','CLIENTNAME_fin'])

### diff in contractID, billingID, nameID, and Soldto
diff_in_contract_bpi = bpi[~bpi[['REFERENCE_NBR_bpi']].apply(tuple,1).isin(ContractID_i[['REFERENCE_NBR_bpi']].apply(tuple,1))]
diff_in_contract_fin = fin[~fin[['CONTRACTID_fin']].apply(tuple,1).isin(ContractID_i[['REFERENCE_NBR_bpi']].apply(tuple,1))]
diff_in_Billing = ContractID_i[~ContractID_i[['BILLING_ID_bpi','REFERENCE_NBR_bpi']].apply(tuple,1).isin(Contract_and_Billing_i[['BILLINGID_fin','CONTRACTID_fin']].apply(tuple,1))]
diff_in_name = ContractID_i[~ContractID_i[['CLIENT_NAME_bpi','REFERENCE_NBR_bpi']].apply(tuple,1).isin(Contract_and_name_i[['CLIENTNAME_fin','CONTRACTID_fin']].apply(tuple,1))]
diff_in_soldto = ContractID_i[~ContractID_i[['REFERENCE_NBR_bpi','SOLDTO_bpi']].apply(tuple,1).isin(Contract_and_soldto_i[['CONTRACTID_fin','SOLDTO_fin']].apply(tuple,1))]
### testing --- make sure without any big mistakes
diff_test = ContractID_i.merge(Contract_and_soldto_i.drop_duplicates(), on=['REFERENCE_NBR_bpi','SOLDTO_bpi'], how='left', indicator=True)
diff_in_soldto_test = diff_test[diff_test['_merge'] == 'left_only']

### switch the rows, which is easy to have a quick look --- ContractID
diff_in_contract_fin_proc = diff_in_contract_fin[diff_in_contract_fin["CONTRACTID_fin"].isin(u_contract_num_fin)]
diff_in_contract_fin_final = pd.merge(diff_in_contract_fin_proc, bpi, how='inner', left_on=['SOLDTO_fin'], right_on=['SOLDTO_bpi'])
diff_in_contract_fin_final = diff_in_contract_fin_final[['REFERENCE_NBR_bpi', 'CONTRACTID_fin','SOLDTO_fin', 
                                                         'SOLDTO_bpi', 'BILLINGID_fin', 
                                                         'BILLING_ID_bpi', 'CLIENTNAME_fin', 
                                                         'CLIENT_NAME_bpi']]
# save it diff_in_contract_fin_final.to_csv('diff_in_contractID_finance.csv', encoding='utf-8')
### switch the rows, which is easy to have a quick look --- Soldto
diff_in_soldto_final = diff_in_soldto.iloc[:,0:8]
diff_in_soldto_final = diff_in_soldto_final[
        ['SOLDTO_bpi','SOLDTO_fin','CLIENT_NAME_bpi',
        'CLIENTNAME_fin','REFERENCE_NBR_bpi',  'CONTRACTID_fin',
       'BILLING_ID_bpi','BILLINGID_fin']]

# save it diff_in_soldto_final.to_csv('diff_in_soldto_finance.csv', encoding='utf-8')
### general rules to follow for Billing_ID:
# if billing_ID has '-', it may not be not right in bpi.
bpi['T/F'] = bpi['BILLING_ID_bpi'].str.contains(r'\-','True')
diff_in_billing_bpi_dash = bpi[bpi['T/F'] == True]
# if billing_ID is eaqual to SOLDTO, it could be wrong in bpi
bpi['billing=soldto'] = bpi.apply(lambda x: x.BILLING_ID_bpi == x.SOLDTO_bpi, axis=1)
diff_in_billing_bpi_bands = bpi[bpi['billing=soldto'] == True]
# if billing_ID is equal to Contract_ID, it could be wrong in bpi
bpi['billing=contractid'] = bpi.apply(lambda x: x.BILLING_ID_bpi == x.REFERENCE_NBR_bpi, axis=1)
diff_in_billing_bpi_bandc = bpi[bpi['billing=contractid'] == True]
# if billing_ID is equal to Clientname, it could be wrong in bpi
bpi['billing=clientname'] = bpi.apply(lambda x: x.BILLING_ID_bpi == x.CLIENT_NAME_bpi, axis=1)
diff_in_billing_bpi_bandn = bpi[bpi['billing=clientname'] == True]
# if billing_ID is equal to SOLDTO or Client name, it may be wrong in fin table
fin['billing=soldto'] = fin.apply(lambda x: x.BILLINGID_fin == x.SOLDTO_fin, axis=1)
diff_in_billing_fin_bands = fin[fin['billing=soldto'] == True]
fin['billing=clientname'] = fin.apply(lambda x: x.BILLINGID_fin == x.CLIENTNAME_fin, axis=1)
diff_in_billing_fin_bandn = fin[fin['billing=clientname'] == True]
# save it diff_in_billing_bpi_dash.to_csv('BillingIDwithdash_bpi.csv', encoding='utf-8')
# save it diff_in_billing_bpi_bands.to_csv('BillingID_SOLDTO_same_bpi.csv', encoding='utf-8')
# save it diff_in_billing_bpi_bandc.to_csv('BillingID_CONTRACTID_same_bpi.csv', encoding='utf-8')
# save it diff_in_billing_bpi_bandn.to_csv('BillingID_clientname_same_bpi.csv', encoding='utf-8')
# save it diff_in_billing_fin_bands.to_csv('BillingID_CONTRACTID_same_finance.csv', encoding='utf-8')
# save it diff_in_billing_fin_bandn.to_csv('BillingID_clientname_same_finance.csv', encoding='utf-8')
# if billing_ID is start with RMS or equal to ContractID, it could be wrong in fin.
# if billing_ID is a word such as SpecCare (specialty Care), it could be wrong in fin table


















































