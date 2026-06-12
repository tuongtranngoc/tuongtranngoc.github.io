---
title: "ADAS-3D Object Detection"
date: 2026-05-18
permalink: /posts/2026/3d-lidar-od/
tags:
  - Image Processing
  - Object Detection
  - Computer Vision
  - Deep Learning
---

<head>
    <style type="text/css">
        figure{text-align: center;}
        math{text-align: center;}
    </style>
</head>

Trong bài viết nghiên cứu này, chúng ta sẽ khám phá sâu rộng những khái niệm cơ bản, quá trình huấn luyện, triền khai ứng dụng sử dụng bộ dữ liệu KITTI 360 Vision cho xe tự lái (ADAS) với sự kết hợp giữa camera RGB và LiDAR 3D.

## 3D object detection và 2D object detection

Về bản chất, phát hiện vật thể 3D là quá trình xác định và định vị các vật thể trong không gian ba chiều. Khác với phát hiện 2D — vốn chỉ xét chiều cao và chiều rộng trên mặt phẳng ảnh — phát hiện 3D còn tích hợp thêm chiều sâu, mang lại sự hiểu biết không gian toàn diện. Điều này đặc biệt quan trọng đối với các ứng dụng như xe tự lái, robot, và thực tế tăng cường, nơi mà sự tương tác với môi trường xung quanh diễn ra trong không gian ba chiều.

## Nhận thức chiều sâu (Depth perception) con người và kỹ thuật số

| Human | Digital |
|--|--|
| <img src="/images/posts/2026/3d-lidar-od/vizual-edge-depth-perception-animated.gif"> | <img src="/images/posts/2026/3d-lidar-od/digital-depth-perception.png"> |

Human Depth Perception sử dụng đôi mắt và não bộ — một hệ thống sinh học tự nhiên — để nhận thức độ sâu thông qua các gợi ý thị giác gián tiếp như bóng đổ (shading), phối cảnh (perspective) và thị sai giữa hai mắt (parallax); nói cách khác, não bộ không đo khoảng cách mà suy luận ra độ sâu từ những tín hiệu hình ảnh thu được. Trong khi đó, Digital Depth Perception thay thế đôi mắt bằng cảm biến LiDAR và camera, kết hợp với các thuật toán xử lý để đo trực tiếp khoảng cách — LiDAR bắn tia laser và tính thời gian phản hồi, còn stereo matching tính toán độ lệch giữa hai ảnh để suy ra tọa độ chính xác trong không gian ba chiều. Điểm khác biệt cốt lõi nằm ở chỗ con người nhận thức độ sâu một cách chủ quan và gián tiếp qua kinh nghiệm thị giác, còn máy móc thực hiện điều đó một cách khách quan và trực tiếp qua phép đo toán học.

## Một số khái niệm

### Cảm biến LIDAR
