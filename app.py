import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk grafik 1 di Comparisson
def comparisson_graph_1():
    try:
        conn = st.connection("mydb", type="sql", autocommit=True)
        cursor = conn.cursor()
        dimtime_query = 'SELECT TimeKey, CalendarYear, EnglishMonthName FROM dimtime'
        cursor.execute(dimtime_query)
        dimtime = pd.DataFrame(cursor.fetchall(), columns=['TimeKey', 'CalendarYear', 'EnglishMonthName'])
        
        factinternetsales_query = 'SELECT OrderDateKey, SalesAmount FROM factinternetsales'
        cursor.execute(factinternetsales_query)
        factinternetsales = pd.DataFrame(cursor.fetchall(), columns=['OrderDateKey', 'SalesAmount'])
        
        merged_data = pd.merge(factinternetsales, dimtime, left_on='OrderDateKey', right_on='TimeKey')
        sales_per_month_year = merged_data.groupby(['CalendarYear', 'EnglishMonthName'])['SalesAmount'].sum().reset_index()
        
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        sales_per_month_year['MonthOrder'] = pd.Categorical(sales_per_month_year['EnglishMonthName'], categories=month_order, ordered=True)
        sales_per_month_year = sales_per_month_year.sort_values(by=['CalendarYear', 'MonthOrder'])
        
        plt.figure(figsize=(14, 8))
        for year in sales_per_month_year['CalendarYear'].unique():
            yearly_data = sales_per_month_year[sales_per_month_year['CalendarYear'] == year]
            plt.plot(yearly_data['MonthOrder'].cat.codes, yearly_data['SalesAmount'], marker='o', label=year)
            
        plt.xticks(ticks=range(12), labels=month_order, rotation=45)
        plt.xlabel('Month')
        plt.ylabel('Total Sales Amount')
        plt.title('Total Sales per Month/Year')
        plt.legend(title='Year')
        plt.grid(True)
        st.pyplot(plt)
        
    except Exception as e:
        st.error(f"Database connection error: {e}")

# Fungsi untuk grafik 2 di Comparisson
def comparisson_graph_2():
    try:
        conn = st.connection("mydb", type="sql", autocommit=True)
        cursor = conn.cursor()
        dimsalesterritory_query = 'SELECT SalesTerritoryKey, SalesTerritoryRegion FROM dimsalesterritory'
        cursor.execute(dimsalesterritory_query)
        dimsalesterritory = pd.DataFrame(cursor.fetchall(), columns=['SalesTerritoryKey', 'SalesTerritoryRegion'])
        
        factinternetsales_query = 'SELECT SalesTerritoryKey, SalesAmount FROM factinternetsales'
        cursor.execute(factinternetsales_query)
        factinternetsales = pd.DataFrame(cursor.fetchall(), columns=['SalesTerritoryKey', 'SalesAmount'])
        
        merged_data = pd.merge(factinternetsales, dimsalesterritory, on='SalesTerritoryKey')
        sales_per_territory = merged_data.groupby('SalesTerritoryRegion')['SalesAmount'].sum().reset_index()
        
        plt.figure(figsize=(14, 8))
        plt.bar(sales_per_territory['SalesTerritoryRegion'], sales_per_territory['SalesAmount'], color='skyblue')
        plt.xlabel('Sales Territory Region')
        plt.ylabel('Total Sales Amount')
        plt.title('Total Sales per Sales Territory Region')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        st.pyplot(plt)
        
    except Exception as e:
        st.error(f"Database connection error: {e}")

# Fungsi untuk grafik 1 di Relationship
def relationship_graph_1():
    try:
        conn = st.connection("mydb", type="sql", autocommit=True)
        cursor = conn.cursor()
        dimpromotion_query = 'SELECT PromotionKey, EnglishPromotionName, DiscountPct FROM dimpromotion'
        cursor.execute(dimpromotion_query)
        dimpromotion = pd.DataFrame(cursor.fetchall(), columns=['PromotionKey', 'EnglishPromotionName', 'DiscountPct'])

        factinternetsales_query = 'SELECT PromotionKey, SalesAmount FROM factinternetsales'
        cursor.execute(factinternetsales_query)
        factinternetsales = pd.DataFrame(cursor.fetchall(), columns=['PromotionKey', 'SalesAmount'])

        merged_data = pd.merge(factinternetsales, dimpromotion, on='PromotionKey')

        plt.figure(figsize=(12, 8))
        plt.scatter(merged_data['DiscountPct'], merged_data['SalesAmount'], alpha=0.5)
        plt.xlabel('Discount Percentage')
        plt.ylabel('Sales Amount')
        plt.title('Discount Percentage vs Sales Amount (Persentase Diskon vs Jumlah Penjualan)')
        st.pyplot(plt)
        
    except Exception as e:
        st.error(f"Database connection error: {e}")

