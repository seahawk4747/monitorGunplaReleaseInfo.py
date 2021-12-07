import requests
from bs4 import BeautifulSoup
import sys
import os
##from pathlib import Path
#from subprocess import call
#import pandas as pd
import tabula
import argparse
import re
import datetime
import hashlib
import csv


old_kit = ['ガンキャノン','ガンダム','シャア専用ザク','量産ザク','ギャン','旧型ザク','ジム',
'ブラウブロ','アッグ','アッガイ','グフ','ドム','シャアゲルググ','量産ゲルググ','シャアズゴック','量産ズゴック',
'ゴック','アッグガイ','ゾゴック','Gアーマー','ボール','ホワイトベース','メカガンダム','メカニックザク',
'リアルガンダム','リアルザク','リアルガンキャノン','リアル旧ザク','リアルジム','リアルドム','リアルゲルググ',
'ランバラル特攻','ジャブローに散る','テキサスの攻防','ア・バオア・クー','ザンジバル','ミニガンダム','シャア専用モビルスーツ',
'武器セット','コアブースター','ララァ専用モビルアーマー','グラブロ','ビグロ','シャアムサイ','巡洋艦ムサイ','ガウ攻撃空母',
'グワジン','マゼラアタック','アッザム','ミディア','ビグザム','サラミス','マゼラン',
'ザクレロ','リックドム','ジュアッグ','ドダイYS','ジオング','ガンタンク','ゾック']

category_list = ["HG","MG","PG","RG","EG","FG","旧キット","Figure-rise","メガサイズ","BB","SD","Other"]

hobby_site_url = "https://bandai-hobby.net/site/schedule.html"
#hobby_site_url ="https://web.archive.org/web/20201024150438/https://bandai-hobby.net/site/schedule.html"

class Color:
	BLACK          = '\033[30m'
	RED            = '\033[31m'
	GREEN          = '\033[32m'
	YELLOW         = '\033[33m'
	BLUE           = '\033[34m'
	MAGENTA        = '\033[35m'
	CYAN           = '\033[36m'
	WHITE          = '\033[37m'
	COLOR_DEFAULT  = '\033[39m'
	BOLD           = '\033[1m'
	UNDERLINE      = '\033[4m'
	INVISIBLE      = '\033[08m'
	REVERCE        = '\033[07m'
	BG_BLACK       = '\033[40m'
	BG_RED         = '\033[41m'
	BG_GREEN       = '\033[42m'
	BG_YELLOW      = '\033[43m'
	BG_BLUE        = '\033[44m'
	BG_MAGENTA     = '\033[45m'
	BG_CYAN        = '\033[46m'
	BG_WHITE       = '\033[47m'
	BG_DEFAULT     = '\033[49m'
	END          = '\033[0m'




def main(argv):
    parser = argparse.ArgumentParser(description =  u'[Options]\nDetailed options -h or --help')


    
    parser.add_argument("-f","--file", type=str , help='load stored Bandai\'s PDF file.' )

    parser.add_argument("-c","--category", type=str , help='check specific category. e.g. MG, RG', nargs = "*" )

    parser.add_argument("-n","--new", action='store_true', help='check only NEW products')

    parser.add_argument("-w","--wishlist", action='store_true', help='filter by wish_list.csv')

    parser.add_argument("-a","--after", type=str, help='filter by date. e.g. 20211215 for 2021/12/15')

    parser.add_argument("-m","--monitor", action='store_true', help='monitor upcoming sales products')



    args = parser.parse_args()

    product_list = []
    if args.monitor == True:
        list = monitorUpcomingSchedule(args.category, args.new , args.wishlist, args.after)
        showSchedule(list)
        calculatePrice(list)
        exit()

    if args.file != None:
        product_list = readPDF(args.file)

        for line in product_list:
            print(line)
        exit()
    
    for item in product_list:
        print (item)

    if args.category != None:
        pass
    
    download_urls = getDownloadPDF(hobby_site_url)
    for url in download_urls:
        product_list = downloadPDF(url)


    

    return

def getBaseTimestamp(date):
    try:
        if str(date) == None:
            base_timestamp = datetime.datetime.now()
        elif str(date) != None:
            base_timestamp = datetime.datetime.strptime(date, '%Y%m%d')
    except :
        base_timestamp = datetime.datetime.now()
    return base_timestamp

