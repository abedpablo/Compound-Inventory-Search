from selenium import webdriver
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pandas as pd
import numpy as np

searches = ['selegiline', 'methamphetamine', 'THC', 'codeine', 'buprenorphine', 'hydroxychloroquine', 'norselegiline',
            'cocaine', 'morphine', 'hyromorphone', 'noroxycodone', 'oxymorphone', 'nortriptyline']

new = pd.DataFrame()
missing = []
driver = webdriver.PhantomJS('C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')

for search in searches:
    search = search.replace(' ', '+')
    driver.get("https://www.cerilliant.com/ShopOnline/Product_Cat_List.aspx?text=%s" % (search))
    html = driver.page_source
    soup = bs(html)

    price = []
    description = []
    item = []
    
    pages = soup.findAll('td', {'style': 'white-space: nowrap'}, text = True)
    if len(pages) > 0:
        pages = pages[1]
        length = pages.text.strip()
        number = filter(lambda x: x.isdigit(), length)
        number = int(number)
        for i in reversed(range(0, number)):
            source = driver.page_source
            sp = bs(source)
            table = sp.find('table', {'id': 'ContentPlaceHolder1_gvProdCatList'})
            rows = table.findAll('tr')[1:-3]
            for row in rows:
                cost = row.findAll('td', text = True)
                cost = [ele.text.strip() for ele in cost]
                price.append([ele for ele in cost if ele])
                
                itm = row.findAll('a', text = True)
                itm = [ele.text.strip() for ele in itm]
                item.append([ele for ele in itm if ele])
                
                descr_all = row.findAll('span', limit = 1)
                result = []
                for descr in descr_all:
                    result.extend(descr.find_all(text=True))
                    description.append(result)
                
            if i != 0:
                 seven = driver.find_element_by_xpath('//*[@title="Next"]').click()
            else:
                continue

        df_temp = pd.DataFrame({'Description': description})
        df2 = pd.DataFrame(df_temp['Description'].values.tolist())
        arr = df2.fillna('').values.tolist()
        #list comprehension, replace empty spaces to NaN
        s = pd.Series([''.join(x).strip() for x in arr]).replace('^$', np.nan, regex=True)
        #replace NaN to None
        df3 = s.where(s.notnull(), None)

        df = pd.DataFrame({'Item': item, 'Price': price})
        df['Item'] = df['Item'].str[0]
        df['Price'] = df['Price'].str[0]
        df['Description'] = df3
        df.index = search + '.' + df.index.astype(str)

        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]
        new = pd.concat([new, df])
        
    
    else: 
        table = soup.find('table', {'id': 'ContentPlaceHolder1_gvProdCatList'})
        if table == None:
            missing.append(search)
            continue
        else:
            rows = table.findAll('tr')[1:]
            for row in rows:
                cost = row.findAll('td', text = True)
                cost = [ele.text.strip() for ele in cost]
                price.append([ele for ele in cost if ele])
                
                itm = row.findAll('a', text = True)
                itm = [ele.text.strip() for ele in itm]
                item.append([ele for ele in itm if ele])
                
                descr_all = row.findAll('span', limit = 1)
                result = []
                for descr in descr_all:
                    result.extend(descr.find_all(text=True))
                    description.append(result)
        
        df_temp = pd.DataFrame({'Description': description})
        df2 = pd.DataFrame(df_temp['Description'].values.tolist())
        arr = df2.fillna('').values.tolist()
        #list comprehension, replace empty spaces to NaN
        s = pd.Series([''.join(x).strip() for x in arr]).replace('^$', np.nan, regex=True)
        #replace NaN to None
        df3 = s.where(s.notnull(), None)

        df = pd.DataFrame({'Item': item,
                                'Price': price})
        df['Item'] = df['Item'].str[0]
        df['Price'] = df['Price'].str[0]
        df['Description'] = df3
        df.index = search + '.' + df.index.astype(str)
        
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]
        new = pd.concat([new, df])
        

datestr = datetime.now().strftime('%Y%m%d%H%M%S')
new.to_excel('C://OUTPUT_FOLDER//CerilliantSearch_{}.xlsx'.format(datestr), encoding='utf-8-sig')
if len(missing) != 0:
    print(missing)
else:
    print('All compounds found.')
