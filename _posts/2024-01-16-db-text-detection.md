---
title: 'Scene Text Detection With Differentiable Binarization'
date: 2024-01-16
permalink: /posts/2023/db_textdet/
tags:
  - Mathematics
  - OCR
  - Deep Learning
---

<head>
    <style type="text/css">
        figure{text-align: center;}
        math{text-align: center;}
    </style>
</head>

# Introduction

In the real-world, scene text is often with various scales and shapes, including horizontal, multi-oriented and curved text. 
Segmentation-based scene text detection has attracted a lot of attention in state-of-the-art papers. However, most segmentation-based methods require complex post-processing and take a lot of time in inference phrase. Most existing detection methods use the similar post-processing pipeline as below:

<figure>
    <img src='/images/posts/20230116_differentiable_binarization/tradditional_method.png'>
</figure>

+ First, set a fixed threshold for converting the image into a binary image by a segmentation network.
+ Then, use some heristic techniques like pixel clustering to group pixels into text instances.

To minimize the set a fixed threshold value, we insert the binarization operation into a segmentation network for joint optimization. The standard binarization function is not differentiable, we instead present an approximate function for binarization called Differentiable Binarization (DB), which is fully differentable when training it along with a asegmentation network.

# Binarization

<figure>
    <img src='/images/posts/20230116_differentiable_binarization/binarization_architecture.png'>
</figure>

+ First, the input image is fed into a feature-pyramid backbone.
+ Second, the pyramid features are up-sampled to the same scale and cascaded to produce feature $F$.
+ Then, faeture $F$ is used to predict both the probability map $(P)$ and threshold map $(T)$.
+ After that, the approximate binary map $(B)$ is calculated by $P$ and $T$.

### Standard Binarization

Given a probability map $P \in R^{H\times W}$ produced by a segmentation network, it is converted into a binary map $P \in R^{H\times W}$, with value 1 is considered as valid text areas, otherwise the remaining areas are background with value 0.

$$B_{i, j}=  \left\{\begin{array}{rcl}1 & if &  P_{i, j} >= t, \\
0 & otherwise &
  \end{array}\right.$$

where $t$ is the predefined threshold and $(i, j)$ indicates the coordinate point in the map.

### Differentiable Binarization

For the standard binarization, it is not differentiable to optimize in segmentation network. To solve this problem, we use a approximate binarization function:

$$\hat{B}_{i,j}=\frac{1}{1+e^{-k(P_{i,j}-T_{i,j})}}$$

where $\hat{B}$ is the approximate binarization map. $P, T$ is the probability map and threshold map learned from segmentation network, $k$ indicates the amplifying factor (50 empirically).

*Proof the differentiable of $\hat{B}_{i,j}$ in loss function*

Set $x = P-T$, $f(x)=\hat{B}$ $\rightarrow f(x)=\frac{1}{1+e^{-kx}}$. We must proof the differentiable of $L_{\hat{B}}=logf(x)$

$\frac{\partial L}{\partial x} = \frac{1}{lne} \frac{1}{1+e^{-kx}} (-ke^{-kx})=-ke^{-kx}f(x)$

So, $L_{\hat{B}}$ is differentiable over all $x \in R$

### Adaptive threshold

How to create the text border in final result effectively when probability map can not cover totally text area?