def monitorUpcomingSchedule(category, new , wishlist,after):
    
    base_timestamp = getBaseTimestamp(after)

    files = os.listdir(path='.')
    pattern_filename = '[0-9]{4}\-[0-9]{2}.csv'
    repatter = re.compile(pattern_filename)

    monitor_list = []
    for file in files:

        result = repatter.search(file)

        if result != None:
            with open(file, 'r',encoding='utf-8') as f:
                reader = csv.reader(f)
                data = [row for row in reader]
        

            for d in data:
                
                if  (datetime.datetime.strptime(d[3], '%Y-%m-%d %H:%M:%S') - base_timestamp ).days  > -2 and  (datetime.datetime.strptime(d[3], '%Y-%m-%d %H:%M:%S') - base_timestamp ).days  < 8 :
            
                    monitor_list.append([d[0],d[1],int(d[2]),datetime.datetime.strptime(d[3], '%Y-%m-%d %H:%M:%S'),d[4],d[5],int(d[6]) ])
                else:
                    
                    pass

    # do for WISHLIST option
    monitor_list = processWISHLISTOption(monitor_list,wishlist)

    # do for NEW option
    monitor_list = processNEWOption(monitor_list,new)

    # do for CATEGORY option
    monitor_list = processCATEGORYOption(monitor_list, category)

    # sort by datetime object
    sorted_monitor_list = sorted(monitor_list, key=lambda s: s[3])


    

    return sorted_monitor_list

def showSchedule(list):
    sorted_list = sorted(list, key=lambda s: s[3])

    unique_date = []
    for s in sorted_list:
        if s[3] not in unique_date:
            unique_date.append(s[3])

    for ud in unique_date :
        priceA = 0
        priceB = 0
        print("<< 発売日:" + ud.strftime('%Y-%m-%d') + "("+ numToWeekday(ud.weekday())  + ") >>" )
        for sl in sorted_list:
            print_text = ""
            if ud == sl[3]:
                if int(sl[6]) != 0 :
                    print_text += (Color.RED + "*" + Color.END )
                if sl[4] == "NEW":
                    print_text += (Color.RED + "<新製品>" + Color.END )
                
                if int(sl[6]) != 0 :
                    priceA += int(sl[6]) * int(sl[2])
                priceB += int(sl[2])


                print_text += ( "商品ID:" + str(sl[0]) + ", 商品名:" + str(sl[1]) + ", 商品カテゴリー:" + str(sl[5]) + ", 購入予定:" +str(sl[6])+"個")
                

                print(print_text)
        print(Color.GREEN + "Price(only WishList): " + str(priceA) + Color.END )
        print(Color.GREEN + "Price when buying one by one : " + str(priceB) + Color.END )
        print("")
    return 

def calculatePrice(monitor_list) :
            
    total_price = 0
    estimated_price = 0
    for l in monitor_list:
        try:
            total_price += int(l[2]) * int(l[6])
            estimated_price += int(l[2])
        except:
            pass
    print(Color.GREEN + "Total price(only WishList): " + str(total_price) + Color.END )
    print(Color.GREEN + "Total price when buying one by one : " + str(estimated_price) + Color.END )
    return total_price, estimated_price

def processWISHLISTOption(data,wishlist_flag):
    output_data = []
    if wishlist_flag == True:
        
        try:
            with open('wish_list.csv', 'r',encoding='utf-8') as f:
                reader = csv.reader(f)
                wishlist_data = [row for row in reader]

            for wish in wishlist_data:
                for n in range(len(data)):
                    if str(wish[0]) == str(data[n][0]) :
                        data[n][6] =  int(wish[1])
                        output_data.append(data[n])
            
                
        except:
            print("Error")
            pass
    elif wishlist_flag == False:
        try:
            with open('wish_list.csv', 'r',encoding='utf-8') as f:
                reader = csv.reader(f)
                wishlist_data = [row for row in reader]

            for wish in wishlist_data:
                for n in range(len(data)):
                    if str(wish[0]) == str(data[n][0]) :
                        data[n][6] =  int(wish[1])
                        
        except:
            pass
        output_data = data

    return output_data

def processCATEGORYOption(data,category_flag):
    output_data = []
    if category_flag == None  or len(category_flag) == 0:
        return data

    for category in category_flag :
        try:
            for n in range(len(data)):
                if str(category) == str(data[n][5]) :
                    output_data.append(data[n])
        except:
            print("Error")
            pass
    
    return output_data

def processNEWOption(data,new_flag):

    output_data = []
    if new_flag == True:
        try:
            for n in range(len(data)):
                if str(data[n][4])  == "NEW":

                    output_data.append(data[n])        
        except:
            print("Error")
            pass
    elif new_flag == False:
        return data

    return output_data

