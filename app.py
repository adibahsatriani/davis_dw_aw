import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# Fungsi untuk membuat koneksi ke database
conn = st.connection("mydb", type="sql", autocommit=True)

# Fungsi untuk grafik 1 di Comparisson
def comparisson_graph_1():
    try:
        conn = create_connection()
        if conn:
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
            
        else:
            st.error("Failed to connect to database.")
            
    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

# Fungsi untuk grafik 2 di Comparisson
def comparisson_graph_2():
    try:
        conn = create_connection()
        if conn:
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
            
        else:
            st.error("Failed to connect to database.")
            
    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

# Fungsi untuk grafik 1 di Relationship
def relationship_graph_1():
    try:
        conn = create_connection()
        if conn:
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
            
        else:
            st.error("Gagal terhubung ke database.")
            
    except mysql.connector.Error as e:
        st.error(f"Kesalahan koneksi database: {e}")
    finally:
        if conn:
            conn.close()

# Fungsi untuk grafik 2 di Relationship
def relationship_graph_2():
    try:
        conn = create_connection()
        if conn:
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
            
        else:
            st.error("Failed to connect to database.")
            
    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

# Fungsi untuk grafik 1 di Composition
def composition_graph_1():
    try:
        conn = create_connection()
        if conn:
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
            
        else:
            st.error("Failed to connect to database.")
            
    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

# Fungsi untuk grafik 2 di Composition
def composition_graph_2():
    try:
        conn = create_connection()
        if conn:
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
            
        else:
            st.error("Failed to connect to database.")
            
    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

