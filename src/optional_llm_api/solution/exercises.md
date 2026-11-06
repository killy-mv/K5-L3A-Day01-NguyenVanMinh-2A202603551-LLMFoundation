# Bài tập side lab — bản phân tích có hỗ trợ AI

## 2.1 Temperature

Chưa có API key, nên chưa thực hiện bốn lần gọi API và không có bốn phản hồi để nhận xét thực nghiệm. Dự đoán lý thuyết: temperature thấp thường tập trung vào các lựa chọn có xác suất cao; temperature cao tăng độ đa dạng, không bảo đảm độ đúng. Với chatbot hỗ trợ khách hàng, có thể bắt đầu ở 0–0,3 rồi đánh giá trên bộ câu hỏi chuẩn; factuality còn phụ thuộc nguồn dữ liệu và cơ chế kiểm chứng.

## 2.2 Chi phí

Theo giá đề bài, cả đơn giá input và output của model lớn đều gấp **10 lần** model nhỏ. 10.000×3=30.000 lượt/ngày; 30.000×350=10,5 triệu token/ngày. Đề chưa nêu tỷ lệ input/output, nên chưa đủ để tính một chi phí tuyệt đối duy nhất. Nếu cả 350 token đều là output: model lớn $52,50/ngày, model nhỏ $5,25/ngày. Nếu có cả input, dùng tổng token input×giá input + tổng token output×giá output; tỷ lệ chi phí vẫn là 10 nếu hai model dùng cùng số token.

Model lớn có thể đáng giá ở câu hỏi phân tích phức tạp khi đánh giá cho thấy cải thiện đủ lớn. Model nhỏ phù hợp phân loại đơn giản hoặc câu trả lời thường gặp khi đạt ngưỡng chất lượng. Đây là phân tích theo bảng giá trong đề, chưa phải kết quả API.

## 2.3 Streaming

Streaming có ích trong hội thoại hoặc câu trả lời dài vì người dùng đọc được phần đầu trước khi toàn bộ nội dung hoàn tất. Nó giảm thời gian cảm nhận tới nội dung đầu tiên, không mặc nhiên giảm tổng thời gian hay số token. Non-streaming phù hợp phân loại một nhãn, tác vụ batch hoặc JSON cần được kiểm tra đầy đủ trước khi sử dụng; streaming JSON phải đợi tài liệu hoàn chỉnh mới parse an toàn.

## AI log

Yêu cầu: “can you do the lab for me?” ChatGPT viết các hàm và phân tích trên, kiểm thử bằng mock; học viên chưa xác nhận tự sửa hoặc đã hiểu. Chưa có thử nghiệm API trực tiếp.
