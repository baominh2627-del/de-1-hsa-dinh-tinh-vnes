import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the JSON array
json_str = content.replace('export const examData = ', '').strip().rstrip(';')
data = json.loads(json_str)

# We need to find the repeated passages and remove them from subsequent questions.
# A passage is typically identified by "<b>Đọc ngữ liệu sau...</b><br><br>...<br><br>"
for q in data:
    if '<b>Đọc ngữ liệu sau' in q['question']:
        # Extract the passage prefix. It usually ends with "</div><br><br>" or similar.
        # Let's find the split point. We can split by "<br><br>" but we might split the passage itself.
        # The question text is whatever comes after the last "<br><br>" or "</div><br><br>".
        parts = q['question'].split('<br><br>')
        if len(parts) > 1:
            passage = '<br><br>'.join(parts[:-1]) + '<br><br>'
            # We want to remove this exact passage from all OTHER questions.
            for other_q in data:
                if other_q['id'] != q['id'] and passage in other_q['question']:
                    other_q['question'] = other_q['question'].replace(passage, '')

out_js = 'export const examData = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n'

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(out_js)

# Update the prompt
with open('Prompt_HuongDan_DinhTinh_HSA.md', 'r', encoding='utf-8') as f:
    prompt = f.read()

old_rule = r'- \*\*Tích hợp ngữ liệu:\*\* Đối với chùm câu hỏi chung một ngữ liệu \(ví dụ: Từ câu 66 - 70\), đoạn ngữ liệu phải được chèn vào trước nội dung của TỪNG câu hỏi trong chùm đó để học sinh có thể đọc mà không phải cuộn lên\. Thêm tiêu đề <b>Đọc ngữ liệu sau và trả lời các câu hỏi từ \.\.\.:</b> ở đầu\.'
new_rule = r'- **Tích hợp ngữ liệu:** Đối với chùm câu hỏi chung một ngữ liệu (ví dụ: Từ câu 66 - 70), đoạn ngữ liệu CHỈ CẦN được chèn vào trước nội dung của CÂU HỎI ĐẦU TIÊN trong chùm đó (ví dụ: chèn vào câu 66). Các câu hỏi phía sau (67-70) chỉ cần ghi trực tiếp nội dung câu hỏi. Thêm tiêu đề <b>Đọc ngữ liệu sau và trả lời các câu hỏi từ ...:</b> ở đầu phần ngữ liệu.'

# Try simple replace first
prompt = prompt.replace(
    "- **Tích hợp ngữ liệu:** Đối với chùm câu hỏi chung một ngữ liệu (ví dụ: Từ câu 66 - 70), đoạn ngữ liệu phải được chèn vào trước nội dung của TỪNG câu hỏi trong chùm đó để học sinh có thể đọc mà không phải cuộn lên. Thêm tiêu đề <b>Đọc ngữ liệu sau và trả lời các câu hỏi từ ...:</b> ở đầu.",
    "- **Tích hợp ngữ liệu:** Đối với chùm câu hỏi chung một ngữ liệu (ví dụ: Từ câu 66 - 70), đoạn ngữ liệu CHỈ CẦN được chèn vào trước nội dung của CÂU HỎI ĐẦU TIÊN trong chùm đó (ví dụ: chèn vào câu 66). Các câu hỏi phía sau (67-70) chỉ cần ghi trực tiếp nội dung câu hỏi. Thêm tiêu đề <b>Đọc ngữ liệu sau và trả lời các câu hỏi từ ...:</b> ở đầu phần ngữ liệu."
)

with open('Prompt_HuongDan_DinhTinh_HSA.md', 'w', encoding='utf-8') as f:
    f.write(prompt)
