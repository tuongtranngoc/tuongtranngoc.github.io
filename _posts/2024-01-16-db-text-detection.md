---
title: 'Sence Text Detection With Differentiable Binarization'
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

In the real-world, sence text is often with various scales and shapes, including horizontal, multi-oriented and curved text. 
Segmentation-based sence text detection has attracted a lot of attention in state-of-the-art papers. However, most segmentation-based methods require complex post-processing and take a lot of time in inference phrase. Most existing detection methods use the similar post-processing pipeline as below:

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

