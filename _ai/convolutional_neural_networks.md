---
title: "Convolutional Neural Networks (CNN)"
order: 2
description: "Convolutions, pooling, and the architectures that learn to see."
---

> *Coming soon* — this chapter will cover the core ideas behind convolutional
> neural networks, the architectures that drove the deep learning revolution
> in computer vision.

## Overview

Convolutional Neural Networks (CNNs) are a family of deep neural networks
designed to process data with a grid-like topology — most notably images.
By exploiting local connectivity, weight sharing, and translation
equivariance, CNNs learn hierarchies of features that progress from edges
and textures to objects and scenes.

## What you'll learn

- The convolution operation, kernels, stride, padding, and receptive fields
- Pooling, normalization, and activation functions in vision networks
- Classic architectures: LeNet, AlexNet, VGG, GoogLeNet/Inception, ResNet
- Modern variants: DenseNet, MobileNet, EfficientNet, ConvNeXt
- Beyond classification: detection, segmentation, and dense prediction
- Practical training: data augmentation, transfer learning, regularization

## Why it matters

CNNs are the workhorse of computer vision and remain a strong baseline for
many perception tasks even in the era of Transformers. Understanding their
inductive biases — locality and translation equivariance — is essential to
choosing the right model and reasoning about what a network can and cannot
learn from limited data.