def updateProductList(data):
    # list:   product ID, product name, price, category
    products_data = []

    if os.path.exists('products_list.csv') == True:
        
        with open('products_list.csv', 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            latest_data = [row for row in reader]
        if len(latest_data) != 0 and len(data) != 0:
            for m in range(len(data)):
                flag = 0
                for n in range(len(latest_data)):
                    if latest_data[n][0] == data[m][0]:
                        # If sales price has been changed, update it.
                        if data[m][2] != None:
                            products_data.append([ latest_data[n][0],latest_data[n][1],data[m][2],latest_data[n][3] ])
                        else:
                            products_data.append([ latest_data[n][0],latest_data[n][1],latest_data[n][2],latest_data[n][3] ])
                        flag = 1

                if flag == 0 :
                    products_data.append([data[m][0],data[m][1],data[m][2],data[m][5]])

        else:
            for d in data:
                products_data.append([ d[0],d[1],d[2],d[5] ])

    else:

        for d in data:
            products_data.append([ d[0],d[1],d[2],d[5] ])
    

    with open('products_list.csv', 'w',encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator="\n")
        
        writer.writerows(products_data)

    return

def readPDF(filepath):
    output_list = []
    print("Reading stored PDF file.")

    if os.path.splitext(filepath)[1] != ".pdf" :
        print("Not PDF file!!!")
        exit()
    
    year,month = getMonthYear(filepath)

    dfs = tabula.read_pdf(filepath, lattice=True, pages = 'all')

    raw_list = []
    for df in dfs:
        raw_list += df.to_numpy().tolist()

    
    output_list = parseTable(raw_list,year,month)

    # convert nan to None
    for n in range(len(output_list)):
        if type(output_list[n][4]) != 'str' and output_list[n][4] != "NEW":
            output_list[n][4] = None

    updateProductList(output_list)
    
    return output_list

def parseTable(data,year,month):
    output_list = []

    for row in data:
        if len(row) < 3:
            continue

        pattern_num = '^[0-9]{7}'
        repatter = re.compile(pattern_num)

        result = repatter.search(str(row[0]))
        if result != None:
            row[0] = result.group(0)

        
        result = repatter.match(str(row[0]))
        
        if result == None:
            pass
        else:
            pattern_release_date = '[0-9]{1,2}日'
            repatter2 = re.compile(pattern_release_date)

            for n in range(3):

                result2 = repatter2.match(str(row[n+4]))
                if result2 != None:
                    output_list.append([ row[0],row[n+2],row[n+3],row[n+4],row[n+5],check_category(row[n+2]),0])

        for n in range(4):
            result = repatter.match(str(row[n+5]))
            if result == None:
                pass
            else:

                pattern_release_date = '[0-9]{1,2}日'
                repatter3 = re.compile(pattern_release_date)
                for m in range(6):
                    result3 = repatter3.match(str(row[n+m+5]))
                    if result3 != None:
                        output_list.append([ row[n+5], row[n+m+3],row[n+m+4],row[n+m+5],row[n+m+6],check_category(row[n+m+3]),0])

    # data cleansing
    pattern_prefix = '^[0-9]+'
    repatter = re.compile(pattern_prefix)
    for line in output_list:

        try:
            line[1] = line[1].replace("\xad","")
        except:
            pass
        
        try:
            if line[1][0:2] != "1/"  :
                result = repatter.search(line[1])
                # example:238238. Repeating first 3digit twice, that should be BB
                if line[1][0:3] == line[1][3:6] :
                    line[5] = 'BB'
                line[1] = line[1].replace(result.group(0),"").strip()
            
        except:
            pass
        
        # old_kit's name starts from "1/", also includes a word in "old_kit" list.
        try:
            if line[1][0:2] == "1/"  :
                for name in old_kit:
                    if name in line[1]:
                        line[5] = '旧キット'
        except:
            pass

        try:
            line[2] = int(line[2].replace(",",""))
        except:
            line[2] = line[2].replace(",","")
        day = int(line[3].replace("日",""))
        line[3] = datetime.datetime(year,month,day)


    return output_list

def check_category(data):
    output ="Other"
    category = ["HG","MG","PG","RG","EG","FG","旧キット","Figure-rise","メガサイズ","BB","SD","Other"]
    for cat in category:
        if cat in data and "GD" not in data:
            output = cat
        
    return output

def downloadPDF(url):

    output = []

    output_filename = ""
 
    pdf_path = (url.split('/')[len(url.split('/'))-1])
    filename=  os.path.splitext(pdf_path)[0]
    #print(filename)
    if  os.path.splitext(pdf_path)[1] == '.pdf' :
        urlData = requests.get(url).content
        
        with open(pdf_path ,mode='wb') as f: 
            f.write(urlData)
        pdf_hash = hashlib.md5(urlData).hexdigest()
        #print(pdf_hash)
        year,month = getMonthYear(pdf_path)
        output.append([pdf_path,pdf_hash,year,month])

        if year != None and month != None:
            output_filename = str(year)+"-"+ str(month)+ ".csv"
    else:
        return None


    dfs = tabula.read_pdf(pdf_path, lattice=True, pages = 'all')

    raw_list = []
    for df in dfs:
        raw_list += df.to_numpy().tolist()


    output_list = parseTable(raw_list,year,month)

    # convert nan to None
    for n in range(len(output_list)):
        if type(output_list[n][4]) != 'str' and output_list[n][4] != "NEW":
            output_list[n][4] = None
    
    if os.path.exists('downloaded_files_info.csv') == False:
        with open('downloaded_files_info.csv', 'w',encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerows(output)
        # write data as <YEAR>-<MONTH>.csv
        #print(output_filename)
        with open( output_filename, 'w',encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerows(output_list)
    else:
        
        with open('downloaded_files_info.csv', 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            latest_data = [row for row in reader]

        for row2 in output:
            #print(row2)
            for row_num in range(len(latest_data)):
                #print(latest_data[row_num],row2)

                if len(latest_data[row_num]) == len(row2) and latest_data[row_num][0] == row2[0] and latest_data[row_num][1] == row2[1]:
                    #print("same file.")
                    pass
                elif len(latest_data[row_num]) == 0:
                    pass
                elif len(latest_data[row_num]) == len(row2) and latest_data[row_num][0] != row2[0] and latest_data[row_num][1] == row2[1]:
                    #print("diffenet filename , but same hash.")
                    latest_data[row_num] = [ row2[0],  latest_data[row_num][1]   ]
                elif len(latest_data[row_num]) == len(row2) and latest_data[row_num][0] == row2[0] and latest_data[row_num][1] != row2[1] :
                    #print("same filename , but different hash.")
                    latest_data[row_num] = [ latest_data[row_num][0],   row2[1]     ]
                elif len(latest_data[row_num]) == len(row2) and latest_data[row_num][0] != row2[0] and latest_data[row_num][1] != row2[1]:
                    #print("different filename , different hash.")

                    # add row2
                    latest_data.append(row2)
                    # write data as <YEAR>-<MONTH>.csv
                    #print(output_filename)
                    with open( output_filename, 'w',encoding='utf-8') as f:
                        writer = csv.writer(f, lineterminator="\n")
                        writer.writerows(output_list)

        #print(latest_data)

        # update 'downloaded_files_info.csv'
        with open('downloaded_files_info.csv', 'w',encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerows(latest_data)
        pass

    updateProductList(output_list)

    
    return output_list

def getDownloadPDF(url):

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    header = {
	    'User-Agent': user_agent
	}
    try:
        response = requests.get(url,headers=header)
        
        soup = BeautifulSoup(response.text, "html.parser")

        onclick = soup.find_all('input', type="button")
        pdf_urls =[]
        for data in onclick:
            if data.get('value') == 'PDFダウンロード':
                pdf_url = 'https://bandai-hobby.net/site/' + re.sub('window.open\(\'|\'\)$', '', data.get('onclick'))
                pdf_urls.append(pdf_url)
    except:
        return None

    return pdf_urls

def monthToNum(shortMonth):
    return {
            'jan': 1,
            'feb': 2,
            'mar': 3,
            'apr': 4,
            'may': 5,
            'jun': 6,
            'june':6,
            'jul': 7,
            'july':7,
            'aug': 8,
            'august':8,
            'sep': 9, 
            'oct': 10,
            'nov': 11,
            'dec': 12
    }[shortMonth]

def numToWeekday(num):
    return {
            0: "月",
            1: "火",
            2: "水",
            3: "木",
            4: "金",
            5: "土",
            6: "日",
    }[num]

def getMonthYear(filename):
    pattern_year = '[0-9]{4}'
    repatter = re.compile(pattern_year)

    result = repatter.search(filename)
    year = int(result.group(0))
    
    pattern_month = r'jan|feb|mar|apr|may|jun|june|jul|july|aug|august|sep|oct|nov|dec'
    repatter = re.compile(pattern_month)

    result = repatter.search(filename)
    month = monthToNum(result.group(0))

    return year,month

def checkFilehash(input,data_filename):
    # downloaded_files_info.csvをチェックして、過去に同じファイルを処理していないか確認。
    
    flags = [0,0,0]
    if os.path.exists(data_filename) == True:
        with open(data_filename,'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            latest_data = [row for row in reader]
    

    for data in latest_data:

        if len(data) == 4:
            print(input, data)
            if data[1] == input[1]:
                flags[0] = 1

            if data[0] == input[0]:
                flags[1] = 1
            if str(data[2]) == str(input[2]) and str(data[3]) == str(input[3]):
                flags[2] = 1

    return flags

if __name__ == '__main__':
    main(sys.argv[1:])