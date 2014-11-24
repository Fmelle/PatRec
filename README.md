PatRec
======

Pattern Recognition Project 18794

Basic Outline
=============

1) Data filtering and selection
	- Pull out the relevant users
	- Generate likeness factor (attractionFactor, digItFactor?)
2) Determine similar users
3) Predict establishment likeness factor for user
4) Recommend an establishment for the specified user

Current JSON Data
=================
- Extracted elite users into _user_reduced_elite__training.json (20054 users) -- Can be used to train characterizing user models
- Extracted all restaurants into _business_reduced_restaurants.json (14303 restaurants)
- Extracted set of sample users (non-elite) into _user_reduced_sample__test.json (2014 users) -- Can be used for testing
- Extracted top 50 reviewers into _user_reduced_top50.json

TODO: Expand Users by mapping Restaurant_Info->Reviews->Users

TODO v2.0
=========
- (IMPORTANT - FRITZ) Get user vector with restaurant types
- (FRITZ) Expand restaurant information with Price Range, Geograpich Information, Average stars (Baseline/Restaurant Prior) -> add this data to the user vector
- (DONE) Predict Rating -> Only for selected user
- (SPENCER) Add prediction baseline where predicted user rating is just restaurant avg
- (DONE) Clean-up validation code
- (GAVI) Incorporate PCA
- (GAVI) Move knn and pca to a similar user class
- Analysis for report: Best K, Best User Features
- Add restuarant data to recommendation

Secondary goals:
================
- DigIt factor (norm. star=star/avg.star)
- Recommendation filter for nearby restaurants
- Implement further intelligent clustering/classification scheme with K-Means/Naïve Bayes/GMM..
