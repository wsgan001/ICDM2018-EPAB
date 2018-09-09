# ICDM2018-EPAB
<strong>Conference: IEEE International Conference on Data Mining (Singapore) - ICDM2018 (accepted)</strong><br>
<strong>Author</strong>: Qitian Wu, <a href="http://chaoqiyang.com">Chaoqi Yang</a>, Xiaofeng Gao, Peng He, Guihai Chen<br>
<strong>Title</strong>: EPAB: Early Pattern Aware Bayesian Model for Social Content Popularity Prediction<br><br>
<img src="ICDM_cover.png"><br><br>
## Brief Model
#### (1). The early pattern of each cascade is represent as a vector:<br>
<img src="formula1.png"><br>
#### cluster the early pattern
<img src="pattern.png"><br>
#### (2). We introduce three hidden variable to capture describe the state of each cascade.<br>
- Influence(h1): how many people have been influenced by this tweet.
- Attractiveness(h2): how many people tend to click and repost this tweet.
- Potentiality(h3): how many people will be exposed to this tweet.
<img src="formula2.png">
#### optimize the loss function between ground truth and predicted value, get alpha, beta, gamma for each pattern, and h1, h2, h3 for each cascade.
<img src="formula3.png">
<img src="formula4.png">
<img src="formula5.png">
<img src="formula6.png">
