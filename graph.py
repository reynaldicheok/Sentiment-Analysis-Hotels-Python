import pandas as pd
import seaborn as sns
color = sns.color_palette()
import folium
from folium import features


'Histogram'
# fig = px.histogram(df, x='reviews_rating')
# fig.update_layout(title_text='Review rating')
# fig.show()

'Heatmap SG'
# import folium
# from folium.plugins import HeatMap
# from IPython.display import display
# m=folium.Map([1.44255,103.79580],zoom_start=11)
# HeatMap(df2[['latitude','longitude']].dropna(),radius=8,gradient={0.2:'blue',0.4:'purple',0.6:'orange',1.0:'red'}).add_to(m)
#
# m.save('output.html')

'Heatmap US'
# df = pd.read_csv('datafiniti_hotel_reviews (2).csv', encoding = "ISO-8859-1")
#
# import folium
# from folium.plugins import HeatMap
# from IPython.display import display
# m=folium.Map([37.090240,-95.712891],zoom_start=5)
# HeatMap(df[['latitude','longitude']].dropna(),radius=13,gradient={0.2:'blue',0.4:'purple',0.6:'orange',1.0:'red'}).add_to(m)
# m.save('heatmap3.html')
df = pd.read_csv('datafiniti_hotel_reviews (2) - Copy.csv', encoding="ISO-8859-1")
df2 = pd.read_csv('The Showboat Hotel Atlantic City.csv', encoding="ISO-8859-1")
def usheatmap(x,y):

    df1=x
    df2=y

    pointerlatitude = df2['latitude'][0]
    pointerlongitude = df2['longitude'][0]
    pointername = df2['id'][0]

    # Import folium
    # from folium import features

    m = folium.Map(location=[pointerlatitude, pointerlongitude], zoom_start=12)
    mk = features.Marker([pointerlatitude, pointerlongitude])

    popup = "<html></html>" \
            "<body>" + "<p>" + pointername + "</p>" + \
            "<p>Latitude:" + str(pointerlatitude)[0:7] + "</p>" + \
            "<p>Longitude:" + str(pointerlongitude)[0:7] + "</p>" + \
            "</body>"

    pointerlatitude = df2['latitude'][0]
    pointerlongitude = df2['longitude'][0]
    pointername = df2['id'][0]

    folium.Marker([pointerlatitude, pointerlongitude], popup=popup, max_width=len(pointername) * 20,
                  icon=folium.Icon(color='red', icon_color='#FFFF00')).add_to(m)

    differencelatitudep2 = int(float(pointerlatitude)) + 1
    differencelatitudem2 = int(float(pointerlatitude)) - 1
    differencelongitudep2 = int(float(pointerlongitude)) + 1
    differencelongitudem2 = int(float(pointerlongitude)) - 1

    'get unique name of each hotel in area'
    count = 1
    storage = []
    storagecount = []
    for i in range(0, len(df)):
        if (int(df['latitude'][i]) > differencelatitudem2 and int(df['latitude'][i]) < differencelatitudep2) and (
                int(df['longitude'][i]) > differencelongitudem2 and int(df['longitude'][i]) < differencelongitudep2):
            if not storage:
                count -= 1
                addin = df['name'][i], df['latitude'][i], df['latitude'][i], df['reviews_rating'][i]
                storage.append(addin)
                storagecount.append(count)

            if storage[int(count)][0] != df['name'][i]:
                addin = df['name'][i], df['latitude'][i], df['latitude'][i], df['reviews_rating'][i]
                storage.append(addin)
                storagecount.append(count)
                count += 1

    hotel = []
    for i in storage:
        for x in range(0, len(df)):
            if i[0] == df['name'][x]:
                addin = df['name'][x], df['latitude'][x], df['latitude'][x], df['reviews_rating'][x]
                hotel.append(addin)
    score1 = 0
    score2 = 0
    score3 = 0
    score4 = 0
    score5 = 0
    currenthotel = []
    hoteltotalscore = []
    for i in storage:
        if not currenthotel:
            currenthotel.append(i[0])
        for x in hotel:
            if i[0] == x[0]:
                if str(x[3]) == '1.0':
                    score1 += 1
                elif str(x[3]) == '2.0':
                    score2 += 1
                elif str(x[3]) == '3.0':
                    score3 += 1
                elif str(x[3]) == '4.0':
                    score4 += 1
                elif str(x[3]) == '5.0':
                    score5 += 1
        addin = i[0], score1, score2, score3, score4, score5
        hoteltotalscore.append(addin)
        score1 = 0
        score2 = 0
        score3 = 0
        score4 = 0
        score5 = 0

    import altair as alt
    import pandas as pd

    for i in range(0, len(df)):
        if (int(df['latitude'][i]) > differencelatitudem2 and int(df['latitude'][i]) < differencelatitudep2) and (
                int(df['longitude'][i]) > differencelongitudem2 and int(
                df['longitude'][i]) < differencelongitudep2) and (df['name'][i] != pointername):

            for x in hoteltotalscore:
                if df['name'][i] == x[0]:
                    currentscore = [x[1], x[2], x[3], x[4], x[5]]

            source = pd.DataFrame(
                {
                    'Review Rating': ['1', '2', '3', '4', '5'],
                    'Amount of review': currentscore,
                }
            )
            chart = alt.Chart(source).mark_bar().encode(x='Review Rating', y='Amount of review').properties(width=300,
                                                                                                            height=200,
                                                                                                            autosize=alt.AutoSizeParams(
                                                                                                                type='pad',
                                                                                                                contains='padding'))
            vis1 = chart.to_json()

            popup = "<html></html>" \
                    "<body>" + "<p>" + df['name'][i] + "</p>" + \
                    "<p>Latitude:" + str(df['latitude'][i])[0:7] + "</p>" + \
                    "<p>Longitude:" + str(df['longitude'][i])[0:7] + "</p>" + \
                    "<p>Latest Review:" + str(df['reviews_rating'][i]) + "</p>" + \
                    "</body>"
            addtomap = folium.Marker(location=[df['latitude'][i], df['longitude'][i]], tooltip=popup,
                                     popup=folium.Popup(max_width=400).add_child(
                                         folium.VegaLite(vis1, width=600, height=200))).add_to(m)

    m.save('HotelVicinity.html')
    import webbrowser
    webbrowser.open("HotelVicinity.html")

usheatmap(df,df2)
