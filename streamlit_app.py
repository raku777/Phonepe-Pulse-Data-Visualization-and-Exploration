import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import mysql.connector as sql
import json
import requests


def change_state_name():
     url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
     response = requests.get(url)
     data = json.loads(response.content)
     state_name = [i['properties']['ST_NM'] for i in data['features']]
     state_name.sort()
     return state_name

#Function to convert columns to numerical datatype
def convert_numerical_dt(df,column_names):
    for column in column_names:
        df[column_names]= pd.to_numeric(df[column_names],errors='coerce')
    return df

# Function to fetch data from MySQL
def fetch_data(query,year,quarter):
    my_db = sql.connect(host='localhost', user='root', password='raku#123', database='phonepe_pulse')
    cursor = my_db.cursor()
    cursor.execute(query,(year,quarter))
    column_names = [i[0] for i in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=column_names)
    cursor.close()
    my_db.close()
    return df

def fetch_data_by_state(query,state,year,quarter):
    my_db = sql.connect(host='localhost', user='root', password='raku#123', database='phonepe_pulse')
    cursor = my_db.cursor()
    cursor.execute(query,(state,year,quarter))
    column_names = [i[0] for i in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=column_names)
    cursor.close()
    my_db.close()
    return df

class AddUnit:
    def millions(transaction):
        num = transaction
        num = float(num)/1000000
        num = '{:.2f}'.format(num)
        n = str(num) + ' Million'
        return n

    def billions(transaction):
        num = transaction
        num = float(num)/1000000000
        num = '{:.2f}'.format(num)
        n = str(num) + ' Billion'
        return n

    def trillions(transaction):
        num = transaction
        num = float(num)/1000000000000
        num = '{:.2f}'.format(num)
        n = str(num) + ' Trillion'
        return n
    
    def unit(transaction):
        num = str(transaction)
        if len(num) <= 6:
            return num
        elif 7 <= len(num) <= 9:
            return AddUnit.millions(num)
        elif 10 <= len(num) <= 12:
            return AddUnit.billions(num)
        elif len(num) >= 13:
            return AddUnit.trillions(num)

def geo_map(data,color_column,user_input,title):
        fig = px.choropleth_mapbox(data,
                            geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',  
                            featureidkey='properties.ST_NM',  
                            locations='state',
                            color=color_column,
                            hover_data= ['state',color_column,user_input],
                            color_continuous_scale='Viridis',
                            mapbox_style="carto-positron",
                            center={"lat": 20.5937, "lon": 78.9629},
                            zoom=3,
                            opacity=0.5,
                            title=title,
                            height=1000,
                            width= 1000,
                            )
        fig.update_geos(fitbounds='locations', visible=False)
        st.plotly_chart(fig, use_container_width=True)

