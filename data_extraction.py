import pandas as pd
import json
import os
import git
def clone_repo():
    try:
        git.Repo.clone_from('https://github.com/PhonePe/pulse.git', 'pulse')
    except:
        print('Error occured while cloning repository')

#Aggregate Transaction
def aggregate_transaction():
    path="pulse/data/aggregated/transaction/country/india/state/"
    Agg_transaction_state_list=os.listdir(path)

    clm={'State':[], 'Year':[],'Quarter':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}
    for i in Agg_transaction_state_list:
        p_i=path+i+"/"
        Agg_yr=os.listdir(p_i)
        for j in Agg_yr:
            p_j=p_i+j+"/"
            Agg_yr_list=os.listdir(p_j)
            for k in Agg_yr_list:
                p_k=p_j+k
                Data=open(p_k,'r')
                D=json.load(Data)
                for z in D['data']['transactionData']:
                    Name=z['name']
                    count=z['paymentInstruments'][0]['count']
                    amount=z['paymentInstruments'][0]['amount']
                    clm['Transaction_type'].append(Name)
                    clm['Transaction_count'].append(count)
                    clm['Transaction_amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))

    Agg_Trans=pd.DataFrame(clm)
    return Agg_Trans

#Aggregate Users
def aggregate_users():
    path="pulse/data/aggregated/user/country/india/state/"
    Agg_user_state_list=os.listdir(path)

    clm={'State':[], 'Year':[],'Quarter':[],'Registered_Users':[], 'App_Opens':[]}
    for i in Agg_user_state_list:
        p_i=path+i+"/"
        Agg_yr=os.listdir(p_i)
        for j in Agg_yr:
            p_j=p_i+j+"/"
            Agg_yr_list=os.listdir(p_j)
            for k in Agg_yr_list:
                p_k=p_j+k
                Data=open(p_k,'r')
                D=json.load(Data)
                count=D['data']['aggregated']['registeredUsers']
                app_opens=D['data']['aggregated']['appOpens']
                clm['Registered_Users'].append(count)
                clm['App_Opens'].append(app_opens)
                clm['State'].append(i)
                clm['Year'].append(j)
                clm['Quarter'].append(int(k.strip('.json')))

    Agg_Users=pd.DataFrame(clm)
    return Agg_Users

#Map Transaction
def map_transaction():
    path="pulse/data/map/transaction/hover/country/india/state/"
    Map_transaction_state_list=os.listdir(path)

    clm={'State':[], 'Year':[],'Quarter':[],'District':[], 'Transaction_count':[], 'Transaction_amount':[]}
    for i in Map_transaction_state_list:
        p_i=path+i+"/"
        Agg_yr=os.listdir(p_i)
        for j in Agg_yr:
            p_j=p_i+j+"/"
            Agg_yr_list=os.listdir(p_j)
            for k in Agg_yr_list:
                p_k=p_j+k
                Data=open(p_k,'r')
                D=json.load(Data)
                for z in D['data']['hoverDataList']:
                    district=z['name']
                    count=z['metric'][0]['count']
                    amount=z['metric'][0]['amount']
                    clm['District'].append(district)
                    clm['Transaction_count'].append(count)
                    clm['Transaction_amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))

    Map_Trans=pd.DataFrame(clm)
    return Map_Trans

#Map Users
def map_users():
    path="pulse/data/map/user/hover/country/india/state/"
    Map_user_state_list=os.listdir(path)

    clm={'State':[], 'Year':[],'Quarter':[],'District':[], 'Registered_Users':[], 'App_Opens':[]}
    for i in Map_user_state_list:
        p_i=path+i+"/"
        Agg_yr=os.listdir(p_i)
        for j in Agg_yr:
            p_j=p_i+j+"/"
            Agg_yr_list=os.listdir(p_j)
            for k in Agg_yr_list:
                p_k=p_j+k
                Data=open(p_k,'r')
                D=json.load(Data)
                for z in D['data']['hoverData'].items():
                    district=z[0]
                    reg_users=z[1]['registeredUsers']
                    app_opens=z[1]['appOpens']
                    clm['District'].append(district)
                    clm['Registered_Users'].append(reg_users)
                    clm['App_Opens'].append(app_opens)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))

    Map_Users=pd.DataFrame(clm)
    return Map_Users

