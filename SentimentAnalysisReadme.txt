read_csv(filename) : This function is for user to input their local file locations of the scraped data or any hotel data
		     The function will then read and return a dataframe variable for the sentimental analysis

generate_graph(csv_file): function used for data visualization of the overall review score of all the hotel to give
			  an overview of the whole situation

generate_stopword(csv_df): function used to generate the a word cloud via a series of stopwords, can be updated
			   to exclude certain words to make it more accurate

remove_punctuation(text): removes punctuation in text and returns an output without punctuation for sentiment
			  analysis though is redudant with vader lexicon

generate_dataframe_column(dataframe_input): generates the compound column in this dataframe using the vader lexicon
					    on the review text to determine how positive or negative the review is

getAnalysis(score): function to return in english based on the score whether its good bad or neutral

breakdown_dataframe(new_dataframe): With reference to the generate_dataframe_column function, use this after using that
				    to further breakdown the dataframe to return it in a more readible format

export_csv(dataframe): Use to export the dataframe into CSV file saved locally. Recommend to use after breakdown_dataframe function
		       though can be used for any dataframe

wordcloud_gen(dataframe): Use to generate positive and negative word cloud based on the dataframe