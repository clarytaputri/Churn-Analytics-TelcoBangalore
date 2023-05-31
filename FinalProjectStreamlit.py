import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

# Konfigurasi awal streamlit
st.set_page_config(
    page_title = 'FSB - Claryta - Final Project', 
    page_icon = '🐧', 
    layout = "wide"
)

# Ekstrak data & cleansing
@st.cache_resource
def ekstrak_data(url_data):
    #Ekstraksi data
    raw_data = pd.read_csv(url_data)

    # Copy data ke variabel baru
    data = raw_data.copy()
    
    # Transformasi nama kolom menjadi lowercase
    data.columns = data.columns.str.lower()
    data.columns = data.columns.str.replace(' ', '_')

    # Drop some columns
    data = data.drop(columns = ['zip_code',	'latitude',	'longitude'])

    return (data)

# Ornamen pada header
@st.cache_resource
def header():
    spacer1, row1, spacer2 = st.columns([0.1, 7.2, 0.1])
    
    row1.title('Telco Churn Analysis')
    row1.subheader('Streamlit App by [Claryta Putri Dedyana Wati](https://www.linkedin.com/in/claryta-putri-dedyana-wati/)')
    
    row1.header('Background')
    
    row1.markdown("""
        <b>Customer churn</b> refers to the proportion of customers who terminate their relationship with a business or cease utilizing its services. 
        The churn rate is determined by the number of customers who discontinue their association with the business within a specific timeframe. 
        Gaining an understanding of customer churn is crucial for companies as it serves as an indicator of their success in retaining customers.<br>

        <b>Telco Bangalore</b> 
        Telco Bangalore is a fictional telecommunications company that not only offers telephone services but has also expanded its offerings to include 
        secure and high-quality internet services, streaming of TV shows, movies, music, and various other services. Despite the promising nature of the 
        services provided by the company, it is inevitable that some customers will eventually decide to unsubscribe or churn. Numerous factors contribute 
        to this occurrence, underscoring the significance for the company to analyze these factors comprehensively.By doing so, they can formulate data-
        driven policies that enable them to retain their valuable customers.<br>
        """, 
        unsafe_allow_html = True
    )

@st.cache_resource       
def tampilkan_data(data):
    spacer1, row1, spacer2 = st.columns([0.1, 7.2, 0.1])
    row1.header('Data')
    row1.markdown(
        'The data used in this project is presented in the following table',
        unsafe_allow_html = True
    )
    
    spacer1, row2, row3, spacer2 = st.columns([0.1, 7.2, 7.2, 0.1])
    row2.metric(
        label = "Total Data", 
        value = data.shape[0]
    )
        
    row3.metric(
        label = "Total Coloumn", 
        value = data.shape[1]
    )
    
    spacer1, row4, spacer2 = st.columns([0.1, 7.2, 0.1])
    row4.dataframe(data)

# Hitung banyak customer yang dikelompokkan berdasarkan status
@st.cache_resource
def perhitungan_customer_status(data):
    # Hitung total data (unik) customer id per status customernya
    cust_status = data.groupby(['customer_status'], as_index = False).agg(total_cust_status = ('customer_id', pd.Series.nunique))

    # Buat grafik pie
    fig = px.pie(
        cust_status, 
        values = 'total_cust_status', 
        names = 'customer_status',
        #hover_data = ['total_cust_status'], 
        labels = {
            'customer_status' : 'Customer Status',
            'total_cust_status' : 'Total Customer'
        },
        color = 'customer_status',
        color_discrete_map = {
            'Churned' : '#ff0000',
            'Stayed' : '#5bb450',
            'Joined' : '#72bf6a'                                 
        }
    )

    fig.update_traces(
        textposition = 'inside', 
        textinfo = 'percent+label',
        pull = [0.1, 0, 0]
    )


    fig.update_layout(
        autosize = False,
        width = 400,
        height = 450,
        showlegend = False,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)'
    )

    return (cust_status, fig)

