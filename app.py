import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, request, jsonify, current_app, render_template, url_for, make_response
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()  # Load variables from a .env file if present

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "finalproject111306061"),
    "database": os.getenv("DB_NAME", "club_equipment"),
    "charset": "utf8mb4",
    "autocommit": False,
    "cursorclass": pymysql.cursors.DictCursor,
}

app = Flask(__name__, 
    static_folder='static',  # 設置靜態文件目錄
    template_folder='templates'  # 設置模板目錄
)
CORS(app)

# Establish a single connection for simplicity; consider pooling for production.
def get_db():
    try:
        if not hasattr(get_db, 'db') or not get_db.db.open:
            get_db.db = pymysql.connect(**DB_CONFIG)
            get_db.cursor = get_db.db.cursor()
        return get_db.db, get_db.cursor
    except Exception as e:
        current_app.logger.error(f"Database connection error: {e}")
        raise

def fetch_one_or_404(sql, params):
    db, cursor = get_db()
    try:
        cursor.execute(sql, params)
        record = cursor.fetchone()
        if not record:
            raise APIError("Resource not found", 404)
        return record
    except pymysql.Error as e:
        current_app.logger.error(f"Database error: {e}")
        raise APIError("Database error", 500)

# ---------------------------------------------------------------------------
# Page Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("login/Login.html")

@app.route("/login")
def login_page():
    return render_template("login/Login.html")

@app.route("/userLogin")
def userLogin():
    return render_template("login/userLogin.html")

@app.route("/clubLogin")
def clubLogin():
    return render_template("login/clubLogin.html")

@app.route("/register")
def register():
    return render_template("註冊/註冊畫面.html")

@app.route("/userRegister")
def userRegister():
    return render_template("註冊/個人註冊畫面.html")

@app.route("/clubRegister")
def clubRegister():
    return render_template("註冊/社團註冊畫面.html")

@app.route("/registerSuccess")
def registerSuccess():
    return render_template("註冊/註冊成功.html")

@app.route("/check")
def check():
    return render_template("管理選項/check.html")

@app.route("/member")
def member():
    return render_template("管理選項/member.html")

@app.route("/equipment-management")
def equipment_management():
    return render_template("管理選項/equipment.html")

@app.route("/clubRecord")
def clubRecord():
    return render_template("管理選項/record.html")

@app.route("/repair")
def repair():
    return render_template("管理選項/repair.html")

@app.route("/userRecord")
def userRecord():
    return render_template("user/record.html")

@app.route("/loan")
def loan():
    return render_template("user/loan.html")

# ---------------------------------------------------------------------------
# Error Handling
# ---------------------------------------------------------------------------

