import re

def extract_text_from_file_with_keywords(file_path, keywords, output_file_path, remove_words=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # 파일 내용 읽기

        # 키워드 중 가장 먼저 발견된 위치를 찾습니다.
        min_index = len(content)  # 텍스트 끝을 초기값으로 설정
        matched_keyword = None  # 잘린 키워드를 저장할 변수

        for keyword in keywords:
            if keyword in content:
                index = content.index(keyword)
                if index < min_index:
                    min_index = index
                    matched_keyword = keyword  # 잘린 키워드 업데이트

        # 첫 번째 키워드 이전의 텍스트 추출
        extracted_text = content[:min_index].strip() if min_index < len(content) else content.strip()

        # 특정 단어가 포함된 문장을 제거
        if remove_words:
            lines = extracted_text.splitlines()  # 줄 단위로 분리
            filtered_lines = [
                line for line in lines if not any(word in line for word in remove_words)
            ]
            extracted_text = "\n".join(filtered_lines)  # 줄바꿈을 유지하면서 다시 합침

        # 추출한 텍스트를 출력 파일에 저장
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(extracted_text)

        # 잘린 키워드와 함께 결과 메시지 반환
        if matched_keyword:
            return f"The text was saved to '{output_file_path}'. It was cut at the keyword: '{matched_keyword}'"
        else:
            return f"The text was saved to '{output_file_path}'. No keyword was found in the text."

    except FileNotFoundError:
        return "Can't find file"
    except Exception as e:
        return f"A  error occurs {e}"

def main():
    # 사용 예제
    file_path = "webpage_text.txt"  # 읽을 텍스트 파일 경로
    keywords = ["다음 기사", 
                "다음기사", 
                "볼만한", 
                "다른 기사",
                "다른기사", 
                "어땠나요",
                "관련뉴스",
                "관련 뉴스",
                "마음에 들",
                "마음에 듦",
                "마음에 드",
                "기자입니다"]  # 본문을 자를 키워드 리스트
    output_file_path = "webpage_text.txt"  # 저장할 출력 파일 경로

    # 특정 단어가 들어간 문장을 삭제할 단어 리스트
    remove_words = ["AI요약", "AI 요약", "'세 줄 요약' 기술", "...", "주소:", "copyright", "Copyright", "(c)", "(C)", "@"]

    result = extract_text_from_file_with_keywords(file_path, keywords, output_file_path, remove_words)

    # 결과 메시지 출력

if __name__ == "__main__":
    main()
