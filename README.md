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

Additionally we will work on validation

TODO
====
- Extract top 50 reviewers
- Users Vect: Votes, num reviews, average stars, compliments
- Users to reviews: stars

Current JSON Data
=================
- Extracted elite users into _user_reduced_elite__training.json (20054 users) -- Can be used to train characterizing user models
- Extracted all restaurants into _business_reduced_restaurants.json (14303 restaurants)
- Extracted set of sample users (non-elite) into _user_reduced_sample__test.json (2014 users) -- Can be used for testing
- Extracted top 50 reviewers into _user_reduced_top50.json

TODO: Expand Users by mapping Restaurant_Info->Reviews->Users
Challenge: Reviews count 1.2M objects/reviews - elite users has ~200 reviews each