class APIError(Exception):
    """Custom exception carrying a message and an HTTP status code."""

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code

    def to_response(self):
        return jsonify({"error": {"message": str(self)}}), self.status_code


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all unhandled exceptions."""
    current_app.logger.error(f"Unhandled exception: {str(e)}")
    response = jsonify({
        "error": {
            "message": "Internal server error",
            "type": str(type(e).__name__)
        }
    })
    response.status_code = 500
    return response


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def commit_or_rollback(success: bool):
    """Commit on success; rollback otherwise."""
    db, cursor = get_db()
    if success:
        db.commit()
    else:
        db.rollback()


# ---------------------------------------------------------------------------
# User Endpoints
# ---------------------------------------------------------------------------

@app.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    user = fetch_one_or_404("SELECT * FROM Users WHERE BINARY user_id=%s", (user_id,))
    return jsonify(user)


@app.route("/user", methods=["POST"])
def add_user():
    db, cursor = get_db()
    data = request.get_json(force=True)
    hashed_pw = generate_password_hash(data["password"], method="pbkdf2:sha256")

    sql = """
        INSERT INTO Users (user_name, email, password, user_role)
        VALUES (%s, %s, %s, %s)
    """
    values = (
        data["user_name"],
        data["email"],
        hashed_pw,
        data["user_role"]
    )
    try:
        cursor.execute(sql, values)
        db.commit()
    except pymysql.err.IntegrityError as err:
        current_app.logger.exception(err)
        raise APIError("User already exists", 409)
    return jsonify({"message": "User created successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=True)
        db, cursor = get_db()
        cursor.execute("SELECT * FROM Users WHERE email=%s", (data["email"],))
        user = cursor.fetchone()
        if not user:
            raise APIError("Invalid credentials", 401)

        if check_password_hash(user["password"], data["password"]):
            user.pop("password", None)
            return jsonify({"message": "Login successful", "user": user})
        raise APIError("Invalid credentials", 401)
    except APIError as e:
        return e.to_response()
    except Exception as e:
        current_app.logger.error(f"Login error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/user/<user_id>/score", methods=["GET", "PUT"])
def user_score(user_id):
    try:
        db, cursor = get_db()
        if request.method == "GET":
            cursor.execute("SELECT credit_score FROM Users WHERE user_id=%s", (user_id,))
            user = cursor.fetchone()
            if not user:
                raise APIError("User not found", 404)
            return jsonify({"credit_score": user["credit_score"]})
        else:  # PUT
            new_score = request.get_json(force=True)["credit_score"]
            cursor.execute("UPDATE Users SET credit_score=%s WHERE user_id=%s", (new_score, user_id))
            db.commit()
            return jsonify({"message": "Score updated successfully"})
    except APIError as e:
        return e.to_response()
    except Exception as e:
        current_app.logger.error(f"Error in user_score: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/user/member",methods=["GET"])
def get_user_member():
    db, cursor = get_db()
    cursor.execute("SELECT * FROM Users WHERE user_role='user'")
    user = cursor.fetchall()
    return jsonify(user)

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    db, cursor = get_db()
    cursor.execute("DELETE FROM Users WHERE user_id=%s", (user_id,))
    db.commit()
    return jsonify({"message": "User deleted"})


# ---------------------------------------------------------------------------
# Club Endpoints
# ---------------------------------------------------------------------------

@app.route("/club/<club_id>", methods=["GET"])
def get_club(club_id):
    club = fetch_one_or_404("SELECT * FROM Clubs WHERE club_id=%s", (club_id,))
    return jsonify(club)


@app.route("/club", methods=["POST"])
def add_club():
    data = request.get_json(force=True)
    db, cursor = get_db()
    sql = """
        INSERT INTO Clubs (club_id, club_name, club_password, user_id)
        VALUES (%s, %s, %s, %s)
    """
    values = (
        data["club_id"],
        data["club_name"],
        generate_password_hash(data["club_password"], method="pbkdf2:sha256"),
        data["user_id"],
    )
    cursor.execute(sql, values)
    db.commit()
    return jsonify({"message": "Club created successfully"}), 201


@app.route("/club/<club_id>/update_user", methods=["PUT"])
def update_club_user(club_id):
    db, cursor = get_db()
    new_user_id = request.get_json(force=True)["user_id"]
    cursor.execute("UPDATE Clubs SET user_id=%s WHERE club_id=%s", (new_user_id, club_id))
    db.commit()
    return jsonify({"message": "Club user updated successfully"})


@app.route("/club/<club_id>", methods=["DELETE"])
def delete_club(club_id):
    db, cursor = get_db()
    cursor.execute("DELETE FROM Clubs WHERE club_id=%s", (club_id,))
    db.commit()
    return jsonify({"message": "Club deleted successfully"})


# ---------------------------------------------------------------------------
# Equipment Endpoints
# ---------------------------------------------------------------------------

@app.route("/equipment", methods=["POST"])
def add_equipment():
    try:
        data = request.get_json(force=True)
        
        # 驗證必要欄位
        if not data.get("equipment_name"):
            return jsonify({"error": {"message": "器材名稱為必填"}}), 400
            
        # 驗證數據類型
        if not isinstance(data["equipment_name"], str) or not data["equipment_name"].strip():
            return jsonify({"error": {"message": "器材名稱不能為空"}}), 400
            
        db, cursor = get_db()
        sql = """
            INSERT INTO Equipment (equipment_name, equipment_description, equipment_status)
            VALUES (%s, %s, %s)
        """
        values = (
            data["equipment_name"],
            data.get("equipment_description", ""),
            data.get("equipment_status", "available"),
        )
        
        try:
            cursor.execute(sql, values)
            db.commit()
            return jsonify({"message": "Equipment created successfully"}), 201
        except pymysql.err.IntegrityError as e:
            db.rollback()
            current_app.logger.error(f"Database integrity error: {e}")
            return jsonify({"error": {"message": "器材名稱已存在"}}), 409
        except Exception as e:
            db.rollback()
            current_app.logger.error(f"Database error: {e}")
            return jsonify({"error": {"message": "新增器材失敗"}}), 500
            
    except Exception as e:
        current_app.logger.error(f"Error adding equipment: {e}")
        return jsonify({"error": {"message": "新增器材失敗"}}), 500

@app.route("/equipment", methods=["GET"])
def get_all_equipment():
    try:
        db, cursor = get_db()
        cursor.execute("SELECT * FROM Equipment")
        return jsonify(cursor.fetchall())
    except Exception as e:
        current_app.logger.error(f"Error getting equipment: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/equipment/available", methods=["GET"])
def get_available_equipment():
    try:
        db, cursor = get_db()
        cursor.execute("SELECT * FROM Equipment WHERE equipment_status='available'")
        return jsonify(cursor.fetchall())
    except Exception as e:
        current_app.logger.error(f"Error getting available equipment: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/equipment/<equipment_id>/status", methods=["GET"])
def get_equipment_status(equipment_id):
    result = fetch_one_or_404("SELECT equipment_status FROM Equipment WHERE equipment_id=%s", (equipment_id,))
    return jsonify(result)


@app.route("/equipment/<int:equipment_id>/status", methods=["PUT"])
def update_equipment(equipment_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': {'message': '無效的請求數據'}}), 400

        # 驗證必要欄位
        required_fields = ['equipment_name', 'equipment_status']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': {'message': f'缺少必要欄位: {field}'}}), 400

        # 驗證數據類型
        if not isinstance(data['equipment_name'], str) or not data['equipment_name'].strip():
            return jsonify({'error': {'message': '器材名稱不能為空'}}), 400
        if data['equipment_status'] not in ['available', 'repairing']:
            return jsonify({'error': {'message': '無效的器材狀態'}}), 400

        # 獲取數據庫連接
        db, cursor = get_db()

        # 檢查器材是否存在且未被借用
        cursor.execute('SELECT equipment_status FROM Equipment WHERE equipment_id=%s FOR UPDATE', (equipment_id,))
        equipment = cursor.fetchone()
        if not equipment:
            return jsonify({'error': {'message': '找不到該器材'}}), 404
        if equipment['equipment_status'] == 'borrowed':
            return jsonify({'error': {'message': '器材正在借用中，無法更改狀態'}}), 403

        # 更新器材信息
        cursor.execute('''
            UPDATE Equipment 
            SET equipment_name = %s, 
                equipment_description = %s, 
                equipment_status = %s
            WHERE equipment_id = %s
        ''', (
            data['equipment_name'],
            data.get('equipment_description', ''),
            data['equipment_status'],
            equipment_id
        ))
        
        db.commit()
        return jsonify({'message': '更新成功'}), 200

    except Exception as e:
        current_app.logger.error(f"更新器材失敗: {str(e)}")
        return jsonify({'error': {'message': '更新器材失敗'}}), 500


@app.route("/equipment/<equipment_id>", methods=["DELETE"])
def delete_equipment(equipment_id):
    try:
        db, cursor = get_db()
        cursor.execute("DELETE FROM Equipment WHERE equipment_id=%s", (equipment_id,))
        db.commit()
        return jsonify({"message": "Equipment deleted successfully"})
    except Exception as e:
        current_app.logger.error(f"Error deleting equipment: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/equipment/<equipment_id>", methods=["GET"])
def get_equipment(equipment_id):
    try:
        db, cursor = get_db()
        cursor.execute("SELECT * FROM Equipment WHERE equipment_id=%s", (equipment_id,))
        equipment = cursor.fetchone()
        if not equipment:
            return make_response(jsonify({"error": "Equipment not found"}), 404)
        return make_response(jsonify(equipment), 200)
    except Exception as e:
        current_app.logger.error(f"Error getting equipment: {e}")
        return make_response(jsonify({"error": "Internal server error"}), 500)


@app.route("/equipment/pending-inspection", methods=["GET"])
def get_pending_inspection():
    try:
        db, cursor = get_db()
        # 獲取所有待檢查的器材
        cursor.execute("""
            SELECT e.equipment_id, e.equipment_name, e.equipment_description, r.end_date as return_time
            FROM Equipment e
            LEFT JOIN Record r ON e.equipment_id = r.equipment_id
            WHERE e.equipment_status = 'pending_inspection'
            AND (r.end_date = (
                SELECT MAX(end_date)
                FROM Record
                WHERE equipment_id = e.equipment_id
            ) OR r.end_date IS NULL)
            ORDER BY r.end_date DESC
        """)
        equipment_list = cursor.fetchall()

        # 轉換為列表格式
        result = []
        for equipment in equipment_list:
            result.append({
                'equipment_id': equipment['equipment_id'],
                'equipment_name': equipment['equipment_name'],
                'equipment_description': equipment['equipment_description'],
                'return_time': equipment['return_time'].strftime('%Y-%m-%d %H:%M:%S') if equipment['return_time'] else None
            })

        return jsonify(result)

    except Exception as e:
        current_app.logger.error(f"獲取待檢查器材失敗: {str(e)}")
        return jsonify({'error': '獲取待檢查器材失敗'}), 500


@app.route("/equipment/update-status", methods=["PUT"])
def update_equipment_status():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': {'message': '無效的請求數據'}}), 400

        # 驗證必要欄位
        required_fields = ['equipment_id', 'equipment_status']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': {'message': f'缺少必要欄位: {field}'}}), 400

        # 驗證數據類型
        if not isinstance(data['equipment_id'], str):
            return jsonify({'error': {'message': '器材ID格式錯誤'}}), 400
        if data['equipment_status'] not in ['available', 'repairing']:
            return jsonify({'error': {'message': '無效的器材狀態'}}), 400

        # 獲取數據庫連接
        db, cursor = get_db()

        # 檢查器材是否存在
        cursor.execute('SELECT equipment_status FROM Equipment WHERE equipment_id=%s FOR UPDATE', (data['equipment_id'],))
        equipment = cursor.fetchone()
        if not equipment:
            return jsonify({'error': {'message': '找不到該器材'}}), 404

        # 更新器材狀態
        cursor.execute('''
            UPDATE Equipment 
            SET equipment_status = %s
            WHERE equipment_id = %s
        ''', (data['equipment_status'], data['equipment_id']))
        
        db.commit()
        return jsonify({'message': '更新成功'}), 200

    except Exception as e:
        current_app.logger.error(f"更新器材狀態失敗: {str(e)}")
        return jsonify({'error': {'message': '更新器材狀態失敗'}}), 500


# ---------------------------------------------------------------------------
# Record Endpoints – Borrow & Return
# ---------------------------------------------------------------------------

@app.route("/record", methods=["POST"])
def borrow_equipment():
    try:
        data = request.get_json(force=True)
        current_app.logger.info(f"Received borrow request: {data}")
        
        # 驗證必要欄位
        required_fields = ['user_id', 'equipment_id', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                raise APIError(f"Missing required field: {field}", 400)

        db, cursor = get_db()
        
        # Lock the equipment row to avoid concurrent borrow
        cursor.execute(
            "SELECT equipment_status FROM Equipment WHERE equipment_id=%s FOR UPDATE",
            (data["equipment_id"],),
        )
        equipment = cursor.fetchone()
        if not equipment:
            raise APIError("Equipment not found", 404)
        if equipment["equipment_status"] != "available":
            raise APIError("Equipment is not available", 409)

        try:
            # 將前端傳來的日期字符串轉換為 datetime 對象
            start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")
            
            # 獲取今天的日期（不包含時間）
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # 檢查日期是否有效
            if start_date > end_date:
                raise APIError("開始日期不能晚於結束日期", 400)
            if start_date < today:
                raise APIError("不能預約過去的日期", 400)

            # 檢查是否為今天的預約
            is_today = start_date == today

            # 如果是今天的預約，立即更新器材狀態
            if is_today:
                cursor.execute(
                    "UPDATE Equipment SET equipment_status='borrowed' WHERE equipment_id=%s",
                    (data["equipment_id"],),
                )

            # Insert borrow record，不設置 end_date
            sql = """
                INSERT INTO Record (user_id, equipment_id, start_date, is_immediate)
                VALUES (%s, %s, %s, %s)
            """
            values = (
                data["user_id"],
                data["equipment_id"],
                start_date,
                is_today
            )
            cursor.execute(sql, values)
            db.commit()

            # 如果是未來的預約，創建一個定時任務來更新器材狀態
            if not is_today:
                try:
                    # 創建一個定時任務，在開始日期到達時更新器材狀態
                    cursor.execute("""
                        CREATE EVENT IF NOT EXISTS update_equipment_status_%s
                        ON SCHEDULE AT %s
                        DO
                        UPDATE Equipment 
                        SET equipment_status='borrowed' 
                        WHERE equipment_id=%s
                    """, (data["equipment_id"], start_date, data["equipment_id"]))
                    db.commit()
                except Exception as e:
                    current_app.logger.error(f"Failed to create event: {e}")
                    # 即使創建事件失敗，我們仍然繼續，因為這不是關鍵錯誤

            return jsonify({"message": "Borrow record created", "is_immediate": is_today}), 201

        except ValueError as e:
            raise APIError(f"無效的日期格式: {str(e)}", 400)

    except APIError as e:
        db.rollback()
        current_app.logger.error(f"API Error in borrow_equipment: {str(e)}")
        return e.to_response()
    except Exception as e:
        db.rollback()
        current_app.logger.exception(f"Unexpected error in borrow_equipment: {str(e)}")
        raise APIError("Internal Server Error", 500)


@app.route("/record/<record_id>/return", methods=["PUT"])
def return_equipment(record_id):
    try:
        db, cursor = get_db()
        # Get equipment_id of this record to update equipment status
        cursor.execute("SELECT equipment_id FROM Record WHERE record_id=%s AND end_date IS NULL FOR UPDATE", (record_id,))
        rec = cursor.fetchone()
        if not rec:
            raise APIError("Record not found or already returned", 404)
        equipment_id = rec["equipment_id"]

        # Mark record returned
        cursor.execute(
            "UPDATE Record SET end_date=%s WHERE record_id=%s",
            (datetime.now(), record_id),
        )
        # Set equipment status to pending_inspection
        cursor.execute(
            "UPDATE Equipment SET equipment_status='pending_inspection' WHERE equipment_id=%s",
            (equipment_id,),
        )
        db.commit()
        return jsonify({"message": "Equipment returned and pending inspection"})
    except APIError as e:
        db.rollback()
        return e.to_response()
    except Exception as e:
        db.rollback()
        current_app.logger.exception(e)
        raise APIError("Internal Server Error", 500)


@app.route("/record/user/<user_id>", methods=["GET"])
def get_user_records(user_id):
    try:
        db, cursor = get_db()
        # 檢查用戶是否存在
        cursor.execute("SELECT user_id FROM Users WHERE user_id=%s", (user_id,))
        if not cursor.fetchone():
            return make_response(jsonify([]), 200)  # 明確設置狀態碼

        # 獲取用戶的借用記錄
        cursor.execute("""
            SELECT r.*, e.equipment_name, e.equipment_description 
            FROM Record r
            JOIN Equipment e ON r.equipment_id = e.equipment_id
            WHERE r.user_id=%s 
            ORDER BY r.start_date DESC
        """, (user_id,))
        records = cursor.fetchall()
        
        # 將 datetime 對象轉換為字符串
        for record in records:
            if record['start_date']:
                record['start_date'] = record['start_date'].strftime('%Y-%m-%d %H:%M:%S')
            if record['end_date']:
                record['end_date'] = record['end_date'].strftime('%Y-%m-%d %H:%M:%S')
        
        return make_response(jsonify(records), 200)  # 明確設置狀態碼
    except pymysql.Error as e:
        current_app.logger.error(f"Database error in get_user_records: {e}")
        return make_response(jsonify({"error": "Database error"}), 500)
    except Exception as e:
        current_app.logger.error(f"Unexpected error in get_user_records: {e}")
        return make_response(jsonify({"error": "Internal server error"}), 500)


@app.route("/record/equipment/<equipment_id>", methods=["GET"])
def get_equipment_records(equipment_id):
    try:
        db, cursor = get_db()
        cursor.execute("SELECT * FROM Record WHERE equipment_id=%s ORDER BY start_date DESC", (equipment_id,))
        records = cursor.fetchall()
        
        # 將 datetime 對象轉換為字符串
        for record in records:
            if record['start_date']:
                record['start_date'] = record['start_date'].strftime('%Y-%m-%d %H:%M:%S')
            if record['end_date']:
                record['end_date'] = record['end_date'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify(records)
    except Exception as e:
        current_app.logger.error(f"Error getting equipment records: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/record/unreturned", methods=["GET"])
def get_unreturned_records():
    try:
        db, cursor = get_db()
        cursor.execute("SELECT * FROM Record WHERE end_date IS NULL")
        return jsonify(cursor.fetchall())
    except Exception as e:
        current_app.logger.error(f"Error getting unreturned records: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/record/all", methods=["GET"])
def get_all_records():
    try:
        db, cursor = get_db()
        # 獲取所有借用記錄，並關聯器材和用戶信息
        cursor.execute("""
            SELECT 
                r.*,
                e.equipment_name,
                u.user_name
            FROM Record r
            JOIN Equipment e ON r.equipment_id = e.equipment_id
            JOIN Users u ON r.user_id = u.user_id
            ORDER BY r.start_date DESC
        """)
        records = cursor.fetchall()
        
        # 將 datetime 對象轉換為字符串
        for record in records:
            if record['start_date']:
                record['start_date'] = record['start_date'].strftime('%Y-%m-%d %H:%M:%S')
            if record['end_date']:
                record['end_date'] = record['end_date'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify(records)
    except Exception as e:
        current_app.logger.error(f"Error getting all records: {e}")
        return jsonify({"error": "Internal server error"}), 500


# ---------------------------------------------------------------------------
# Belonging Endpoints
# ---------------------------------------------------------------------------

@app.route("/belonging", methods=["POST"])
def add_belonging():
    data = request.get_json(force=True)
    db, cursor = get_db()
    sql = "INSERT INTO Belonging (user_id, equipment_id) VALUES (%s, %s)"
    cursor.execute(sql, (data["user_id"], data["equipment_id"]))
    db.commit()
    return jsonify({"message": "Belonging created"}), 201


@app.route("/belonging/<user_id>", methods=["GET"])
def get_belonging_equipment(user_id):
    db, cursor = get_db()
    sql = """
        SELECT Equipment.*
        FROM Belonging
        JOIN Equipment ON Belonging.equipment_id = Equipment.equipment_id
        WHERE Belonging.user_id=%s
    """
    cursor.execute(sql, (user_id,))
    return jsonify(cursor.fetchall())


@app.route("/belonging", methods=["DELETE"])
def delete_belonging():
    data = request.get_json(force=True)
    db, cursor = get_db()
    cursor.execute(
        "DELETE FROM Belonging WHERE user_id=%s AND equipment_id=%s",
        (data["user_id"], data["equipment_id"]),
    )
    db.commit()
    return jsonify({"message": "Belonging deleted"})


# ---------------------------------------------------------------------------
# Repair Endpoints
# ---------------------------------------------------------------------------

@app.route("/repair", methods=["POST"])
def report_repair():
    try:
        data = request.get_json(force=True)
        db, cursor = get_db()
        
        # 開始事務
        try:
            # 1. 插入報修記錄
            repair_sql = """
                INSERT INTO Equipment_Repair (equipment_id, user_id, report_time, report_notes, repair_status)
                VALUES (%s, %s, %s, %s, %s)
            """
            current_time = datetime.now()
            repair_values = (
                data["equipment_id"],
                data["user_id"],
                current_time,
                data.get("report_notes", ""),
                data["repair_status"],
            )
            cursor.execute(repair_sql, repair_values)

            # 2. 更新器材狀態為維修中
            update_sql = """
                UPDATE Equipment SET equipment_status='repairing' WHERE equipment_id=%s
            """
            cursor.execute(update_sql, (data["equipment_id"],))

            # 3. 創建檢查記錄
            inspection_sql = """
                INSERT INTO Equipment_Inspection (equipment_id, inspected_time, inspection_status, inspection_notes)
                VALUES (%s, %s, %s, %s)
            """
            inspection_values = (
                data["equipment_id"],
                current_time,
                'needs_repair',
                f"報修原因: {data.get('report_notes', '無')}"
            )
            cursor.execute(inspection_sql, inspection_values)

            db.commit()
            return jsonify({"message": "Repair report created"}), 201

        except Exception as e:
            db.rollback()
            current_app.logger.error(f"Error in repair transaction: {e}")
            raise

    except Exception as e:
        current_app.logger.error(f"Error reporting repair: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/repair/<equipment_id>", methods=["GET"])
def get_repair_records(equipment_id):
    try:
        db, cursor = get_db()
        
        # 檢查器材是否存在
        cursor.execute("SELECT equipment_id FROM Equipment WHERE equipment_id=%s", (equipment_id,))
        if not cursor.fetchone():
            return make_response(jsonify([]), 200)

        # 獲取報修記錄
        cursor.execute("""
            SELECT 
                r.record_id as No,
                e.equipment_name as name,
                e.equipment_description as description,
                er.repair_status,
                er.report_time,
                er.report_notes,
                r.user_id
            FROM Equipment_Repair er
            JOIN Equipment e ON er.equipment_id = e.equipment_id
            JOIN Record r ON er.equipment_id = r.equipment_id
            WHERE er.equipment_id=%s 
            AND r.user_id = er.user_id
            ORDER BY er.report_time DESC
        """, (equipment_id,))
        repairs = cursor.fetchall()
        
        # 將 datetime 對象轉換為字符串
        for repair in repairs:
            if repair['report_time']:
                repair['report_time'] = repair['report_time'].strftime('%Y-%m-%d %H:%M:%S')
        
        return make_response(jsonify(repairs), 200)
    except Exception as e:
        current_app.logger.error(f"Error getting repair records: {e}")
        return make_response(jsonify({"error": "Internal server error"}), 500)


@app.route("/repair/update", methods=["PUT"])
def update_repair_status():
    try:
        data = request.get_json(force=True)
        db, cursor = get_db()
        sql = """
            UPDATE Equipment_Repair
            SET repair_status=%s
            WHERE equipment_id=%s AND report_time=%s
        """
        cursor.execute(sql, (data["repair_status"], data["equipment_id"], data["report_time"]))
        db.commit()
        return jsonify({"message": "Repair status updated"})
    except Exception as e:
        current_app.logger.error(f"Error updating repair status: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/repair/all", methods=["GET"])
def get_all_repairs():
    try:
        db, cursor = get_db()
        # 獲取所有器材的最新檢查狀態和報修記錄
        cursor.execute("""
            WITH LatestInspection AS (
                SELECT 
                    equipment_id,
                    inspection_status,
                    inspected_time,
                    ROW_NUMBER() OVER (PARTITION BY equipment_id ORDER BY inspected_time DESC) as rn
                FROM Equipment_Inspection
            ),
            LatestRepair AS (
                SELECT 
                    equipment_id,
                    report_time,
                    report_notes,
                    user_id,
                    ROW_NUMBER() OVER (PARTITION BY equipment_id ORDER BY report_time DESC) as rn
                FROM Equipment_Repair
            )
            SELECT DISTINCT
                e.equipment_id,
                e.equipment_name,
                li.inspection_status,
                li.inspected_time as last_inspection_time,
                lr.report_time,
                lr.report_notes,
                u.user_name
            FROM Equipment e
            LEFT JOIN LatestInspection li ON e.equipment_id = li.equipment_id AND li.rn = 1
            LEFT JOIN LatestRepair lr ON e.equipment_id = lr.equipment_id AND lr.rn = 1
            LEFT JOIN Users u ON lr.user_id = u.user_id
            ORDER BY e.equipment_name
        """)
        repairs = cursor.fetchall()
        
        # 將 datetime 對象轉換為字符串
        for repair in repairs:
            if repair['report_time']:
                repair['report_time'] = repair['report_time'].strftime('%Y-%m-%d %H:%M:%S')
            if repair['last_inspection_time']:
                repair['last_inspection_time'] = repair['last_inspection_time'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify(repairs)
    except Exception as e:
        current_app.logger.error(f"Error getting all repairs: {e}")
        return jsonify({"error": "Internal server error"}), 500


# ---------------------------------------------------------------------------
# Inspection Endpoints
# ---------------------------------------------------------------------------

@app.route("/inspection", methods=["POST"])
def add_inspection():
    data = request.get_json(force=True)
    db, cursor = get_db()
    sql = """
        INSERT INTO Equipment_Inspection (equipment_id, inspected_time, inspection_status, inspection_notes)
        VALUES (%s, %s, %s, %s)
    """
    values = (
        data["equipment_id"],
        datetime.now(),
        data["inspection_status"],
        data.get("inspection_notes", ""),
    )
    cursor.execute(sql, values)
    db.commit()
    return jsonify({"message": "Inspection record added"}), 201


@app.route("/inspection/<equipment_id>", methods=["GET"])
def get_inspection_records(equipment_id):
    try:
        db, cursor = get_db()
        cursor.execute(
            "SELECT * FROM Equipment_Inspection WHERE equipment_id=%s ORDER BY inspected_time DESC",
            (equipment_id,),
        )
        return jsonify(cursor.fetchall())
    except Exception as e:
        current_app.logger.error(f"Error getting inspection records: {e}")
        return jsonify({"error": "Internal server error"}), 500


# ---------------------------------------------------------------------------
# App Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500, debug=True)











