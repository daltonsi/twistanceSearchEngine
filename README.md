# TWISTANCE Search Engine
## Semester Project for Winter 2017 Information Retrieval Course

Alex Czarnik
czarnika@umich.edu
Information Analysis & Retrieval 

Maria Medlarz
medlarmb@umich.edu
Information Analysis & Retrieval

Shreyas Ramani
ramanis@umich.edu
Health Informatics

Dalton Simancek
simancek@umich.edu
Information Analysis & Retrieval













## 1    INTRODUCTION

Our group took on the problem of official federal government agencies Twitter accounts being taken away by the new administration. Many of the agencies and groups that have had their accounts taken away were those related to science and the environment. In response to this, employees from many of these agencies created rogue ‘alternate’ Twitter accounts on their behalf. Currently there are over seventy such rogue accounts in existence. However, it is hard to know exactly which accounts are ‘official’ rogue accounts, since none of these accounts are verified by Twitter. It is even more difficult to keep track of tweets from all of these accounts since there are so many of them. Following accounts wrongly masquerading as rogue accounts could potentially expose the public to misinformation. In general, this problem boils down to informing the public about current events and happenings in science that they would otherwise have issues finding because they either do not know where to find the information, or the sources they do follow do not report the information accurately. We felt that the best way to address this problem was by building a search engine so that users could search for tweets on a certain topic from these rogue Twitter accounts.












## 2    METHODS 

To begin with, we needed to generate a library of tweets from rogue accounts to query from. The only way to do this was by using the Twitter API to pull all tweets from these accounts and generating a CSV file containing all our tweets of interest. Our next step was to implement a retrieval function to query from the library. We chose to implement a basic TF-IDF function to retrieve results by matching terms from the query to those in the documents. As the documents we were querying were all tweets, they were all quite short, and so just by matching terms we felt that we would be able to obtain relevant results. In order to evaluate our search engine, we decided to calculate precision and recall for a given query and generate a plot. The next step was to build a user interface and put our search engine online. We did this using Python and HTML and the user could enter a phrase or word to search, along with the number of results they wanted, and the function would return the appropriate number of relevant results. 

## 3    RESULTS 

To evaluate the performance of the search engine, we measured the recall and precision for the results of a test query on a subset of the data. A subset of 120 were selected for the testing sample and marked as relevant or not-relevant to the query “Climate Change.” 29 of the 120 tweet sample were marked as relevant to “Climate Change.” Our search engine used the test query “Climate Change” to retrieve all of the tweets in the test sample in order of scored relevance.



![alt text](https://github.com/daltonsi/twistanceSearchEngine/blob/master/climate_change_pr_plot.png?raw=true)

Precision and Recall were calculated, recorded and plotted after every new tweet retrieved (See Figure 1). A line of best fit was added to show an overall trend. We also noted that precision and recall shared a score of 0.7931 after 29 tweets had been retrieved. 

## 4    DISCUSSION

Our results demonstrate a well-functioning retrieval system for the sample query of “Climate Change.” However, it should be noted that “Climate Change” is a particularly relevant political topic with a strong presence in the rogue twitter accounts. Queries outside of the current political hot topics will generate few or no relevant results. TF-IDF is an appropriate measure for capturing the key terms of political hot topics, but the system weakens as queries deviate from the core topics of the tweets. Applying smoothing techniques and expanding the document collection to other twitter accounts, websites and feed would expand the information base and offer more opportunities for indexing and retrieving a wider base of rogue news.

## 5    CONCLUSION

As a final deliverable, our group hosted an open source tool on GitHub (link included in the references) with an instruction manual on how to download and run it.1 We felt that an open source downloadable tool would be a better way to host our tool than an online search engine as we would be able to regularly update our tweet library and would not have issues with the large file. Additionally, users would be able to use our tool offline after downloading the code and the library from GitHub initially. During the course of this project, we learned that a simple retrieval function, either including only term frequency and inter document frequency (TF-IDF) without any weighting portion, or a more advanced function such as BM-25 were sufficient for generating precise and relevant results when querying from a library of tweets. The likely reason for this is that tweets are very short documents, so finding relevant results just by matching terms in the query to those in the document reliably does not require an advanced retrieval function. Additionally, we learned of the difficulties in creating a search engine for tweets. Keeping our library updated requires constantly running the Twitter API in the background to load the latest tweets. As with our search engine you are querying a static library, this is a limitation of our project. Lastly, our search engine had issues processing queries that are not relevant. For example, if you search a topic such as forest fires, or healthcare research, our search engine will be able to return relevant results. However, if you search for show times for a movie, for example, our search engine will do its best to return results, but the results will likely not be relevant to the query. 





6    FUTURE STEPS 

One possible future project could be to find a way to filter out non-relevant queries. For example, we could set a minimum TF-IDF score required to return a document as a result of a query, and assume that any query not having a result that meets this minimum score is not-relevant. As another future project, we would find a way for our search engine to query a dynamic library of tweets instead of a static library. Additionally, we could look into links, images and videos, embedded in tweets to results instead of just the tweets themselves. Doing this would require using BeautifulSoup to parse the HTML links and search them for query terms. Given the vast possibilities of what a link could lead to, finding a way to parse all of these pages would be a large project itself. Another possible future direction would be to further optimize our search engine using methods such as smoothing. As we are currently only querying tweets themselves, extensive optimization was not really necessary given the quality of our initial results. But, as we expand the search engine to query links, images, and videos as well, further optimization would likely be necessary. Our project was reasonably successful given its limitations, and there are plenty of future directions in which we could advance our search engine. 

## 7    REFERENCES
[1] https://github.com/daltonsi/twistance_search_
engine
