import unittest
import cv2
import pytesseract

class TestOCR(unittest.TestCase):
    def test_ocr(self):
        # Load the video frames from file
        cap = cv2.VideoCapture('video.mp4')
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()

        # Extract Chinese text from the frames using OCR
        chinese_text = []
        for frame in frames:
            text = pytesseract.image_to_string(frame, lang='chi_sim')
            chinese_text.append(text)

        # Compare the extracted text to the expected results
        expected_text = ['你好', '谢谢', '再见']
        self.assertListEqual(chinese_text, expected_text)

if __name__ == '__main__':
    unittest.main()