@st.cache_resource
def tampilkan_status_customer(data):
    
    spacer1, row1, spacer2 = st.columns([0.1, 7.2, 0.1])
    row1.header('Visualization')
    
    spacer1, row1, spacer2, row2, spacer3 = st.columns([0.1, 4, 0.1, 3.2, 0.1])
    cust_status, fig = perhitungan_customer_status(data)
    
    total_cust_churn = cust_status[cust_status['customer_status'] == 'Churned']['total_cust_status'].values[0]
    total_joined_churn = cust_status[cust_status['customer_status'] == 'Joined']['total_cust_status'].values[0]
    total_stay_churn = cust_status[cust_status['customer_status'] == 'Stayed']['total_cust_status'].values[0]
    
    row1.plotly_chart(
        fig, 
        use_container_width = False
    )
    
    row2.markdown(f"""
        Based on the pie, it can been observed that <b>{total_cust_churn}</b> 
        customers have discontinued their subscribtions (<i>Churned</i>),
        while <b>{total_stay_churn}</b> customers remain active (<i>Stayed</i>) 
        and the company has acquired <b>{total_joined_churn}</b> new customers during this period (<i>Joined</i>).
        <br><br>
        
        Upon close examination, the propotion of <i>churned</i> customers is larger than the propotion of new customers (<i>joined</i>). 
        Therefore it is crucial for company to analyze the available data to identify the factors that contribute customer churn  
        and promptly establish further strategies to retain existing subscribers and increase the number of new customers.
        """,
        unsafe_allow_html = True                               
    )

@st.cache_resource
def perhitungan_churn_reason(data):
    
    # Hitung total data cust
    cust_churn_category = data.groupby(['churn_category', 'churn_reason'], as_index = False).agg(total_cust_churn_per_reason = ('customer_id', pd.Series.nunique))

    cust_churn_category['total_cust_churn_per_category'] = cust_churn_category.groupby(['churn_category'], as_index = False)['total_cust_churn_per_reason'].transform(sum)

    cust_churn_category = cust_churn_category.sort_values(
        by = ['total_cust_churn_per_category', 'total_cust_churn_per_reason'], 
        ascending = True,
        ignore_index = True
    )
    
    cust_churn_category['index_largest'] = cust_churn_category.sort_values(['total_cust_churn_per_reason'], ascending = False) \
             .groupby(['churn_category']) \
             .cumcount() + 1
             
    cust_churn_category['index_largest'] = ['largest' if x == 1 else '' for x in cust_churn_category['index_largest']]
    cust_churn_category['text'] = cust_churn_category['churn_reason'] + '<br> (' + cust_churn_category['total_cust_churn_per_reason'].astype(str) + ')'

    fig = px.bar(
        cust_churn_category, 
        x = "total_cust_churn_per_reason", 
        y = "churn_category", 
        color = "index_largest", 
        color_discrete_map = {
            'largest' : '#FF0000',
            '' : '#F4b4b4'
        },
        orientation = 'h',
        text = "text",
    )

    fig.update_layout(
        autosize = False,
        width = 650,
        height = 400,
        showlegend = False,
        xaxis=dict(
            title = "",
            zeroline=False,
            showgrid = False,
            side = 'top'
        ),
        yaxis=dict(
            title = '',
            visible = True, 
            showticklabels = True,
            showgrid = False
        ),
        font = dict(
            size = 9
        ),
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)'
    )

    hovertemplate = '<b>%{y}</b><br>'\
                    '%{text}<br>'
                    
    fig.update_traces(
        hovertemplate = hovertemplate, 
        customdata = cust_churn_category["churn_reason"]
    )

    return(cust_churn_category, fig)

