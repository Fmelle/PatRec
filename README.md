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
- Extracted elite users into _user_reduced_elite.json (20054 users)

TODO: Expand Users by mapping Restaurant_Info->Reviews->Users
Challenge: Reviews count 1.2M objects/reviews with user and business id