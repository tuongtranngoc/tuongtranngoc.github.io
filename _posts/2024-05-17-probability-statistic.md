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

Anything that happens in our life is uncertain. There's uncertainty anywhere so whatever you try to do, you need to have some way of dealing or thinking about uncertainty. And the way to do that in a systematic way is using the models that are given to us by **Probability Theory**. So if you're an engineer and you're dealing with some real-world problems. Basically, you're facing **I wonder if the crush loves me**, it is random, is uncertain. So, how do you model it? how to you deal with it?

## 1. Core Probability and Aximos

**Sample space ($\Omega$)**: is the set of all possible outcomes of an experiment.
+ Discrete: $\Omega = \lbrace 1, 2, 3, 4, ... \rbrace$
+ Continuous: $\Omega = \lbrace(x, y)\vert 0 <= x, y <= 1 \rbrace$

**Probaility Aximos**

1. The probability of any event $E$ can be defined as: 
   
   $$P(E) = \lim_{n \rightarrow \infty} \frac{\text{count}(E)}{n}$$

2. Nonegativity: 
   
   $$0 \leq P(E) \leq 1$$

3. All outcomes must be from the Sample Space: 
   
   $$P(\Omega)=1$$

4. The probability of an event from its complement: 
   
   $$P(E) = 1 - P(E^c)$$

5. Probability of **or** with Mututally Exclusive Events: 
   
   $$E_1 \cap E_2 = \varnothing => P(E_1 \cup E_2)=P(E_1) + P(E_2)$$

6. If $E_1, E_2, ..., E_n$ are disjoint sets (mutually exclusive)
   
   $$P(E_1 \cup E_2 \cup .... \cup E_n) = P(E_1) + P(E_2) + ... + P(E_n)=\sum_{i=1}^{n}P(E_i)$$

7. Probability of or (Inclusion-Exclusion): 
   
   $$P(E_1 \cup E_2) = P(E_1) + P(E_2) - P(E_1 \cap E_2)$$

8. Probability of and for independent events: If events are independent, the probability of two events occurring is
   
   $$P(E_1 \cap E_2 ... \cap E_n) = \prod_{i=1}^{n}P(E_i)$$

9.  General Probability of and (The Chain Rule):
   
   $$P(E_1 \cap E_2 ... \cap E_n) = P(E_1). P(E_2 \vert E_1). P(E_3|E_1 \cap E_2) ... P(E_n|E_1\cap ... \cap E_{n-1})$$

10. The Law of Total Probability: For 2 any events $E_1$ and $E_2$:
   
   $$P(E_1) = P(E_1 \cap E_2) + P(E_1 \cap E_2^C)=P(E_1|E_2).P(E_2) + P(E_1|E_2^C).P(E_2^C)$$

11. Bayes' Theory
   
   $$P(B\vert E) = \frac{P(E\vert B). P(B)}{P(E)}$$


### 1.1 Counting

### 1.2 Combinatorics

### 1.3 Definition of Probability

### 1.4 Probability of or

### 1.5 Conditional Probability

**Conditional Probabilty**

<p style="text-align:center;">
  <img src="/images/posts/2024-05-17-probability-statistic/conditional_prob.png">
</p>

$P(A\vert B)$ : The probability of $A$ given that $B$ occured

Assuming that $P(B) \neq 0$

$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

$$\Rightarrow P(A \cap B) = P(B). P(A|B)$$

$$=P(A). P(B|A)$$

Assuming that $P(A \cup B) \neq 0$,

$$P(A \cup B | C) = P(A|C) + P(B|C)$$


Conditioning on multiple events

$$P(A\vert B,C) = \frac{P(A \space \text{and} \space B \vert C)}{P(B \vert C)}$$

### 1.6 Independence

### 1.7 Probability of and

### 1.8 Law of Total Probability

### 1.9 Bayes' Theorem

### 1.10 Log Probabilities


## Reference

1. [Probability For Computer Scientists](https://chrispiech.github.io/probabilityForComputerScientists/en/index.html)
2. [Probabilistic Systems Analysis and Applied Probability](https://www.youtube.com/playlist?list=PLUl4u3cNGP61MdtwGTqZA0MreSaDybji8)