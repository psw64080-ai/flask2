"""
Flask BMI 계산기 - 메인 애플리케이션 (flask2)
향상된 버전: app.py의 기능을 유지하면서 최적화
"""
from flask import Flask, render_template, request, redirect, url_for
from backend.models.database import Database
from backend.services.bmi_service import BMICalculator
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# Flask 앱 생성
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# 전역 데이터베이스 인스턴스
db = None

def init_database():
    """데이터베이스 초기화 및 연결"""
    global db
    db = Database()
    print("✅ 데이터베이스 연결 완료")

@app.route('/', methods=['GET'])
def index():
    """BMI 계산 페이지"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """BMI 계산 및 저장"""
    try:
        # 입력값 받기
        weight = float(request.form.get('weight', 0))
        height = float(request.form.get('height', 0))
        
        # 입력값 유효성 검사
        if weight <= 0 or height <= 0:
            return render_template('index.html', error="체중과 신장은 0보다 커야 합니다.")
        
        # BMI 계산
        calculator = BMICalculator(weight, height)
        bmi = calculator.calculate_bmi()
        category = calculator.get_bmi_category()
        
        # 데이터베이스에 저장
        if db:
            success = db.save_bmi_record(weight, height, bmi, category)
            print(f"📊 BMI 기록 저장 - 체중: {weight}kg, 신장: {height}cm, BMI: {bmi:.2f}, 분류: {category}")
        
        # 결과 페이지로 이동
        return render_template('result.html',
                              weight=weight,
                              height=height,
                              bmi=round(bmi, 2),
                              category=category)
    
    except ValueError:
        return render_template('index.html', error="유효한 숫자를 입력해주세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return render_template('index.html', error="계산 중 오류가 발생했습니다.")

@app.route('/history')
def history():
    """BMI 이력 조회"""
    records = []
    if db:
        records = db.get_bmi_records(limit=10)
        print(f"📜 조회된 이력: {len(records)}개")
    return render_template('history.html', records=records)

@app.errorhandler(404)
def not_found(error):
    """404 에러 처리"""
    return render_template('index.html', error="페이지를 찾을 수 없습니다."), 404

@app.errorhandler(500)
def server_error(error):
    """500 에러 처리"""
    return render_template('index.html', error="서버 오류가 발생했습니다."), 500

if __name__ == '__main__':
    print("="*60)
    print("🚀 Flask BMI 계산기 서버 시작 (flask2 버전)")
    print("="*60)
    
    # 데이터베이스 초기화
    init_database()
    
    print("📍 웹사이트: http://localhost:5000")
    print("🔍 디버그 모드: ON")
    print("="*60)
    
    # Flask 서버 실행
    app.run(debug=True, host='localhost', port=5000, use_reloader=True)