st.set_page_config(layout="wide")
SELECT = option_menu(
    menu_title = None,
    options = ["Explore Data","Insights"],
    icons =["map","bar-chart"],                
    default_index=0,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100%"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}})

if SELECT=='Explore Data':
    # Sidebar with dropdown options
    st.sidebar.title('Select Options')
    options = st.sidebar.selectbox('Choose an option', ['Aggregate Transaction', 'Aggregate Users'])
    year = st.sidebar.slider('Choose a year',2018,2023)
    quarter = st.sidebar.slider('Choose a quarter',1,4)
    # Main content area
    st.title('PhonePe Pulse Dashboard')

    # Display data based on user selection
    if options == 'Aggregate Transaction':
        st.header('Aggregate Transaction Data')
        query = """select state, `year`,`quarter`,sum(transaction_amount) as transaction_amount ,sum(transaction_count) as transaction_count from aggregate_transaction
            where year = %s and quarter = %s group by year, quarter, state order by state asc"""
        df = fetch_data(query,year,quarter)
        
        state_name = change_state_name()
        for i in range(len(df.loc[:,'state'])):
            df['state'][i] = state_name[i]
        # df = convert_numerical_dt(df,'transaction_count')
        df['transaction_count']= df['transaction_count'].apply(lambda x: AddUnit.unit(x))

        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            geo_map(df,'transaction_amount','transaction_count','Aggregate Transaction Amount on India Map')
        with col2:
            st.title(' Transaction ')
            query1 = """select sum(transaction_count) as 'All PhonePe Transaction',sum(transaction_amount) as 'Total Payment Value',
                        sum(transaction_amount)/sum(transaction_count) as 'Avg Transaction Value' from aggregate_transaction
                        where year=%s and quarter=%s"""
            query2 = """select transaction_type as'Transaction Type',sum(transaction_amount) as 'Transaction Amount',sum(transaction_count) as 'Transaction Count',
                        sum(transaction_amount)/sum(transaction_count) as 'Average Value Per Transaction'
                        from aggregate_transaction where year = %s and quarter = %s
                        group by transaction_type order by 'Transaction Amount' desc""" 
            df1 = fetch_data(query1,year,quarter)
            st.header('All PhonePe transactions (UPI + Cards + Wallets)')
            st.subheader(AddUnit.unit(df1['All PhonePe Transaction'][0])) 
            st.header('Total Payment Value in Rs')
            st.subheader(AddUnit.unit(round(df1['Total Payment Value'][0])))
            st.header('Avg Transaction Value in Rs')
            st.subheader(round(df1['Avg Transaction Value'][0]))
            st.divider()
            df2 = fetch_data(query2,year,quarter)
            df2['Transaction Amount']=df2['Transaction Amount'].apply(lambda x:AddUnit.unit(round(x)))
            df2['Transaction Count']=df2['Transaction Count'].apply(lambda x:AddUnit.unit(round(x)))
            df2['Average Value Per Transaction']=round(df2['Average Value Per Transaction'])
            st.dataframe(df2,hide_index=1)


    elif options == 'Aggregate Users':
        st.header('Aggregate Users Data')
        query = """select state, `year`,`quarter`,sum(registered_users) as 'Registered Users',sum(app_opens) as 'App Opens'
                from aggregate_users where year=%s and quarter=%s
                group by state, year,quarter"""
        df = fetch_data(query,year,quarter)
        state_name = change_state_name()
        for i in range(len(df.loc[:,'state'])):
            df['state'][i] = state_name[i]
        df = convert_numerical_dt(df,'Registered Users')
        df['App Opens']= df['App Opens'].apply(lambda x: AddUnit.unit(x))
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            geo_map(df,'Registered Users','App Opens','Aggregate Users Count on India Map')
        with col2:
            st.title(' Users ')
            query1="""select sum(registered_users) as 'Registered Users',sum(app_opens) as 'App Opens'
                    from aggregate_users where year=%s and quarter=%s"""
            df1 = fetch_data(query1,year,quarter)
            st.header(f'Registered PhonePe users till Q{quarter} {year} ')
            st.subheader(AddUnit.unit(df1['Registered Users'][0])) 
            st.header(f'PhonePe app opens in Q{quarter} {year}')
            if df1['App Opens'][0]==0:
                st.header('Unavailable')
            else:
                st.subheader(AddUnit.unit(df1['App Opens'][0]))
            st.divider()
            tab1, tab2, tab3 = st.tabs(['State', 'District', 'Pincode'])
            with tab1:
                query2="""select state,sum(registered_users) as 'Registered Users',sum(app_opens) as 'App Opens', sum(app_opens)/sum(registered_users) as 'Avg App Open by User Per Quarter'
                    from aggregate_users where year=%s and quarter=%s group by state,year,quarter order by sum(registered_users) desc limit 10"""
                df2 = fetch_data(query2,year,quarter)
                df2['Registered Users']=df2['Registered Users'].apply(lambda x:AddUnit.unit(x))
                df2['App Opens']=df2['App Opens'].apply(lambda x:AddUnit.unit(x))
                df2 = convert_numerical_dt(df2,'Avg App Open by User Per Quarter')
                df2['Avg App Open by User Per Quarter']=round(df2['Avg App Open by User Per Quarter'])
                st.dataframe(df2,hide_index=1)
                with st.expander('See Explanation'):
                    st.write('Data not available for App Opens for year 2018 and for Q1 of 2019')
            with tab2:
                query3="""select district,sum(registered_users) as 'Registered Users' from top_users_district where year=%s and quarter=%s
                        group by year,quarter,district order by sum(registered_users) desc limit 10"""
                df3=fetch_data(query3,year,quarter)
                df3['Registered Users']=df3['Registered Users'].apply(lambda x:AddUnit.unit(x))
                st.dataframe(df3,hide_index=1)
            with tab3:
                query4="""select pincode,sum(registered_users) as 'Registered Users' from top_users_pincode where year=%s and quarter=%s
                        group by year,quarter,pincode order by sum(registered_users) desc limit 10"""
                df4=fetch_data(query4,year,quarter)
                st.dataframe(df4,hide_index=1)

if SELECT== 'Insights':
    options=st.selectbox('Choose an option',['Top 10 Districts by Transaction Amount of each State',
                                             'Top 10 Districts by Transaction Count of each State',
                                             'Top 10 Pincodes by Transaction Amount of each State',
                                             'Top 10 Pincodes by Transaction Count of each State',
                                             'Transaction Amount of each Transaction Type of each State',
                                             'Transaction Count of each Transaction Type of each State',
                                             'Top 10 Districts by Registered Users of each State',
                                             'Top 10 Pincodes by Registered Users of each State'])
    if options=='Top 10 Districts by Transaction Amount of each State':
        col1,col2,col3= st.columns([0.3,0.3,0.3])
        with col1:
            state=st.selectbox('Select a State or Union Territory',['andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam',
                                'bihar','chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep','madhya-pradesh',
                                'maharashtra','manipur','meghalaya','mizoram','nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'])
        with col2:
            year=st.selectbox('Select a Year',[2018,2019,2020,2021,2022,2023])
        with col3:
            quarter=st.selectbox('Select a Quarter',[1,2,3,4])
        query="""select state,`year`,`quarter`,district as 'District',transaction_amount as 'Transaction Amount' from top_transaction_district
                    where state=%s and year=%s and quarter=%s order by transaction_amount"""
        df=fetch_data_by_state(query,state,year,quarter)
        fig=px.bar(df,x='District',y='Transaction Amount',color='Transaction Amount',color_continuous_scale='ylorrd')
        st.plotly_chart(fig,use_container_width=True)

    elif options=='Top 10 Districts by Transaction Count of each State':
        col1,col2,col3= st.columns([0.3,0.3,0.3])
        with col1:
            state=st.selectbox('Select a State or Union Territory',['andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam',
                                'bihar','chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep','madhya-pradesh',
                                'maharashtra','manipur','meghalaya','mizoram','nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'])
        with col2:
            year=st.selectbox('Select a Year',[2018,2019,2020,2021,2022,2023])
        with col3:
            quarter=st.selectbox('Select a Quarter',[1,2,3,4])
        query="""select state,`year`,`quarter`,district as 'District',transaction_count as 'Transaction Count' from top_transaction_district
                    where state=%s and year=%s and quarter=%s order by transaction_count"""
        df=fetch_data_by_state(query,state,year,quarter)
        fig=px.bar(df,x='District',y='Transaction Count',color='Transaction Count',color_continuous_scale='ylorrd')
        st.plotly_chart(fig,use_container_width=True)

    elif options=='Top 10 Pincodes by Transaction Amount of each State':
        col1,col2,col3= st.columns([0.3,0.3,0.3])
        with col1:
            state=st.selectbox('Select a State or Union Territory',['andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam',
                                'bihar','chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep','madhya-pradesh',
                                'maharashtra','manipur','meghalaya','mizoram','nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'])
        with col2:
            year=st.selectbox('Select a Year',[2018,2019,2020,2021,2022,2023])
        with col3:
            quarter=st.selectbox('Select a Quarter',[1,2,3,4])
        query="""select state,`year`,`quarter`,pincode as 'Pincode',transaction_amount as 'Transaction Amount' from top_transaction_pincode
                    where state=%s and year=%s and quarter=%s order by transaction_amount"""
        df=fetch_data_by_state(query,state,year,quarter)
        st.bar_chart(df,x='Pincode',y='Transaction Amount',use_container_width=True)
    
    elif options=='Top 10 Pincodes by Transaction Count of each State':
        col1,col2,col3= st.columns([0.3,0.3,0.3])
        with col1:
            state=st.selectbox('Select a State or Union Territory',['andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam',
                                'bihar','chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep','madhya-pradesh',
                                'maharashtra','manipur','meghalaya','mizoram','nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'])
        with col2:
            year=st.selectbox('Select a Year',[2018,2019,2020,2021,2022,2023])
        with col3:
            quarter=st.selectbox('Select a Quarter',[1,2,3,4])
        query="""select state,`year`,`quarter`,pincode as 'Pincode',transaction_count as 'Transaction Count' from top_transaction_pincode
                    where state=%s and year=%s and quarter=%s order by transaction_count"""
        df=fetch_data_by_state(query,state,year,quarter)
        st.bar_chart(df,x='Pincode',y='Transaction Count',use_container_width=True)

    elif options=='Transaction Amount of each Transaction Type of each State':
        col1,col2,col3= st.columns([0.3,0.3,0.3])
        with col1:
            state=st.selectbox('Select a State or Union Territory',['andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam',
                                'bihar','chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep','madhya-pradesh',
                                'maharashtra','manipur','meghalaya','mizoram','nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'])
        with col2:
            year=st.selectbox('Select a Year',[2018,2019,2020,2021,2022,2023])
        with col3:
            quarter=st.selectbox('Select a Quarter',[1,2,3,4])
        query="""select state,`year`,`quarter`,transaction_type as 'Transaction Type',transaction_amount as 'Transaction Amount'
          from aggregate_transaction where state=%s and year=%s and quarter=%s order by transaction_amount """
        df=fetch_data_by_state(query,state,year,quarter)
        fig=px.bar(df,x='Transaction Type',y='Transaction Amount',color='Transaction Amount',color_continuous_scale='ylorrd')
        st.plotly_chart(fig,use_container_width=True) 

    elif options=='Transaction Count of each Transaction Type of each State':
        col1,col2,col3= st.columns([0.3,0.3,0.3])
        with col1:
            state=st.selectbox('Select a State or Union Territory',['andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam',
                                'bihar','chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep','madhya-pradesh',
                                'maharashtra','manipur','meghalaya','mizoram','nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'])
        with col2:
            year=st.selectbox('Select a Year',[2018,2019,2020,2021,2022,2023])
        with col3:
            quarter=st.selectbox('Select a Quarter',[1,2,3,4])
        query="""select state,`year`,`quarter`,transaction_type as 'Transaction Type',transaction_count as 'Transaction Count'
          from aggregate_transaction where state=%s and year=%s and quarter=%s order by transaction_count """
        df=fetch_data_by_state(query,state,year,quarter)
        fig=px.bar(df,x='Transaction Type',y='Transaction Count',color='Transaction Count',color_continuous_scale='ylorrd')
        st.plotly_chart(fig,use_container_width=True)
    
    elif options=='Top 10 Districts by Registered Users of each State':
        col1,col2,col3= st.columns([0.3,0.3,0.3])
        with col1:
            state=st.selectbox('Select a State or Union Territory',['andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam',
                                'bihar','chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep','madhya-pradesh',
                                'maharashtra','manipur','meghalaya','mizoram','nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'])
        with col2:
            year=st.selectbox('Select a Year',[2018,2019,2020,2021,2022,2023])
        with col3:
            quarter=st.selectbox('Select a Quarter',[1,2,3,4])
        query="""select state,district as 'District',`year`,`quarter`,registered_users as 'Registered Users'
          from top_users_district where state=%s and year=%s and quarter=%s order by registered_users """
        df=fetch_data_by_state(query,state,year,quarter)
        fig=px.bar(df,x='District',y='Registered Users',color='Registered Users',color_continuous_scale='ylorrd')
        st.plotly_chart(fig,use_container_width=True)        
    
    elif options=='Top 10 Pincodes by Registered Users of each State':
        col1,col2,col3= st.columns([0.3,0.3,0.3])
        with col1:
            state=st.selectbox('Select a State or Union Territory',['andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam',
                                'bihar','chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep','madhya-pradesh',
                                'maharashtra','manipur','meghalaya','mizoram','nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'])
        with col2:
            year=st.selectbox('Select a Year',[2018,2019,2020,2021,2022,2023])
        with col3:
            quarter=st.selectbox('Select a Quarter',[1,2,3,4])
        query="""select state,pincode as 'Pincode',`year`,`quarter`,registered_users as 'Registered Users'
          from top_users_pincode where state=%s and year=%s and quarter=%s order by registered_users """
        df=fetch_data_by_state(query,state,year,quarter)
        st.bar_chart(df,x='Pincode',y='Registered Users',use_container_width=True)
