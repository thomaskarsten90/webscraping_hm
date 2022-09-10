# Imports
import os
import logging
import re
import pandas  as pd
import numpy   as np
import numpy   as np
import requests
import sqlite3
from sqlalchemy   import create_engine
from bs4          import BeautifulSoup
from datetime     import datetime

#Data Collection
def data_collection(url, headers):
    
    # Request to URL
    page = requests.get (url, headers=headers)

    # Beautiful soup Object
    soup = BeautifulSoup (page.text, 'html.parser')

    # ====================== Product Data ============================= #
    products = soup.find ('ul', class_= 'products-listing small')
    product_list = products.find_all('article', class_='hm-product-item')

    # Product id
    product_id = [p.get('data-articlecode') for p in product_list]

    # Product Category
    product_category = [p.get('data-category') for p in product_list]

    # Product name
    product_list = products.find_all('a', class_='link')
    product_name = [p.get_text() for p in product_list]

    # Product price
    product_list = products.find_all('span', class_='price regular')
    product_price = [p.get_text() for p in product_list]

    data = pd.DataFrame([product_id, product_category, product_name, product_price]).T
    data.columns = ['product_id', 'product_category', 'product_name', 'product_price']

    return data

#Data Collection by product
def data_collection_by_product(data, headers):

    # Empty dataframe
    df_compositions = pd.DataFrame()

    # Unique columns for all products
    aux=[]

    df_pattern = pd.DataFrame( columns=['Art. No.', 'Composition', 'Fit'])
    for i in range (len(data)):
        # API Requests
        url = 'https://www2.hm.com/en_us/productpage.' + data.loc[i, 'product_id'] +'.html'
        
        page = requests.get (url, headers=headers)

        # Beautiful Soup object
        soup = BeautifulSoup (page.text, 'html.parser')

        # ======================= Color name ================================
        product_list = soup.find_all('a', class_= 'filter-option miniature active' ) + soup.find_all('a', class_= 'filter-option miniature' )
        color_name = [p.get('data-color') for p in product_list]

        # Product id
        product_id = [p.get('data-articlecode') for p in product_list]
        
        df_color = pd.DataFrame([product_id, color_name]).T
        df_color.columns = ['product_id', 'color_name']

        for j in range(len(df_color)):
            # API Requests
            url = 'https://www2.hm.com/en_us/productpage.' + df_color.loc[j, 'product_id'] +'.html'
            
            page = requests.get (url, headers=headers)

            # Beautiful Soup object
            soup = BeautifulSoup (page.text, 'html.parser')
            
            # ======================= Product Name ====================
            product_name = soup.find_all('section', class_= 'product-name-price')
            product_name = product_name[0].get_text().split('\n')
            product_name = product_name[3]
            
            # ======================= Product Price ====================
            product_price = soup.find_all('section', class_= 'product-name-price')
            product_price = re.findall(r'\d+\.?\d+', product_price[0].get_text())[0]
            
            # ======================= Composition ================================
            product_composition_list = soup.find_all('div', class_ = 'details-attributes-list-item')
            product_composition = [list(filter(None, p.get_text(). split('\n'))) for p in product_composition_list ]

            # Rename Dataframe
            df_composition = pd.DataFrame(product_composition).T
            df_composition.columns = df_composition.iloc[0]

            # Delete First row
            df_composition = df_composition.iloc[1:].fillna(method='ffill')

            # Remove pocket lining, shell and lining
            df_composition['Composition'] = df_composition['Composition'].replace('Pocket lining: ', '', regex=True)
            df_composition['Composition'] = df_composition['Composition'].replace('Shell: ', '', regex=True)
            df_composition['Composition'] = df_composition['Composition'].replace('Lining: ', '', regex=True)
            df_composition['Composition'] = df_composition['Composition'].replace('Pocket: ', '', regex=True)

            # Garantee the same number of columns
            df_composition = pd.concat([df_pattern, df_composition], axis=0)

            # Selecting only the desired columns
            df_composition = df_composition[['Art. No.', 'Fit', 'Composition']].copy()

            # Rename Columns
            df_composition.columns = ['product_id', 'fit', 'composition']
            df_composition['product_name'] = product_name
            df_composition['product_price'] = product_price

            # Keep new columns if it shows up
            aux = aux + df_composition.columns.tolist()

            # Merge data color + decomposition
            df_composition = pd.merge (df_composition, df_color, how= 'left', on= 'product_id')

            # all products
            df_compositions = pd.concat([df_compositions, df_composition], axis=0)
        
    # Join showroom data + details    
    df_compositions['style_id'] = df_compositions['product_id'].apply (lambda x: x[:-3])
    df_compositions['color_id'] = df_compositions['product_id'].apply (lambda x: x[-3:])

    # Scrapy datetime
    df_compositions['scrapy_datetime'] = datetime.now(). strftime('%Y-%m-%d %H:%M:%S')    

    return df_compositions

