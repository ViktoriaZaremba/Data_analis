import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("DATABASE.csv", sep = ';', decimal=',')
data = data.rename(
        columns={"day/month": "Date", 'Dew Point': 'Dew_Point', 'Wind Speed': 'Wind_Speed', 'Wind Gust': 'Wind_Gust',
                 'Precip Accum': 'Precip_Accum', 'Precip.': 'Precip'})


def pars(data, colums):
    data['Date'] = pd.to_datetime(data["Date"] + ".2019")
    data['Time'] = pd.to_datetime(data['Time']).dt.strftime('%H:%M')
    data['Pressure'] = data['Pressure'].astype(float)
    for c in colums:
        data[c] = data[c].map(lambda x: x.strip(' mph%'))
        data[c] =data[c].astype(int)
    data.set_index('Date')


colums = ['Wind_Speed', 'Wind_Gust','Humidity']
pars(data, colums)



def dia_choose(a):
    print('Columns:')
    for col in data.columns:
        print(col, end=', ')
    b = list(map(str, input("\nEnter columns: ").strip().split()))
    if a == 1:
        print("Do you want to group data by date?\n If yes, print 'min', 'max' or 'mean'. \nIf not print 'no'")
        c = str(input())
        try:
            dia_plotbar(b, c)
        except KeyError:
            print('Input data is incorrect. Please, try againe: ')
            b = list(map(str, input("\nEnter columns: ").strip().split()))
            print("Do you want to group data by date?\n If yes, print 'min', 'max' or 'mean'. \nIf not print 'no'")
            c = str(input())
            dia_plotbar(b, c)
    elif a == 2:
        try:
            dia_pie(b)
        except KeyError:
            print('Input data is incorrect. Please, try againe: ')
            b = list(map(str, input("\nEnter columns: ").strip().split()))
            dia_pie(b)
    elif a == 3:
        try:
            dia_scat(b)
        except KeyError:
            print('Input data is incorrect. Please, try againe: ')
            b = list(map(str, input("\nEnter columns: ").strip().split()))
            dia_scat(b)
    elif a == 4:
        print("Do you want to group data by date?\n If yes, print 'min', 'max' or 'mean'. \nIf not print 'no'")
        c = str(input())
        try:
            dia_box(b, c)
        except KeyError:
            print('Input data is incorrect. Please, try againe: ')
            b = list(map(str, input("\nEnter columns: ").strip().split()))
            print("Do you want to group data by date?\n If yes, print 'min', 'max' or 'mean'. \nIf not print 'no'")
            c = str(input())
            dia_box(b, c)
    elif a == 5:
        print("Do you want to group data by date?\n If yes, print 'min', 'max' or 'mean'. \nIf not print 'no'")
        c = str(input())
        try:
            dia_spaghetti(b, c)
        except KeyError:
            print('Input data is incorrect. Please, try againe: ')
            b = list(map(str, input("\nEnter columns: ").strip().split()))
            print("Do you want to group data by date?\n If yes, print 'min', 'max' or 'mean'. \nIf not print 'no'")
            c = str(input())
            dia_spaghetti(b, c)


def dia_scat(datalist):
    if len(datalist) == 2:
        fig, ax = plt.subplots()
        ax.set_xlabel(datalist[0])
        ax.set_ylabel(datalist[1])
        ax.set_title('Точкова діаграма\n' + datalist[0] + ' - ' + datalist[1])
        ax.scatter(data[datalist[0]], data[datalist[1]])
    elif len(datalist) == 3:
        if data[datalist[2]].dtype == object:
            sns.scatterplot(x=data[datalist[0]], y=data[datalist[1]], alpha=0.5, hue=data[datalist[2]])
        else:
            sns.scatterplot(x=data[datalist[0]], y=data[datalist[1]], size=data[datalist[2]])
    elif len(datalist) == 4:
        if data[datalist[2]].dtype == object:
            sns.scatterplot(x=data[datalist[0]], y=data[datalist[1]], alpha=0.5, hue=data[datalist[2]], size=data[datalist[3]])
        else:
            sns.scatterplot(x=data[datalist[0]], y=data[datalist[1]], size=data[datalist[2]], alpha=0.5, hue=data[datalist[3]])
    plt.legend(title='Точкова діаграма', bbox_to_anchor=(1.05, 1), loc='upper left', ncol = 2)
    plt.title('Scatter plot')
    plt.tick_params(labelrotation=45)
    plt.show()


def dia_plotbar(datalist, c):
    if c == 'no':
        if len(datalist) == 1:
            plt.hist(data[datalist[0]])
            plt.title('Histogram ' + datalist[0])
        else:
            vol = data[datalist]
            vol.plot.bar(colormap = 'plasma')
            plt.title('Histogram ' + datalist[0] + ' ' + datalist[1])
    else:
        if len(datalist) == 1:
            plt.hist(data[datalist[0]])
            plt.title('Histogram ' + datalist[0])
        else:
            vol = data.groupby('Date').agg(dict.fromkeys(datalist, c))
            vol.plot.bar(colormap = 'plasma')
            plt.title('Histogram' + datalist[0] +  ' ' + datalist[1])
    plt.legend(title='Plotbar', bbox_to_anchor=(1.05, 1), loc='upper left', ncol=2)
    plt.tick_params(labelrotation=45)
    plt.show()


def dia_spaghetti(datalist, c):
    vol = data.groupby('Date').agg(dict.fromkeys(datalist, c))
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
    num = 0
    for column in vol:
        num += 1
        plt.plot(vol.index, vol[column], marker='', color=palette(num), label=column)
    plt.legend(title='Spaghetti', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.title('Spagetti')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.tick_params(labelrotation = 45)
    plt.show()


def dia_pie(datalist):
    l = ['' for i in range(len(data["Condition"].unique()))]
    if data[datalist[0]].dtype != object or len(datalist) != 1:
        print('Incorrect data. Please, print just one object-type column')
        c = str(input())
        dia_pie(c)
    else:
        cond = data.groupby(datalist[0]).agg(dict.fromkeys(datalist, 'count'))
        cond.plot.pie(y='Condition', figsize=(10, 10), autopct='%1.f%%', labels = l)
        plt.title('Pie')
        plt.legend(title='Pie', bbox_to_anchor=(1.05, 1), loc='upper left', labels = cond.index)
        plt.show()


def dia_box(datalist, c):
    if len(datalist) == 2:
        if c == 'no':
            sns.boxplot(x = data[datalist[0]], y = data[datalist[1]],palette = 'flare')
        else:
            vol = data.groupby('Date').agg(dict.fromkeys(datalist, c))
            sns.boxplot(x = vol[datalist[0]], y = vol[datalist[1]], palette = 'flare')
    else:
        print('Incorrect data')
    plt.title('Poxplot')
    plt.tick_params(labelrotation=45)
    plt.show()


print('What diagram would you like to choose?\n 1 - histagram\n 2 = pie\n 3 - scatter or bubble\n 4 - box\n 5 - line\n')
a = int(input())
dia_choose(a)