@st.cache_resource
def tampilkan_alasan_churn(data):
    spacer1, row1, spacer2 = st.columns([0.1, 7.2, 0.1])
    row1.header('Reason for Customer Churn?')
    
    spacer1, row1, row2 = st.columns([0.1, 5, 6])
    cust_churn_category, fig = perhitungan_churn_reason(data)
    
    row1.markdown(f"""
       <br> Upon investigation, Upon investigation, it has been found that the primary reason for a significant number 
       of customers switching away from the company is due to competition. Specifically, it appears that competitor 
       companies offer devices or technologies that are superior or more advanced. Another correlated reason relates 
       to the main cause of customer churn, which is dissatisfaction with the products provided by the company. 
       Consequently, the company must evaluate its service offerings, analyze the attractive products offered by competitors,
       and make necessary upgrades. It is not only product-related aspects that require improvement, but also other factors 
       such as assessing the attitudes and performance of employees, implementing promotions, and considering other reasons for churn. 
       These factors should be prioritized by the company if they aim to enhance customer retention in the future.
        """,
        unsafe_allow_html = True                               
    )
    
    row2.plotly_chart(
        fig, 
        use_container_width = False
    )
     
def text_graph(text1, text2, color):
    fig, [ax1, ax2] = plt.subplots(
        nrows = 2, 
        ncols = 1,
        figsize = (1, 0.5)
    )

    ax1.text(
        x = 0, 
        y = 0.2, 
        s = text1,
        color = color,
        fontsize = 14,
        fontweight = 'light',
    )

    ax2.text(
        x = 0, 
        y = 0.1, 
        s = text2,
        color = color,
        fontsize = 18,
        fontweight = 'semibold',
    )

    ax1.axis('off')
    ax2.axis('off')
    
    return fig 

@st.cache_resource
def tampilkan_revenue_impact(data):
    # Hitung total data (unik) customer id per status customernya
    revenue_per_status = data.groupby(['customer_status'], as_index = False).agg(total_revenue = ('total_revenue', pd.Series.sum))

    raw_revenue_stayed = revenue_per_status[revenue_per_status['customer_status'] == 'Stayed']['total_revenue'].values[0] 
    raw_revenue_joined = revenue_per_status[revenue_per_status['customer_status'] == 'Joined']['total_revenue'].values[0]
    raw_revenue_churn = revenue_per_status[revenue_per_status['customer_status'] == 'Churned']['total_revenue'].values[0]

    revenue_stayed = round(raw_revenue_stayed / 10**6, 2)
    revenue_joined = round(raw_revenue_joined / 10**6, 2)
    revenue_churn = round(raw_revenue_churn / 10**6, 2)
    
    fig1 = text_graph('Stayed', '$ ' + str(revenue_stayed) + 'M', '#5bb450')
    fig2 = text_graph('Joined', '$ ' + str(revenue_joined) + 'M', '#5bb450')
    fig3 = text_graph('Churn', '$ ' + str(revenue_churn) + 'M', '#ff0000')
    
    spacer1, row1, spacer2 = st.columns([0.1, 7.2, 0.1])
    row1.header('Impact On The Company')
    
    spacer1, row2, row3, row4, spacer2 = st.columns([0.1, 3, 3, 3, 0.1])
    
    row2.pyplot(
        fig1, 
        use_container_width = False
    )
    
    row3.pyplot(
        fig2, 
        use_container_width = False
    )
    
    row4.pyplot(
        fig3, 
        use_container_width = False
    )
    
    spacer1, row5, spacer2 = st.columns([0.1, 7.2, 0.1])
    row5.markdown(f"""
        The impact of customers deciding to unsubscribe from the company is evident in the significant loss of \${revenue_churn}M (in more detail = \${round(raw_revenue_churn, 2)}). 
        This is a concern for the company, as the financial loss resulting from customer churn outweighs the revenue generated from new customers, 
        which amounts to \${revenue_joined}M (lebih detail = \${round(raw_revenue_joined, 2)}). Therefore, considering the imbalance in revenue, it is crucial for the 
        company to pay close attention to the reasons behind customer attrition in order to minimize the potential for greater negative impacts.
        
        """, 
        unsafe_allow_html = True
    )

# All Demografi
def count_per_gender(data):
    count_data_per_gender = data.groupby(['gender'], as_index = False).agg(count_data_per_gender = ('customer_id', pd.Series.nunique))
    count_male_data = count_data_per_gender[count_data_per_gender['gender'] == 'Male']['count_data_per_gender'].values[0]
    count_female_data = count_data_per_gender[count_data_per_gender['gender'] == 'Female']['count_data_per_gender'].values[0]
    return (count_male_data, count_female_data)

