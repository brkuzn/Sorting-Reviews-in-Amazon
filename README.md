# Sorting Reviews in Amazon
Our goal in this project is to properly rank ratings and comments on an SD card. We'll use Amazon data. We'll sort user reviews by time weighted average and wilson lower bound method.
*********************************************************************************
**Dataset

This dataset contains amazon product information and various metadata.It includes product with the most comments in the electronics category and its ratings and reviews.
*********************************************************************************
VARIABLES
*********************************************************************************
reviewerID <- UserID
*********************************************************************************
asin <- ProductID
*********************************************************************************
reviewerName <- Username
*********************************************************************************
helpful <- likes and dislikes[x,y]
*********************************************************************************
reviewText <- user-written review
*********************************************************************************
overall <- rating value of the product
*********************************************************************************
summary <- summary of the review text
*********************************************************************************
unixReviewTime <- user's rating time by unix time
*********************************************************************************
reviewTime <- user's rating time (raw)
*********************************************************************************
day_diff <- Number of days since review
*********************************************************************************
helpful_yes <- number of likes the review received
*********************************************************************************
total_vote <- total vote
