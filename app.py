"""
Flask BMI 계산기 애플리케이션
"""
from flask import Flask
from backend.models.database import Database
from backend.routes.main_routes import main_bp, init_db

def create_app():
    """Flask 앱 인스턴스 생성"""
    app = Flask(__name__)
    
    # 데이터베이스 초기화
    db = Database()
    init_db(db)  # 라우트에서 DB를 사용할 수 있도록 주입
    
    # Blueprint 등록
    app.register_blueprint(main_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("=" * 50)
    print("🚀 Flask BMI 계산기 서버 시작")
    print("=" * 50)
    print("📍 웹사이트: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='localhost', port=5000)