# Fungsi untuk grafik 2 di Relationship
def relationship_graph_2():
    try:
        conn = st.connection("mydb", type="sql", autocommit=True)
        cursor = conn.cursor()
        dimproduct_query = 'SELECT ProductKey, EnglishProductName, ListPrice FROM dimproduct'
        cursor.execute(dimproduct_query)
        dimproduct = pd.DataFrame(cursor.fetchall(), columns=['ProductKey', 'EnglishProductName', 'ListPrice'])
        
        dimcustomer_query = 'SELECT CustomerKey, GeographyKey, YearlyIncome FROM dimcustomer'
        cursor.execute(dimcustomer_query)
        dimcustomer = pd.DataFrame(cursor.fetchall(), columns=['CustomerKey', 'GeographyKey', 'YearlyIncome'])

        merged_data = pd.merge(dimproduct, dimcustomer, left_on='ProductKey', right_on='GeographyKey')

        plt.figure(figsize=(12, 8))
        plt.scatter(merged_data['ListPrice'], merged_data['YearlyIncome'], alpha=0.5)
        plt.xlabel('List Price')
        plt.ylabel('Yearly Income')
        plt.title('List Price vs Yearly Income (Harga Daftar vs Pendapatan Tahunan)')
        st.pyplot(plt)
        
    except Exception as e:
        st.error(f"Database connection error: {e}")

# Fungsi untuk grafik 1 di Composition
def composition_graph_1():
    try:
        conn = st.connection("mydb", type="sql", autocommit=True)
        cursor = conn.cursor()
        dimcustomer_query = 'SELECT CustomerKey, GeographyKey FROM dimcustomer'
        cursor.execute(dimcustomer_query)
        dimcustomer = pd.DataFrame(cursor.fetchall(), columns=['CustomerKey', 'GeographyKey'])
        
        dimgeography_query = 'SELECT GeographyKey, EnglishCountryRegionName FROM dimgeography'
        cursor.execute(dimgeography_query)
        dimgeography = pd.DataFrame(cursor.fetchall(), columns=['GeographyKey', 'EnglishCountryRegionName'])

        merged_data = pd.merge(dimcustomer, dimgeography, on='GeographyKey')

        grouped_data = merged_data.groupby('EnglishCountryRegionName')['CustomerKey'].nunique().reset_index()

        plt.figure(figsize=(12, 8))
        wedges, texts, autotexts = plt.pie(grouped_data['CustomerKey'], labels=grouped_data['EnglishCountryRegionName'], autopct='%1.1f%%', startangle=140, pctdistance=0.85)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        plt.title('Percentage of Unique Customers by Country (Persentase Customer Unik per Negara)')
        plt.tight_layout()
        st.pyplot(plt)
        
    except Exception as e:
        st.error(f"Database connection error: {e}")