def distribusi_umur(data, gender, color):
    fig = px.histogram(
        data[data['gender'] == gender], 
        x = "age",
        nbins = 10,
        color_discrete_sequence=[color]
    )

    fig.update_layout(
        autosize = False,
        width = 500,
        height = 400,
        bargap = 0.02,
        showlegend = False,
        xaxis = dict(
            title = f"Customer Age Distribution<br>{gender}",
            zeroline = False,
            showgrid = False
        ),
        yaxis = dict(
            title = "",
            visible = True, 
            showticklabels = True,
            showgrid = False
        ),
        font = dict(
            size=9
        ),
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)'
    )

    return fig

def married_status(data, gender, color):
    married_per_gender = data[data['gender'] == gender].groupby(['married'], as_index = False).agg(married_per_gender = ('customer_id', pd.Series.nunique))

    fig = px.pie(
        married_per_gender, 
        values = 'married_per_gender', 
        names = 'married',
        labels = {
            'married' : 'is Married?',
            'married_per_gender' : 'Total Customer'
        },
        color = 'married',
        color_discrete_map = {
            'Yes' : color[0],
            'No' : color[1]                                
        },
        hole = 0.5
    )

    fig.update_traces(
        textposition = 'inside', 
        textinfo = 'percent+label',
        pull = [0.01, 0]
    )


    fig.update_layout(
        autosize = False,
        width = 500,
        height = 400,
        showlegend = False,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        annotations=[
            dict(
                text = 'Married<br>Status', 
                x = 0.5, 
                y =0.5, 
                font_size=20, 
                showarrow=False
            )
        ]
    )
    
    fig.update_annotations(
        font = dict(
            family = "sans serif", 
            color = color[0]
        )
    )
                 
    return (fig)

def contract_type(data, gender):
    
    data = data[data['gender'] == gender]
    data['internet_type'] = data['internet_type'].fillna('No Internet Service')
    internet_type_per_gender = data.groupby(['contract', 'internet_type'], as_index = False).agg(total_cust_per_internet_type = ('customer_id', pd.Series.nunique))
 
    if(gender == 'Male'):
        color_internet_type = {
            '(?)':'#9FFFCB',
            'Fiber Optic' : '#32CD32',
            'Cable' : '#93DC5C',
            'DSL' : '#B7E892',
            'No Internet Service' : '#21D375'                              
        }
    else:
        color_internet_type = {
            '(?)':'#93E9BE',
            'Fiber Optic' : '#3A5A40',
            'Cable' : '#588157',
            'DSL' : '#5A9F68',
            'No Internet Service' : '#BBD58E'                              
        }
        
    fig = px.treemap(
        internet_type_per_gender, 
        path = [
            px.Constant('Contract Type'),
            'contract',
            'internet_type'
        ], 
        values = 'total_cust_per_internet_type',
        color = 'internet_type',
        color_discrete_map = color_internet_type,
        title = f'Contract Status and Internet Type of <br>{gender}'
    )

    fig.update_layout(
        autosize = False,
        width = 525,
        height = 425,
        showlegend = False,
        xaxis = dict(
            title = f"Customer Age Distribution<br>{gender}"
        ),
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)'
    )

    fig.update_traces(
        marker = dict(cornerradius = 5)
    )
    
    return (fig)
    
    
