---
title: "Instance Segmentation"
date: 2024-06-02
permalink: /posts/2024/instancesegmentation/
tags:
  - Mathematics
  - Machine Learning
  - Computer Vision
  - Object Detection
---

<head>
    <style type="text/css">
        figure{text-align: center;}
        math{text-align: center;}
    </style>
</head>


## Introduction

**Instance Segmentation** is a task in Computer Vision. Unlike the *object detection* algorithms, where the goal is to localize and classify individual objects using bounding box, and *semantic segmentation*, where the goal is to classify each pixel into a fixed set of categories without differentiating object instances. 

**Instance Segmentation** requires the correct deection of all objects in an image while also precisely segmenting each instance.

<p style="text-align:center;">
  <img src="/images/posts/20240602_maskrcnn/maskrcnn.jpg">
</p>

## Region of Intersect (RoI)
