"""
데이터베이스 초기화 스크립트
BMI 기록 테이블을 생성합니다
"""
import pymysql
from config import Config

def init_database():
    """데이터베이스 및 테이블 생성"""
    try:
        # 관리자 연결 (데이터베이스 선택 전)
        connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT,
            charset='utf8mb4'
        )
        
        print(f"✅ MariaDB 연결 성공! (호스트: {Config.DB_HOST})")
        
        with connection.cursor() as cursor:
            # 1. 데이터베이스 생성 (utf8mb4)
            cursor.execute(f"""
            CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}
            CHARACTER SET utf8mb4
            COLLATE utf8mb4_unicode_ci
            """)
            print(f"✅ 데이터베이스 '{Config.DB_NAME}' 생성/확인 완료")
            
            # 2. 데이터베이스 선택
            cursor.execute(f"USE {Config.DB_NAME}")
            
            # 3. BMI 기록 테이블 생성
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                weight FLOAT NOT NULL COMMENT '체중(kg)',
                height FLOAT NOT NULL COMMENT '신장(cm)',
                bmi FLOAT NOT NULL COMMENT 'BMI 지수',
                category VARCHAR(50) NOT NULL COMMENT 'BMI 분류(저체중/정상/과체중/비만/고도비만)',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '기록 생성 시간',
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("✅ '테이블 'bmi_records' 생성/확인 완료")
            
        connection.commit()
        connection.close()
        
        print("\n" + "="*50)
        print("✨ 데이터베이스 초기화 완료!")
        print("="*50)
        
    except pymysql.Error as e:
        print(f"❌ 데이터베이스 오류: {e}")
        print("\n⚠️ MariaDB/MySQL 서버가 실행 중인지 확인하세요!")
        print(f"   호스트: {Config.DB_HOST}")
        print(f"   포트: {Config.DB_PORT}")
        print(f"   사용자: {Config.DB_USER}")

if __name__ == '__main__':
    print("🔧 데이터베이스 초기화를 시작합니다...")
    print("-" * 50)
    init_database()
