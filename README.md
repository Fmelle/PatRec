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
- Get user vector with restaurant types (Also average stars (User prior) and secondary user rating -> DigIt factor (norm. star=star/avg.star))
- Expand restaurant information with Price Range, Geograpich Information, Average stars (Baseline/Restaurant Prior)
- Predict Rating -> Only for selected user, add baseline
- Possible Analysis for report: Best K, Best User Features
- Introduce Basline in prediction model
- Validation -> Predict whole user vector / As much as possible and add up MSE for each recommendation towards GT wherever possible.

Secondary goals:
================
- DigIt factor
- Recommendation filter for close /lookup restaurant
- Implement further intelligent clustering/classification scheme with K-Means/Naïve Bayes/GMM..
