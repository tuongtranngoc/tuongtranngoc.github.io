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

$$y=\sum_jw_jx_j+b$$

and the most loss function is the squared error, defined as

$$L(y, t)=\frac{1}{2}(y-t)^2$$

Expand with x

