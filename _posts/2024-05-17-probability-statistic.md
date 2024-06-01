---
title: "Probability and Statistics"
date: 2024-05-17
permalink: /posts/2024/probability_statistic/
tags:
  - Mathematics
  - Machine Learning
---

<head>
    <style type="text/css">
        figure{text-align: center;}
        math{text-align: center;}
    </style>
</head>


## Why Probability

Anything that happens in our life is uncertain. There's uncertainty anywhere so whatever you try to do, you need to have some way of dealing or thinking about uncertainty. And the way to do that in a systematic way is using the models that are given to us by **Probability Theory**. So if you're an engineer and you're dealing with some real-world problems. Basically, you're facing noise, noise is random, is uncertain. So, how do you model it? how to you deal with it?

## 1. Probability Models and Aximos

**Sample space ($\Omega$)**
+ Discrete: $\Omega = \lbrace 1, 2, 3, 4, ... \rbrace$
+ Continuous: $\Omega = \lbrace(x, y) | 0 <= x, y <= 1 \rbrace$

**Probaility Aximos**

1. Nonegativity $P(A) >= 0$
2. Normaliztion $P(\Omega)=1$
3. Additivity: If $A \cap B = \varnothing => P(A \cup B)=P(A) + P(B)$
4. If $A_1, A_2, ...$ are disjoint sets. 
$$P(A_1 \cup A_2 \cup ....) = P(A_1) + P(A_2) + ...$$

## 2. Conditioning and Bayes' Rule

**Conditional Probabilty**

<p style="text-align:center;">
  <img src="/images/posts/2024-05-17-probability-statistic/conditional_prob.png">
</p>

$P(A | B)$ : The probability of $A$ given that $B$ occoured

Assuming that $P(B) \neq 0$

$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

$$\Rightarrow P(A \cap B) = P(B). P(A|B)$$

$$=P(A). P(B|A)$$