#Top Transaction by District
def top_transaction_district():
    path="pulse/data/top/transaction/country/india/state/"
    Top_Transaction_state_District_list=os.listdir(path)

    clm={'State':[], 'Year':[],'Quarter':[],'District':[], 'Transaction_Count':[],'Transaction_Amount':[]}
    for i in Top_Transaction_state_District_list:
        p_i=path+i+"/"    
        Agg_yr=os.listdir(p_i)
        for j in Agg_yr:
            p_j=p_i+j+"/"
            Agg_yr_list=os.listdir(p_j)
            for k in Agg_yr_list:
                p_k=p_j+k
                Data=open(p_k,'r')
                D=json.load(Data)
                for z in D['data']['districts']:
                    district=z['entityName']
                    count=z['metric']['count']
                    amount=z['metric']['amount']
                    clm['District'].append(district)
                    clm['Transaction_Count'].append(count)
                    clm['Transaction_Amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))

    Top_Transaction_by_district=pd.DataFrame(clm)
    return Top_Transaction_by_district


#Top Transaction by Pincode
def top_transaction_pincode():
    path="pulse/data/top/transaction/country/india/state/"
    Top_Transaction_state_District_list=os.listdir(path)

    clm={'State':[], 'Year':[],'Quarter':[],'Pincode':[], 'Transaction_Count':[],'Transaction_Amount':[]}
    for i in Top_Transaction_state_District_list:
        p_i=path+i+"/"    
        Agg_yr=os.listdir(p_i)
        for j in Agg_yr:
            p_j=p_i+j+"/"
            Agg_yr_list=os.listdir(p_j)
            for k in Agg_yr_list:
                p_k=p_j+k
                Data=open(p_k,'r')
                D=json.load(Data)
                for z in D['data']['pincodes']:
                    pincode=z['entityName']
                    count=z['metric']['count']
                    amount=z['metric']['amount']
                    clm['Pincode'].append(pincode)
                    clm['Transaction_Count'].append(count)
                    clm['Transaction_Amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))

    Top_Transaction_by_pincode=pd.DataFrame(clm)
    return Top_Transaction_by_pincode


#Top Users by District
def top_users_district():
    path="pulse/data/top/user/country/india/state/"
    Top_User_state_District_list=os.listdir(path)

    clm={'State':[], 'Year':[],'Quarter':[],'District':[], 'Registered_Users':[]}
    for i in Top_User_state_District_list:
        p_i=path+i+"/"    
        Agg_yr=os.listdir(p_i)
        for j in Agg_yr:
            p_j=p_i+j+"/"
            Agg_yr_list=os.listdir(p_j)
            for k in Agg_yr_list:
                p_k=p_j+k
                Data=open(p_k,'r')
                D=json.load(Data)
                for z in D['data']['districts']:
                    district=z['name']
                    reg_users=z['registeredUsers']
                    clm['District'].append(district)
                    clm['Registered_Users'].append(reg_users)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))

    Top_Users_by_district=pd.DataFrame(clm)
    return Top_Users_by_district

#Top Users by Pincode
def top_users_pincode():
    path="pulse/data/top/user/country/india/state/"
    Top_User_state_Pincode_list=os.listdir(path)

    clm={'State':[], 'Year':[],'Quarter':[],'Pincode':[], 'Registered_Users':[]}
    for i in Top_User_state_Pincode_list:
        p_i=path+i+"/"    
        Agg_yr=os.listdir(p_i)
        for j in Agg_yr:
            p_j=p_i+j+"/"
            Agg_yr_list=os.listdir(p_j)
            for k in Agg_yr_list:
                p_k=p_j+k
                Data=open(p_k,'r')
                D=json.load(Data)
                for z in D['data']['pincodes']:
                    pincode=z['name']
                    reg_users=z['registeredUsers']
                    clm['Pincode'].append(pincode)
                    clm['Registered_Users'].append(reg_users)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))

    Top_Users_by_pincode=pd.DataFrame(clm)
    return Top_Users_by_pincode 



