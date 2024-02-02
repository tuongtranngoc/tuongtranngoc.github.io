---
title: "Transformer: Attention is All You Need"
date: 2024-01-21
permalink: /posts/2024/transformer/
tags:
  - Mathematics
  - Natural Language Processing 
  - Deep Learning
---

<head>
    <style type="text/css">
        figure{text-align: center;}
        math{text-align: center;}
        {font-size: 0.8em;} 
    </style>
</head>

## Introduction

**Transformer** is a term that everyone also must understand first if they want to dive into Large Language Model, but I happened to read about LayoutLM, BERT term first. After that, I returned Transformer to understand how it works. Unlike the tasks in Computer Vision, for me, LLM is actually much more difficult to approach and takes a lot of time to read papers, mathematics understanding and code implementation. 

In the blog, let's learn about design, mathematical models and their applications. In the other blog on Harvard NLP also provides detail explanation with code implementation.

## Model Architecture
Transformer model has an encoder-decoder structure:

Given a input sequence of symbol representations 

$$X = (x_1, x_2, ..., x_n)$$

The encoder will map X to sequence of countinuous representations 

$$Z=(z_1, z_2, ..., z_n)$$

Given $Z$, the decoder then generates an output sequence $Y=(y_1, y_2, ..., y_m)$ of symbols of one element at a time. At each step the model is auto-regressive, consuming the previously generated symbols as additional input when generating the next.

Next, we go to the detailed components of the architecture in Transformer.

<p align="center">
  <img src="/images/posts/transformer/Transformer_model_architecture.png" width=300px>
</p>

### Encoder

The encoder is composed of a stack $N=6$ identical layers. At each layer includes two sub-layer:
+ Multi-Head Self-Attention and Add & Norm
+ Feed Forward and Add & Norm

**Add & Norm Layer** is a component followed by layer normalization and the output of each sub-layer is: 

$$LN(x + S(x))$$

where $S(x)$ is the function implemented by the sub-layer itself, $LN$ is layer normalization.

**Attention** is function can be described mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors. Assume that, the input consists of queries and keys of dimemsion $d_k$, and values of dimension $d_v$. 

<p align="center">
  <img src="/images/posts/transformer/scaled_dot_product_attention.png" width=150px>
</p>

The output of Attention is computed by the Scaled Dot-Product Attention:

$$\text{Attention}(Q, K, V)=\text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$$

Code implementation:

```python
<p style="font-size: 32px;">
def masked_softmax(X, valid_lens):
    """Perform softmax operation by masking elements on the last axis.

    Defined in :numref:`sec_attention-scoring-functions`"""
    # X: 3D tensor, valid_lens: 1D or 2D tensor
    def _sequence_mask(X, valid_len, value=0):
        maxlen = X.size(1)
        mask = torch.arange((maxlen), dtype=torch.float32,
                            device=X.device)[None, :] < valid_len[:, None]
        X[~mask] = value
        return X

    if valid_lens is None:
        return nn.functional.softmax(X, dim=-1)
    else:
        shape = X.shape
        if valid_lens.dim() == 1:
            valid_lens = torch.repeat_interleave(valid_lens, shape[1])
        else:
            valid_lens = valid_lens.reshape(-1)
        # On the last axis, replace masked elements with a very large negative
        # value, whose exponentiation outputs 0
        X = _sequence_mask(X.reshape(-1, shape[-1]), valid_lens, value=-1e6)
        return nn.functional.softmax(X.reshape(shape), dim=-1)

class DotProductAttention(nn.Module):
    """Scaled dot product attention.

    Defined in :numref:`subsec_batch_dot`"""
    def __init__(self, dropout):
        super().__init__()
        self.dropout = nn.Dropout(dropout)

    # Shape of queries: (batch_size, no. of queries, d)
    # Shape of keys: (batch_size, no. of key-value pairs, d)
    # Shape of values: (batch_size, no. of key-value pairs, value dimension)
    # Shape of valid_lens: (batch_size,) or (batch_size, no. of queries)
    def forward(self, queries, keys, values, valid_lens=None):
        d = queries.shape[-1]
        # Swap the last two dimensions of keys with keys.transpose(1, 2)
        scores = torch.bmm(queries, keys.transpose(1, 2)) / math.sqrt(d)
        self.attention_weights = masked_softmax(scores, valid_lens)
        return torch.bmm(self.dropout(self.attention_weights), values)
</p>
```

**Multi-Head Attention** allows the model to jointly attend to information from different representation subspaces at different positions.