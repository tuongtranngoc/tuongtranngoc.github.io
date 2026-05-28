---
title: "Convolutional Neural Networks (CNN)"
order: 2
description: "Convolutions, pooling, and the architectures that learn to see."
---

## 1. Tổng quan

Dữ liệu ảnh được biểu diễn dưới dạng ma trận hai chiều gồm các pixel, bất kể là ảnh đơn sắc (monochromatic) hay ảnh màu. Bởi cấu trúc phong phú này mà việc xử lý ảnh như những vector số bằng cách flattening sẽ không tận dụng về quan hệ không gian (spatial relation) giữa các pixel. Ví dụ đưa ảnh về vector 1 chiều sau đó cho đi qua một MLP fully connected, điều này sẽ thu được kết quả tương tự nhau dù ta có giữ nguyên hay hoán vị các cột, hàng của ma trận trước khi fitting các tham số của MLP.

Bằng cách tận dụng tính chất không gian của ảnh, các pixel ở gần nhau thường có liên kết với nhau. Ví dụ: vùng pixel tạo nên con mắt, cái tai, lông trắng trên bụng mèo sẽ nằm sát và có màu sắc gần giống nhau và liền kề. Khác với MLP, CNN sẽ khai thác và học từ ảnh hiệu quả hơn rất nhiều.


## 2. Từ Fully Connected layers đến Convolutions


