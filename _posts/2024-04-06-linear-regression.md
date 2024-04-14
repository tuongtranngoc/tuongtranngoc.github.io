---
title: "Linear Regression"
date: 2024-04-06
permalink: /posts/2024/linear_regression/
tags:
  - Mathematics
  - Optimization
---

<head>
    <style type="text/css">
        figure{text-align: center;}
        math{text-align: center;}
    </style>
</head>


### Problem

In order to formulate a learning problem mathematically, we need to define two things:
+ **Model**: defines the set of allowable hypotheses, or functions that compute predictions from the inputs
+ **Loss function**: which says how far off the prediction is from the target

**Linear Regression** is both simplest and most popular algorithm for tackling regression problems. Mathematically, this is written as:

$$y=\sum_iw_ix_i+b$$

and the most loss function is the squared error, defined as

$$L(w, b)=\frac{1}{2}(y-\hat{y})^2$$

Expand with $x \in R^{n}$

$$L(w,b) = \frac{1}{n} \sum_{i=1}^n\frac{1}{2}(w_ix_i + b - \hat{y_i})^2=\frac{1}{2}||y-Xw||_2^2$$

When training the model, we must seek parameters $(w, b)$ that minimize the total loss across all training samples:
$$w^*, b^* = \argmin_{w, b} L(w, b)$$

### Solution

#### 1. Derivative of the loss

$$\frac{\partial L}{\partial w}=X^T(Xw-y)=0$$

$$X^TXw = X^Ty$$

$$w=(X^TX)^{-1}X^Ty$$

#### 2. SGD

#### 3. Vectorization