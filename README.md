# My Next Pint V2

This is an improved version of a previous prject of the same name where I ask users to input a beer and recommend similar beers based on the reviews and the beer style. In V2, the dataset used to train the model and recommend the beers has 9 million more rows of reviews, allowing more accurate recommendations and a wider library of brews.

I have used PySpark to parse and process the near 3GB of data that reduced processing time by 85% compared to if I used Pandas.

I also use vector embeddings for beer styles to add a dimension of similarity. To avoid performing cosine similarity of 100K beers, which would have created a matrix of size 100K x 100K - I perform K-means clustering and cluster beers into 30+ clusters that would allow for a much faster prcoessing and your computer's processor and memory would thank me. 