#Data Cleanning
def data_cleaning(data_product):
    # Product id
    df_data = data_product.dropna(subset=['product_id'])

    # Product name
    df_data['product_name'] = df_data['product_name'].apply(lambda x: x.replace(' ', '_'). lower())

    # Product_price
    df_data['product_price'] = df_data['product_price'].astype(float)

    # Color name
    df_data['color_name'] = df_data['color_name']. apply(lambda x: x.replace(' ', '_').replace('/', '_').lower())

    # Fit
    df_data['fit'] = df_data['fit']. apply(lambda x: x.replace(' ', '_'). lower())

    # break composition by comma
    df1 = df_data['composition'].str.split(',', expand=True).reset_index(drop=True)

    # cotton | polyester | spandex
    df_ref = pd.DataFrame(index=np.arange(len(df_data)), columns=['cotton', 'polyester', 'spandex'])

    # ===================== Composition ========================
    # ------- cotton ---------
    df_cotton_0 = df1.loc[df1[0].str.contains('Cotton', na=True), 0]
    df_cotton_0.name = 'cotton'

    df_cotton_1 = df1.loc[df1[1].str.contains('Cotton', na=True), 1]
    df_cotton_1.name = 'cotton'

    # Combaine
    df_cotton = df_cotton_0.combine_first(df_cotton_1)

    df_ref = pd.concat([df_ref, df_cotton], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep='last')]

    # --------polyester--------
    df_polyester_0 = df1.loc[df1[0].str.contains('Polyester', na=True), 0]
    df_polyester_0.name = 'polyester'

    df_polyester_1 = df1.loc[df1[1].str.contains('Polyester', na=True), 1]
    df_polyester_1.name = 'polyester'

    # Combaine
    df_polyester = df_polyester_0.combine_first(df_polyester_1)

    df_ref = pd.concat([df_ref, df_polyester], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep='last')]

    # --------spandex-----------
    df_spandex = df1.loc[df1[2].str.contains('Spandex', na=True), 2]
    df_spandex.name = 'spandex'

    df_ref = pd.concat([df_ref, df_spandex], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep='last')]

    # --------lyocell--------
    df_lyocell_0 = df1.loc[df1[0].str.contains('Lyocell', na=True), 0]
    df_lyocell_0.name = 'lyocell'

    df_lyocell_1 = df1.loc[df1[1].str.contains('Lyocell', na=True), 1]
    df_lyocell_1.name = 'lyocell'

    # Combaine
    df_lyocell = df_lyocell_0.combine_first(df_lyocell_1)

    df_ref = pd.concat([df_ref, df_lyocell], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep='last')]

    # --------rayon--------
    df_rayon_0 = df1.loc[df1[0].str.contains('Rayon', na=True), 0]
    df_rayon_0.name = 'rayon'

    df_rayon_1 = df1.loc[df1[2].str.contains('Rayon', na=True), 2]
    df_rayon_1.name = 'rayon'

    # Combaine
    df_rayon = df_rayon_0.combine_first(df_rayon_1)

    df_ref = pd.concat([df_ref, df_rayon], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep='last')]

    # --------elastomultiester-----------
    df_elastomultiester = df1.loc[df1[1].str.contains('Elastomultiester', na=True), 1]
    df_elastomultiester.name = 'elastomultiester'

    df_ref = pd.concat([df_ref, df_elastomultiester], axis=1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep='last')]

    # Join of combine with product_id
    df_aux = pd.concat([df_data['product_id'].reset_index(drop=True), df_ref], axis=1)

    # format composition data
    df_aux['cotton'] = df_aux['cotton'].apply(lambda x: int(re.search('\d+', x).group(0)) / 100 if pd.notnull(x)else x)
    df_aux['polyester'] = df_aux['polyester'].apply(lambda x: int(re.search('\d+', x).group(0)) / 100 if pd.notnull(x) else x)
    df_aux['spandex'] = df_aux['spandex'].apply(lambda x: int(re.search('\d+', x).group(0)) / 100 if pd.notnull(x) else x)
    df_aux['lyocell'] = df_aux['lyocell'].apply(lambda x: int(re.search('\d+', x).group(0)) / 100 if pd.notnull(x) else x)
    df_aux['rayon'] = df_aux['rayon'].apply(lambda x: int(re.search('\d+', x).group(0)) / 100 if pd.notnull(x) else x)
    df_aux['elastomultiester'] = df_aux['elastomultiester'].apply(lambda x: int(re.search('\d+', x).group(0)) / 100 if pd.notnull(x) else x)

    # Final Join
    df_aux = df_aux.groupby('product_id').max().reset_index().fillna(0)
    df_data = pd.merge(df_data, df_aux, on='product_id', how='left')

    # Drop Columns
    df_data = df_data.drop(columns=['composition'], axis=1)

    # Drop Duplicates
    df_data = df_data.drop_duplicates()

    return df_data

#Data Insert
def data_insert (df_data):
	data_insert = df_data[[
    		'product_id',
    		'style_id', 
    		'color_id',
    		'product_name', 
    		'color_name',
    		'product_price',    
    		'fit',   
    		'cotton', 
    		'polyester',
    		'spandex', 
    		'lyocell', 
    		'rayon', 
    		'elastomultiester',
    		'scrapy_datetime'
	]]

	# Create database connection
	conn = create_engine('sqlite:///database_hm.sqlite', echo=False)

	# Insert Data
	data_insert.to_sql('vitrine', con=conn, if_exists='append', index=False)

if __name__ == '__main__':
	# Logging
	path = '/home/linux-thomas/Repos/Curso_Python_DS_ao_DEV/'
	if not os.path.exists( path + 'Logs'):
		os.makedirs(path + 'Logs')

	logging.basicConfig(
		filename= path + 'Logs/webscraping_hm.log',
		level = logging.DEBUG,
		format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
		datefmt = '%Y-%m-%d- %H:%M:%S'
		)

	logger = logging.getLogger('webscraping_hm')
 

	# parameters and constants
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

	# URL
	url = 'https://www2.hm.com/en_us/men/products/jeans.html'

	# Data collection
	data = data_collection(url, headers)
	logger.info ('data collection Done')

    # Data collection by product
	data_product = data_collection_by_product(data, headers)
	logger.info ('data collection by product Done')

    # Data cleanin
	data_product_cleaned = data_cleaning(data_product)
	logger.info ('data product cleaned Done')

    # Data inserction
	data_insert(data_product_cleaned)
	logger.info('data insertion Done')