# Fungsi untuk grafik Distribution
def distribution_graph_1():
    try:
        conn = create_connection()
        if conn:
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
            
        else:
            st.error("Failed to connect to database.")
            
    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

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

    Grafik diatas menunjukkan total penjualan bulanan untuk setiap tahun berdasarkan data dari tabel dimtime dan factinternetsales yang digabungkan. Sumbu x menunjukkan nama bulan dari Januari hingga Desember, sementara sumbu y menunjukkan jumlah total penjualan. Garis yang berbeda dalam grafik mewakili penjualan untuk tahun yang berbeda, memungkinkan melihat bagaimana penjualan setiap bulan dan membandingkan tren penjualan antar tahun. Seperti garis merah menunjungan total penjualan untuk tahun 2004, dan untuk garis hijau menunjukan penjualan pada tahun 2003, untuk garis orange menunjukan penjualan padatahun 2002, untuk garis biru menunjukan penjualan pada tahun 2001. Jika bisa dilihat dari garis pada grafik, garis merah yaitu yang menunjukan tahun 2004 memiliki penjualan tertinggi yaitu pada bulan June. 
    """)

    st.subheader('Graph 2: Total Sales per Sales Territory Region')
    comparisson_graph_2()
    st.write("""
    **Analisa Grafik**

    Grafik bar diatas menunjukkan total penjualan untuk setiap wilayah penjualan berdasarkan data yang digabungkan dari tabel dimsalesterritory dan factinternetsales. Sumbu x menunjukkan wilayah penjualan, sementara sumbu y menunjukkan jumlah total penjualan. Setiap batang dalam grafik mewakili total penjualan di wilayah tertentu, seperti yang bisa dilihat pada grafik bar, negara yang memiliki penjualan tertinggi adalah Australia, lalu diikuti dengan southwest, dan seterusnya. Di dalam grafik juga terdapat wilayah yang tidak ada grafik batangnya, hal itu menunjukan bahwa pada negara tersebut tidak adanya penjualan. 
    """)
    
elif option == 'Relationship':
    st.subheader('Graph 1: Discount Percentage vs Sales Amount')
    relationship_graph_1()
    st.write("""
    **Analisa Grafik**

    Grafik ini menunjukkan hubungan antara persentase diskon dan jumlah penjualan berdasarkan data yang digabungkan dari tabel dimpromotion dan factinternetsales. Grafik scatter plot ini membantu dalam mengidentifikasi apakah ada korelasi antara diskon yang diberikan dan peningkatan jumlah penjualan. Seperti gambar grafik diatas untuk titik pada garis terlihat paling banyak di presentase 0% yang diartikan banyak penjualan yang tidak mendapatkan diskon, namun ada juga titik pada bagian kanan grafik yang menunjukan bahwa ada penjualan yang mendapatkan diskon mulai dari 15% - 20%
    """)
    
    st.subheader('Graph 2: List Price vs Yearly Income')
    relationship_graph_2()
    st.write("""
    **Analisa Grafik**

    Grafik ini menunjukkan hubungan antara harga daftar produk dan pendapatan tahunan pelanggan berdasarkan data dari tabel dimproduct dan dimcustomer yang digabungkan. Grafik scatter plot ini memungkinkan melihat apakah ada pola dalam bagaimana harga produk mempengaruhi pelanggan dengan pendapatan yang berbeda-beda. Keterkaitan ini bisa memberikan wawasan tentang daya beli pelanggan terhadap produk berdasarkan harga dan pendapatan mereka. Tetapi jika dilihat dari grafik semua sama rata, jadi untuk karyawan yang berpenghasilan tinggi pun juga masih memilih harga yang rendah, begitupun juga karyawan yang berpenghasilan rendah, jika dilihat pada grafik, mereka juga banyak yang mampu membeli dengan harga sedang maupun tinggi. 
    """)
    
elif option == 'Composition':
    st.subheader('Graph 1: Persentase Pelanggan Unik per Negara')
    composition_graph_1()
    st.write("""
    **Analisa Grafik**

    Grafik ini menunjukkan persentase pelanggan unik berdasarkan negara berdasarkan data yang digabungkan dari tabel dimcustomer dan dimgeography. Pie chart ini memberikan gambaran proporsi pelanggan di masing-masing negara, membantu dalam analisis pasar dan strategi pemasaran yang lebih efektif. Jadi singkatnya grafik ini menunjukan presentasi pelanggan di Setiap negara, jika dilihat pada grafik, coklat merupakan warna yang cukup dominan dan menunjukan nilai 42.3% pada negara united states yang artinya pada negara tersebut terdapat pelanggan yang banyak, begitupun juga warna yang sedikit yatu warna orange, menunjukan nilai 8.5% pada negara Canada, yang artinya pada negara tersebut terdapat pelanggan yang jumlahnya sedikit.
    """)
    
    st.subheader('Graph 2: Komposisi Edukasi Pelanggan per Negara')
    composition_graph_2()
    st.write("""
    **Analisa Grafik**

    Grafik ini menunjukkan komposisi tingkat edukasi pelanggan per negara berdasarkan data yang digabungkan dari tabel dimcustomer dan dimgeography. Pie chart ini memberikan gambaran distribusi tingkat pendidikan di berbagai negara, yang dapat digunakan untuk memahami demografi pelanggan dan merancang strategi pemasaran yang tepat. Seperti komposisi pada grafik, warna biru merupakan warna yang cukup dominan dan menunjukan nilai 29% dan warna ini menunjukan tingkat edukasi Bachelors, jadi bisa disimpulkan bahwa pelanggan terbanyak dating dari tingkat edukasi Bachelors, begitu pun juga warna yang paling sedikit yaitu warna ungu, yang artinya pelanggan paling sedikit datang dari tingkat edukasi partial high school.
    """)
    
elif option == 'Distribution':
    st.subheader('Graph 1: Distribusi Harga Produk')
    distribution_graph_1()
    st.write("""
    **Analisa Grafik**

    Grafik ini menunjukkan distribusi harga produk berdasarkan data dari tabel dimproduct. Histogram ini membantu dalam melihat bagaimana harga produk tersebar dan dapat memberikan wawasan tentang segmen harga yang paling umum atau jarang terjadi di pasar. Jika dilihat pada grafik barang yang memiliki harga sekitar 100 – 200 memiliki frekuensi yang paling tinggi, dilanjut dengan rentang harga 500 – 1000 memiliki frekuensi yang cukup tinggi dibandingkan dengan harga 3300 - 3500
    """)
