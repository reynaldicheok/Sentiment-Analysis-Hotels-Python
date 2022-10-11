import pandas as pd
import seaborn as sns

color = sns.color_palette()
import folium
from folium.plugins import HeatMap

import branca.colormap
from collections import defaultdict


# User input
df01 = pd.read_csv('datafiniti_hotel_reviews (2) - Copy.csv', encoding="ISO-8859-1")
df02 = pd.read_csv('The Showboat Hotel Atlantic City.csv', encoding="ISO-8859-1")

'Histogram'


# fig = px.histogram(df, x='reviews_rating')
# fig.update_layout(title_text='Review rating')
# fig.show()

# Heatmap of either US or SG
def heatmap(x):
    df = x
    # Heatmap SG
    # m = folium.Map([1.44255, 103.79580], zoom_start=11)
    # HeatMap(df2[['latitude', 'longitude']].dropna(), radius=8,
    #         gradient={0.2: 'blue', 0.4: 'purple', 0.6: 'orange', 1.0: 'red'}).add_to(m)
    # m.save('output.html')

    # Heatmap US
    m = folium.Map([37.090240, -95.712891], zoom_start=5)
    steps = 20
    colormap = branca.colormap.linear.YlOrRd_09.scale(0, 1).to_step(steps)
    gradient_map = defaultdict(dict)
    for i in range(steps):
        gradient_map[1 / steps * i] = colormap.rgb_hex_str(1 / steps * i)

    HeatMap(df[['latitude', 'longitude']].dropna(), radius=13,
            gradient={0.2: 'blue', 0.4: 'purple', 0.6: 'orange', 1.0: 'red'}).add_to(m)
    colormap.add_to(m)
    m.save('USHeatMap.html')
    # webbrowser.open('USHeatMap.html')
    heatmapname = 'USHeatMap.html'
    return heatmapname