def tampilkan_demografi(data, url_img_man, url_img_woman):
    male_color, female_color = '#fbe280', '#5bbc95'
    
    spacer1, row1, spacer2 = st.columns([0.1, 7.2, 0.1])
    row1.header('Customer Demographics by Status')
    
    with row1:
        st.markdown(f"""         
            In today's highly competitive business world, a deep understanding of customers is crucial for success. Every company aims to enhance their
            understanding of customer segmentation, strengthen marketing strategies, and provide more personalized and relevant experiences to each individual 
            customer. Therefore, it is vital for companies to prioritize their focus on customers based on gender and their current status. This knowledge is 
            essential for companies to improve their products and services, but with a more personalized segmentation based on gender and a clear understanding 
            of their specific needs.
            """, 
            unsafe_allow_html = True
        )
        status = st.multiselect(
            label = 'Select Customer Status',
            options = data['customer_status'].unique(),
            default = 'Stayed'
        )
    
    filter_data = data.loc[data['customer_status'].isin(status)]

    count_male_data, count_female_data = count_per_gender(filter_data)
    fig_hist_male = distribusi_umur(filter_data, gender = 'Male', color = male_color)
    fig_hist_female = distribusi_umur(filter_data, gender = 'Female', color = female_color)

    fig_pie_married_male = married_status(filter_data, gender = 'Male', color = ('#bfac60', male_color))
    fig_pie_married_female = married_status(filter_data, gender = 'Female', color = ('#469173', female_color))
    
    fig_treemap_male = contract_type(filter_data, gender = 'Male')
    fig_treemap_female = contract_type(filter_data, gender = 'Female')
    
    spacer1, row2, spacer, row3, spacer3 = st.columns([0.1, 3, 0.5, 3, 0.1])
    with row2:
        st.markdown(
            f"<p style='text-align: center; color: {male_color}; font-size : 350%;'> Male </p>", 
            unsafe_allow_html = True
        )
        
        st.markdown(f"""
            <p style='text-align: center;'> 
                <img src='{url_img_man}' width="250" height="250"> 
            </p>
            """, 
            unsafe_allow_html = True
        )
        
        st.markdown(
            f"<p style='text-align: center; color: {male_color}; font-size : 350%;'> {count_male_data} </p>", 
            unsafe_allow_html = True
        )
        
        st.markdown(
            f"<p style='text-align: center; color: {male_color}; font-size : 150%;'> ({', '.join(status)}) </p>", 
            unsafe_allow_html = True
        )
        
        st.plotly_chart(
            fig_hist_male, 
            use_container_width = False
        )
        
        st.plotly_chart(
            fig_pie_married_male, 
            use_container_width = False
        )
        
        st.plotly_chart(
            fig_treemap_male, 
            use_container_width = False
        )
        
    with row3:        
        st.markdown(
            f"<p style='text-align: center; color: {female_color}; font-size : 350%;'> Female </p>", 
            unsafe_allow_html = True
        )
        
        st.markdown(f"""
            <p style='text-align: center;'> 
                <img src='{url_img_woman}' width="250" height="250"> 
            </p>
            """, 
            unsafe_allow_html = True
        )
        
        st.markdown(
            f"<p style='text-align: center; color: {female_color}; font-size : 350%;'> {count_female_data} </p>", 
            unsafe_allow_html = True
        )
        
        st.markdown(
            f"<p style='text-align: center; color: {female_color}; font-size : 150%;'> ({', '.join(status)}) </p>", 
            unsafe_allow_html = True
        )

        st.plotly_chart(
            fig_hist_female, 
            use_container_width = False
        )
        
        st.plotly_chart(
            fig_pie_married_female, 
            use_container_width = False
        )
        
        st.plotly_chart(
            fig_treemap_female, 
            use_container_width = False
        )
    
    
if __name__ == "__main__":
    header()
    
    url_data = 'https://raw.githubusercontent.com/clarytaputri/Claryta-Final-Project-Churn-Analytics/main/telecom_customer_churn.csv'
    data = ekstrak_data(url_data)
    
    tampilkan_data(data)
    tampilkan_status_customer(data)
    tampilkan_alasan_churn(data)
    tampilkan_revenue_impact(data)
    
    url_img_man = 'https://raw.githubusercontent.com/clarytaputri/Claryta-Final-Project-Churn-Analytics/main/man.png'
    url_img_woman = 'https://raw.githubusercontent.com/clarytaputri/Claryta-Final-Project-Churn-Analytics/main/woman.png'
    
    tampilkan_demografi(data, url_img_man, url_img_woman)
