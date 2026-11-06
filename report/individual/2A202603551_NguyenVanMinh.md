# Báo cáo cá nhân — Day 01: Lọc tin nhắn rác bằng ML, DL, Embedding và LLM

- **MSSV:** 2A202603551
- **Họ và tên:** Nguyễn Văn Minh
- **SEED:** 4525

*Bản nháp báo cáo bằng tiếng Việt, được AI biên soạn từ kết quả trong notebook. Cần đọc lại và hoàn thiện các phần yêu cầu tự làm trước khi nộp.*

## 1. Bằng chứng

| File | Present? |
| --- | --- |
| [`day01_lab.ipynb`](day01_lab.ipynb) — notebook đã chạy và lưu output | Có, 15/15 kiểm tra trong notebook đạt |
| [`lab1_report.json`](lab1_report.json) — báo cáo kết quả tự sinh | Có |
| [`hand_calc.jpg`](hand_calc.jpg) — ảnh tính tay có các bước | Có tệp, cần xác nhận đúng là ảnh viết tay thật |

Sau khi bỏ tin trùng, dữ liệu còn **5.169 tin nhắn**, gồm **653 spam** và **4.516 ham**. Theo SEED 4525, chia thành **3.619 train**, **775 validation**, **775 test**; SUB 40 lấy 20 spam và 20 ham từ test.

## 2. Kết quả chính

| Phương pháp | F1 test | F1 SUB 40 | p95 ms/tin | USD/1.000 tin (API) |
| --- | ---: | ---: | ---: | ---: |
| BoW + Logistic Regression | 0,865 | 0,788 | 0,034 | 0 |
| BoW + MLP | 0,924 | 0,889 | 0,167 | 0 |
| MiniLM + kNN | 0,880 | 0,974 | 18,176 | 0 |
| MiniLM + Logistic Regression | 0,954 | 1,000 | 15,507 | 0 |
| MiniLM + MLP head | 0,964 | 1,000 | 15,515 | 0 |

MiniLM + MLP head có F1 test cao nhất (**0,964**); MiniLM + Logistic Regression đạt **0,954** nhưng thể hiện tốt hơn trên tập khó. Chi phí API bằng 0 của năm cách chạy cục bộ không có nghĩa là máy chủ miễn phí. **Chưa chạy các phép thử LLM thật do không có API key**; kiểm tra mock không phải số đo F1, latency hay chi phí.

## 3. Dự đoán và thực tế

Các dự đoán ghi trước thí nghiệm do **AI hỗ trợ soạn**, có lưu thời gian trong JSON. Ba đối chiếu nổi bật:

**Dự đoán về BoW trên case khó:** Dự đoán accuracy **0,55–0,65**, nhưng BoW + LogReg thực tế chỉ **0,52** và BoW + MLP **0,54**. Tin viết tự nhiên, né từ khóa hoặc giả danh làm BoW gặp khó khăn, nên kết quả kém hơn dự kiến.

**Dự đoán overfitting của MLP:** Dự đoán validation loss tăng sau khoảng 5–10 epoch. Validation loss thực tế nhỏ nhất ở chỉ số epoch 6 (tức **epoch thứ 7**), nên dự đoán về thời điểm tương đối sát. F1 test MLP **0,924**, cao hơn BoW + LogReg **0,865** khoảng **0,058**.

**Dự đoán embedding tốt hơn với tin ngụy trang:** BoW đúng **4/6** còn MiniLM + LogReg đúng **6/6**. Ví dụ lời chào mời điện thoại dùng “at no cost” không chứa từ `free` nhưng vẫn có nghĩa khuyến mại. Dự đoán về xu hướng đúng, tuy nhiên sáu tin chưa đủ để kết luận về hiệu quả tổng thể.

## 4. Phân tích 50 case khó

| Mô hình | F1 SUB 40 | F1 50 case khó | Mức giảm |
| --- | ---: | ---: | ---: |
| BoW + LogReg | 0,788 | 0,333 | 0,455 |
| BoW + MLP | 0,889 | 0,378 | **0,511** |
| MiniLM + kNN | 0,974 | 0,702 | 0,272 |
| MiniLM + LogReg | 1,000 | 0,741 | 0,259 |
| MiniLM + MLP head | 1,000 | 0,667 | 0,333 |

**BoW + MLP tụt nhiều nhất, giảm 0,511 F1**. Các nhóm khó là spam diễn đạt tự nhiên, thao túng người nhận và né từ khóa. BoW chỉ xem từ đơn lẻ nên khó hiểu ngữ cảnh; embedding cũng có thể bị đánh lừa khi thông điệp lừa đảo được ngụy trang tinh vi.

**Case #12:** Tin spam mở đầu lịch sự, giả như người quen mới rồi dụ vào trang hẹn hò. Cả năm mô hình đều sai, do nội dung giống trò chuyện bình thường.