# Fungsi untuk grafik 2 di Composition
def composition_graph_2():
    try:
        conn = st.connection("mydb", type="sql", autocommit=True)
        cursor = conn.cursor()
        dimcustomer_query = 'SELECT CustomerKey, EnglishEducation, GeographyKey FROM dimcustomer'
        cursor.execute(dimcustomer_query)
        dimcustomer = pd.DataFrame(cursor.fetchall(), columns=['CustomerKey', 'EnglishEducation', 'GeographyKey'])
        
        dimgeography_query = 'SELECT GeographyKey, EnglishCountryRegionName FROM dimgeography'
        cursor.execute(dimgeography_query)
        dimgeography = pd.DataFrame(cursor.fetchall(), columns=['GeographyKey', 'EnglishCountryRegionName'])

        merged_data = pd.merge(dimcustomer, dimgeography, on='GeographyKey')

        composition_data = merged_data.groupby(['EnglishCountryRegionName', 'EnglishEducation']).size().unstack()
    
        country = composition_data.index
        education_levels = composition_data.columns
        values = composition_data.sum(axis=0)

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

        color_map = {education: color for education, color in zip(education_levels, colors)}

        assigned_colors = [color_map[edu] for edu in education_levels]

        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(aspect="equal"))

        wedges, texts, autotexts = ax.pie(values, autopct='%1.1f%%', startangle=140, pctdistance=0.85, colors=assigned_colors)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig.gca().add_artist(centre_circle)

        ax.legend(wedges, education_levels, title="Education Levels", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        plt.title('Komposisi Edukasi Pelanggan per Country')
        st.pyplot(plt)
        
    except Exception as e:
        st.error(f"Database connection error: {e}")

# Fungsi untuk grafik Distribution
def distribution_graph_1():
    try:
        conn = st.connection("mydb", type="sql", autocommit=True)
        cursor = conn.cursor()
        dimproduct_query = 'SELECT ProductKey, EnglishProductName, ListPrice FROM dimproduct'
        cursor.execute(dimproduct_query)
        dimproduct = pd.DataFrame(cursor.fetchall(), columns=['ProductKey', 'EnglishProductName', 'ListPrice'])

        # Buat Histogram
        plt.figure(figsize=(10, 6))
        plt.hist(dimproduct['ListPrice'], bins=20, color='skyblue', edgecolor='black')
        plt.xlabel('Harga Produk')
        plt.ylabel('Frekuensi')
        plt.title('Distribusi Harga Produk')
        st.pyplot(plt)
        
    except Exception as e:
        st.error(f"Database connection error: {e}")

# Sidebar
st.sidebar.title('Dashboard Options')
option = st.sidebar.selectbox('Choose Aspect', ('Comparisson', 'Relationship', 'Composition', 'Distribution'))

# Main dashboard
st.title(f'Dashboard - {option}')

if option == 'Comparisson':
    st.subheader('Graph 1: Total Sales per Bulan/Tahun')
    comparisson_graph_1()
    st.write("""
    **Analisa Grafik**

    Grafik diatas menunjukkan total penjualan bulanan untuk setiap tahun berdasarkan data dari tabel dimtime dan factinternetsales yang digabungkan. Sumbu x menunjukkan nama bulan dari Januari hingga Desember, sementara sumbu y menunjukkan jumlah total penjualan. Garis yang berbeda dalam grafik mewakili penjualan untuk tahun yang berbeda, memungkinkan melihat bagaimana penjualan setiap bulan dan membandingkan tren penjualan antar tahun. Grafik ini membantu mengidentifikasi pola musiman dan tahunan dalam penjualan, mendukung perencanaan bisnis dan strategi pemasaran yang lebih efektif berdasarkan data historis.
    """)

    st.subheader('Graph 2: Total Sales per Sales Territory Region')
    comparisson_graph_2()
    st.write("""
    **Analisa Grafik**

    Grafik bar diatas menunjukkan total penjualan untuk setiap wilayah penjualan berdasarkan data yang digabungkan dari tabel dimsalesterritory dan factinternetsales. Sumbu x menunjukkan wilayah penjualan, sementara sumbu y menunjukkan jumlah total penjualan. Setiap batang dalam grafik mewakili total penjualan di wilayah tertentu, memungkinkan melihat perbandingan penjualan antar wilayah dengan jelas. Grafik ini membantu mengidentifikasi wilayah dengan performa penjualan tinggi dan rendah, yang dapat digunakan untuk analisis lebih lanjut dan pengambilan keputusan strategis.
    """)
    
elif option == 'Relationship':
    st.subheader('Graph 1: Discount Percentage vs Sales Amount')
    relationship_graph_1()
    st.write("""
    **Analisa Grafik**

    Grafik ini menunjukkan hubungan antara persentase diskon dan jumlah penjualan berdasarkan data yang digabungkan dari tabel dimpromotion dan factinternetsales. Grafik scatter plot ini membantu dalam mengidentifikasi apakah ada korelasi antara diskon yang diberikan dan peningkatan jumlah penjualan.
    """)
    
    st.subheader('Graph 2: List Price vs Yearly Income')
    relationship_graph_2()
    st.write("""
    **Analisa Grafik**

    Grafik ini menunjukkan hubungan antara harga daftar produk dan pendapatan tahunan pelanggan berdasarkan data dari tabel dimproduct dan dimcustomer yang digabungkan. Grafik scatter plot ini memungkinkan melihat apakah ada pola dalam bagaimana harga produk mempengaruhi pelanggan dengan pendapatan yang berbeda-beda.
    """)
    
elif option == 'Composition':
    st.subheader('Graph 1: Persentase Pelanggan Unik per Negara')
    composition_graph_1()
    st.write("""
    **Analisa Grafik**

    Grafik ini menunjukkan persentase pelanggan unik berdasarkan negara berdasarkan data yang digabungkan dari tabel dimcustomer dan dimgeography. Pie chart ini memberikan gambaran proporsi pelanggan di masing-masing negara, membantu dalam analisis pasar dan strategi pemasaran yang lebih efektif.
    """)
    
    st.subheader('Graph 2: Komposisi Edukasi Pelanggan per Negara')
    composition_graph_2()
    st.write("""
    **Analisa Grafik**

    Grafik ini menunjukkan komposisi tingkat edukasi pelanggan per negara berdasarkan data yang digabungkan dari tabel dimcustomer dan dimgeography. Pie chart ini memberikan gambaran distribusi tingkat pendidikan di berbagai negara, yang dapat digunakan untuk memahami demografi pelanggan dan merancang strategi pemasaran yang tepat.
    """)
    
elif option == 'Distribution':
    st.subheader('Graph 1: Distribusi Harga Produk')
    distribution_graph_1()
    st.write("""
    **Analisa Grafik**

    Grafik ini menunjukkan distribusi harga produk berdasarkan data dari tabel dimproduct. Histogram ini membantu dalam melihat bagaimana harga produk tersebar dan dapat memberikan wawasan tentang segmen harga yang paling umum atau jarang terjadi di pasar.
    """)