# Hotel Vicinity function
def ushotelvicinitymap(x, y):
    df = x
    df2 = y
    # Get and set scrapped excel values
    pointerlatitude = df2['latitude'][0]
    pointerlongitude = df2['longitude'][0]
    pointername = df2['id'][0]

    # plot where map will look
    m = folium.Map(location=[pointerlatitude, pointerlongitude], zoom_start=12)

    # Hotel details
    popup = "<html></html>" \
            "<body>" + "<p>" + pointername + "</p>" + \
            "<p>Latitude:" + str(pointerlatitude)[0:7] + "</p>" + \
            "<p>Longitude:" + str(pointerlongitude)[0:7] + "</p>" + \
            "</body>"

    pointerlatitude = df2['latitude'][0]
    pointerlongitude = df2['longitude'][0]
    pointername = df2['id'][0]

    # Plot marker for scraped hotel, in red
    folium.Marker([pointerlatitude, pointerlongitude], popup=popup, max_width=len(pointername) * 20,
                  icon=folium.Icon(color='red', icon_color='#FFFF00')).add_to(m)

    # Get +-  lat/long of scraped hotel
    differencelatitudep2 = int(float(pointerlatitude)) + 1
    differencelatitudem2 = int(float(pointerlatitude)) - 1
    differencelongitudep2 = int(float(pointerlongitude)) + 1
    differencelongitudem2 = int(float(pointerlongitude)) - 1

    # get unique name of each hotel in area
    count = 1
    storage = []
    storagecount = []
    for i in range(0, len(df)):
        if (int(df['latitude'][i]) > differencelatitudem2 and int(df['latitude'][i]) < differencelatitudep2) and (
                int(df['longitude'][i]) > differencelongitudem2 and int(df['longitude'][i]) < differencelongitudep2):
            if not storage:
                count -= 1
                addin = df['name'][i], df['latitude'][i], df['longitude'][i], df['reviews_rating'][i], \
                        df['reviews_text'][i]
                storage.append(addin)
                storagecount.append(count)

            if storage[int(count)][0] != df['name'][i]:
                addin = df['name'][i], df['latitude'][i], df['longitude'][i], df['reviews_rating'][i], \
                        df['reviews_text'][i]
                storage.append(addin)
                storagecount.append(count)
                count += 1

    hotel = []
    for i in storage:
        for x in range(0, len(df)):
            if i[0] == df['name'][x]:
                addin = df['name'][x], df['reviews_rating'][x], df['reviews_text'][x]
                hotel.append(addin)

    score1 = 0
    score2 = 0
    score3 = 0
    score4 = 0
    score5 = 0
    hoteltotalscore = []
    for i in storage:
        for x in hotel:
            if i[0] == x[0]:
                if int(float(x[1])) < 2:
                    score1 += 1
                elif int(float(x[1])) < 3:
                    score2 += 1
                elif int(float(x[1])) < 4:
                    score3 += 1
                elif int(float(x[1])) < 5:
                    score4 += 1
                elif int(float(x[1])) < 6:
                    score5 += 1
        addin = i[0], score1, score2, score3, score4, score5
        hoteltotalscore.append(addin)
        score1 = 0
        score2 = 0
        score3 = 0
        score4 = 0
        score5 = 0

    pointerlowreviewtext = ''
    pointerhighreviewtext = ''
    highreviewtext = ''
    lowreviewtext = ''
    import altair as alt
    import pandas as pd
    # Loop through master excel file, check if nearby hotels with required lat/long
    for i in range(0, len(df)):
        if (int(df['latitude'][i]) > differencelatitudem2 and int(df['latitude'][i]) < differencelatitudep2) and (
                int(df['longitude'][i]) > differencelongitudem2 and int(
            df['longitude'][i]) < differencelongitudep2) and (df['name'][i] != pointername):
            if (not highreviewtext) and (not lowreviewtext):
                for x in hotel:
                    if x[0] == df['name'][i]:
                        if int(x[1]) > 4:
                            highreviewtext = x[2]
                            reviewscore = x[1]
                        elif int(x[1]) > 3:
                            highreviewtext = x[2]
                            reviewscore = x[1]
                        elif int(x[1]) > 2:
                            highreviewtext = x[2]
                            reviewscore = x[1]
                        elif int(x[1]) > 1:
                            highreviewtext = x[2]
                            reviewscore = x[1]
                        elif int(x[1]) == 0:
                            highreviewtext = x[2]
                            reviewscore = x[1]
                    if x[0] == pointername:
                        if int(x[1]) > 4:
                            pointerhighreviewtext = x[2]
                            pointerreviewscore = x[1]
                        elif int(x[1]) > 3:
                            pointerhighreviewtext = x[2]
                            pointerreviewscore = x[1]
                        elif int(x[1]) > 2:
                            pointerhighreviewtext = x[2]
                            pointerreviewscore = x[1]
                        elif int(x[1]) > 1:
                            pointerhighreviewtext = x[2]
                            pointerreviewscore = x[1]
                        elif int(x[1]) == 0:
                            pointerhighreviewtext = x[2]
                            pointerreviewscore = x[1]

            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
              <script src="https://cdn.jsdelivr.net/npm/vega@{vega_version}"></script>
              <script src="https://cdn.jsdelivr.net/npm/vega-lite@{vegalite_version}"></script>
              <script src="https://cdn.jsdelivr.net/npm/vega-embed@{vegaembed_version}"></script>
              <style>
                table, td, th {{  
                font-family: Verdana, sans-serif;

                text-align: center;
                }}

                table {{
                border-collapse: collapse;
                width: 100%;
                    }}

                th, td {{
                padding: 15px;
                }}
                </style>
            </head>
            <body>
            <table>
            <tr>
            <th><h3>""" + pointername + """</h3></th>
            <th><h3>""" + df['name'][i] + """</h3></th>
            </tr>
            <tr>
            <td><table><tr><th>Latitude</th><th>Longitude</th></tr><tr><td>""" + str(pointerlatitude)[
                                                                                 0:7] + """</td><td>""" + str(
                pointerlongitude)[0:7] + """</td></tr></table></td>
            <td><table><tr><th>Latitude</th><th>Longitude</th></tr><tr><td>""" + str(df['latitude'][i])[
                                                                                 0:7] + """</td><td>""" + str(
                df['longitude'][i])[0:7] + """</td></tr></table></td>
            <td></td>
            </tr>
            <tr>
            <td><div id="vis0"></div></td>
            <td><div id="vis1"></div></td>
            </tr>
            <tr>
            <td><div id="vis2"></div></td>
            <td><div id="vis3"></div></td>
            </tr>
            <tr>
            <td><table><tr><th>Latest Review</th><th>Rating</th></tr><tr><td>""" + pointerhighreviewtext + """</td><td>""" + str(
                pointerreviewscore) + """</td></tr></table></td>
            <td><table><tr><th>Latest Review</th><th>Rating</th></tr><tr><td>""" + highreviewtext + """</td><td>""" + str(
                reviewscore) + """</td></tr></table></td>
            </tr>  
            </table>
            <table>
            <tr>
            <th>
            Comparing hotels
            </th>
            </tr>
            <tr><td>
            <div id="vis4"></div>   
            </td><tr>
            </table>
            <script type="text/javascript">
              vegaEmbed('#vis0', {spec0}).catch(console.error);
              vegaEmbed('#vis1', {spec1}).catch(console.error);
              vegaEmbed('#vis2', {spec2}).catch(console.error);
              vegaEmbed('#vis3', {spec3}).catch(console.error);
              vegaEmbed('#vis4', {spec4}).catch(console.error);
            </script>
            </body>
            </html>
            """

            tooltip = "<html></html>" \
                      "<body>" + "<p>" + df['name'][i] + "</p>" + \
                      "<p>Latitude:" + str(df['latitude'][i])[0:7] + "</p>" + \
                      "<p>Longitude:" + str(df['longitude'][i])[0:7] + "</p>" + \
                      "<p>Latest Review:" + str(df['reviews_rating'][i]) + "</p>" + \
                      "</body>"

            for x in hoteltotalscore:
                if pointername == x[0]:
                    currentscore1 = [x[1], x[2], x[3], x[4], x[5]]

            for x in hoteltotalscore:
                if df['name'][i] == x[0]:
                    currentscore2 = [x[1], x[2], x[3], x[4], x[5]]

            # Plot dataframe/bargraph
            source0 = pd.DataFrame(
                {
                    'Review Rating': ['1', '2', '3', '4', '5'],
                    'Amount of review': currentscore1,
                }
            )
            source1 = pd.DataFrame(
                {
                    'Review Rating': ['1', '2', '3', '4', '5'],
                    'Amount of review': currentscore2,
                }
            )

            source2 = pd.DataFrame(
                {
                    'Review Rating': ['1', '2', '3', '4', '5'],
                    'Input Hotel': [currentscore1[0], currentscore1[1], currentscore1[2], currentscore1[3],
                                    currentscore1[4]],
                    df['name'][i]: [currentscore2[0], currentscore2[1], currentscore2[2], currentscore2[3],
                                    currentscore2[4]],

                }
            )

            chart0 = alt.Chart(source0).mark_bar().encode(x='Review Rating', y='Amount of review').properties(width=300,
                                                                                                              height=200,
                                                                                                              autosize=alt.AutoSizeParams(
                                                                                                                  type='pad',
                                                                                                                  contains='padding'))
            chart1 = alt.Chart(source1).mark_bar().encode(x='Review Rating', y='Amount of review').properties(width=300,
                                                                                                              height=200,
                                                                                                              autosize=alt.AutoSizeParams(
                                                                                                                  type='pad',
                                                                                                                  contains='padding'))
            chart2 = alt.Chart(source0).mark_arc().encode(
                theta=alt.Theta(field="Amount of review", type="quantitative"),
                color=alt.Color(field="Review Rating", type="nominal")).properties(width=300, height=200,
                                                                                   autosize=alt.AutoSizeParams(
                                                                                       type='pad', contains='padding'))
            chart3 = alt.Chart(source1).mark_arc().encode(
                theta=alt.Theta(field="Amount of review", type="quantitative"),
                color=alt.Color(field="Review Rating", type="nominal")).properties(width=300, height=200,
                                                                                   autosize=alt.AutoSizeParams(
                                                                                       type='pad', contains='padding'))
            chart4 = alt.Chart(source2).mark_bar().encode(x='Amt of Reviews:Q', y='score:N', color='score:N',
                                                          row=alt.Row('Review Rating',
                                                                      sort=['1', '2', '3', '4', '5'])).transform_fold(
                as_=['score', 'Amt of Reviews'], fold=['Input Hotel', df['name'][i]]).properties(width=700,
                                                                                                 autosize=alt.AutoSizeParams(
                                                                                                     type='pad',
                                                                                                     contains='padding'))

            charts_code = html_template.format(
                vega_version=alt.VEGA_VERSION,
                vegalite_version=alt.VEGALITE_VERSION,
                vegaembed_version=alt.VEGAEMBED_VERSION,
                spec0=chart0.to_json(indent=None),
                spec1=chart1.to_json(indent=None),
                spec2=chart2.to_json(indent=None),
                spec3=chart3.to_json(indent=None),
                spec4=chart4.to_json(indent=None),
            )
            iframe = branca.element.IFrame(html=charts_code, width=1100, height=800)
            popup = folium.Popup(iframe, max_width=1100, max_height=800)
            folium.Marker(location=[df['latitude'][i], df['longitude'][i]], tooltip=tooltip, popup=popup).add_to(m)
            highreviewtext = ''
            lowreviewtext = ''

            # chart = alt.Chart(source).mark_bar().encode(x='Review Rating', y='Amount of review').properties(width=300,height=200,autosize=alt.AutoSizeParams(type='pad',contains='padding'))
            # vis1 = chart.to_json()

            # popup = "<html></html>" \
            #         "<body>" + "<p>" + df['name'][i] + "</p>" + \
            #         "<p>Latitude:" + str(df['latitude'][i])[0:7] + "</p>" + \
            #         "<p>Longitude:" + str(df['longitude'][i])[0:7] + "</p>" + \
            #         "<p>Latest Review:" + str(df['reviews_rating'][i]) + "</p>" + \
            #         "</body>"

            # addtomap = folium.Marker(location=[df['latitude'][i], df['longitude'][i]], tooltip=popup,popup=folium.Popup(max_width=400).add_child(folium.VegaLite(vis1, width=600, height=200))).add_to(m)

    m.save(pointername + ' HotelVicinity2.html')
    # webbrowser.open(pointername + ' HotelVicinity2.html')
    hotelvicinityname = pointername + ' HotelVicinity2.html'
    return hotelvicinityname


# def reviewfilter(x,y):
#     df=x
#     filteredreview=[]
#     selectedword=y
#     count=0
#     for i in range(0, len(df)):
#         if selectedword in str(df['reviews_text'][i]):
#             addin=df['name'][i],df['reviews_text'][i]
#             filteredreview.append(addin)
#     return filteredreview


# Output file names, heatmap ontop hotelvicnity below

# heatmapname = heatmap(df01)
hotelvicinityname = ushotelvicinitymap(df01, df02)
# filtered = reviewfilter(df01,'staff')