**Case #22:** Tin giả mạo ngân hàng, dọa tài khoản bị khóa và yêu cầu xác minh danh tính. Cả năm mô hình đều sai vì tín hiệu lừa đảo dựa vào sự khẩn cấp và uy hiếp, không nhất thiết dùng từ khóa spam.

50 case là **stress test**, không đại diện cho tỷ lệ spam thực tế. Phần LLM chưa chạy nên không thể kết luận tác dụng của phòng thủ prompt injection.

## 5. Thử thách cá nhân

Với **SEED 4525**, đề số 2 yêu cầu đổi từ điển thành **100** và **5.000** từ, huấn luyện lại Logistic Regression với cùng cách chia train/test rồi so sánh.

| Số từ | Precision | Recall | F1 test | Train |
| --- | ---: | ---: | ---: | ---: |
| 100 | 0,9688 | 0,6392 | 0,7702 | 0,0559 giây |
| 5.000 | 1,0000 | 0,7629 | 0,8655 | 2,7096 giây |

Từ điển lớn giữ nhiều dấu hiệu spam hơn nên recall/F1 tăng, nhưng thời gian train cũng tăng. **Đây là kết quả từ code tham khảo do AI hỗ trợ**, không phải bằng chứng học viên đã tự viết thử thách. Quy tắc lab yêu cầu học viên làm phần này độc lập.

## 6. Phương án cho sản phẩm thật

Với 10 triệu SMS/ngày (trung bình khoảng **116 tin/giây**) và yêu cầu **p95 < 50 ms/tin**, cả năm mô hình đo được đều đáp ứng p95 trên từng tin trong lab. Tuy vậy, throughput của MiniLM + Logistic Regression chỉ khoảng **107 tin/giây** trên một worker, nên cần thử nghiệm tải đồng thời, mở rộng worker và xử lý lưu lượng đỉnh.

**Phương án cần tiếp tục kiểm chứng:** MiniLM + Logistic Regression, đạt F1 test **0,954**, F1 trên tập khó **0,741**, p95 **15,507 ms**. MiniLM + MLP head có F1 test **0,964** cao hơn nhưng F1 tập khó chỉ **0,667**. Không thể kết luận mô hình nào tốt hơn ngoài đời chỉ từ tập stress test nhỏ.

Có thể thiết kế **router hai tầng**: BoW + MLP phân loại tin chắc chắn, còn tin ở vùng lưỡng lự (ví dụ p từ 0,3 đến 0,7) chuyển sang MiniLM + LogReg. Cần kiểm tra riêng false positive, tải đồng thời và tỷ lệ chuyển tầng.

Theo giá LLM giả định trong đề (100 input token, 1 output token mỗi SMS; 0,10/0,50 USD mỗi triệu token), chi phí xử lý 10 triệu SMS là **105 USD/ngày**, tương đương **3.150 USD/30 ngày**. Đây là phép tính lý thuyết, không phải chi phí API đã đo.

## 7. AI log và điều đã học

| Phần | Đã hỏi/nhờ AI gì | AI đã cung cấp gì | Kiểm chứng / phần cần tự làm |
| --- | --- | --- | --- |
| ML, DL, Embedding (1–3) | Hỗ trợ code TODO, giải thích và sửa lỗi | Code tham khảo và giải thích | Đã chạy kiểm thử; **cần tự viết lại các phần cấm dùng AI** |
| Dự đoán | Soạn dự đoán trước thí nghiệm | 10 dự đoán có dấu thời gian | Đối chiếu với output; dự đoán gốc do AI soạn |
| LLM (4) | Viết code API, prompt và parser | Code tham khảo, mock test | Chưa chạy LLM thật vì thiếu API key |
| Thử thách và bonus | Viết code/ví dụ tham khảo | Code thử thách #2 và 5 case bonus | Theo quy định phải tự làm lại các nội dung cá nhân |
| Tính tay | Giải thích năm phép tính | Công thức và hình minh họa | Có ảnh trong thư mục; cần xác nhận là ảnh tự viết tay |
| Báo cáo | Viết lại theo mẫu, dịch tiếng Việt | Bản báo cáo này | Người học phải tự kiểm tra và diễn đạt phần phản ánh |

**Gợi ý về điều đã học (học viên cần viết lại bằng trải nghiệm cá nhân):** F1 cao trên test thường chưa bảo đảm mô hình xử lý tốt tin lừa đảo tinh vi, thể hiện qua sự sụt giảm điểm của BoW + MLP trên tập khó. Khi triển khai thực tế phải xét cả F1, false positive, p95 và throughput thay vì chỉ chọn mô hình có một chỉ số cao. Embedding giúp nhận diện ngữ nghĩa tốt hơn BoW nhưng vẫn cần đánh giá độc lập trên dữ liệu thực.

