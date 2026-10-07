from flask import Flask, render_template,request,redirect,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(override=True)
print("database user:",repr(os.getenv("DB_USER")))

app=Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY")

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@app.route("/")
def home():
    return render_template("index.html")


#----------Check Login ----------

def student_login_required(f):

    @wraps(f)
    def decorated_function(*args,**kwargs):

        if "student_id" not in session:
            return redirect(url_for("student_login"))

        return f(*args,**kwargs)


    return decorated_function


#------------Submit Complaints---------


@app.route("/submit",methods=["GET","POST"])
@student_login_required
def submit_complaint():


    if "student_id" not in session:
        return redirect(url_for("student_login"))

    
    if request.method=="POST":

    
        category=request.form.get("category")
        description=request.form.get("description")

        student_id=session["student_id"]

        try:
            conn=get_db_connection()
            cur=conn.cursor()

            
            cur.execute(
                """insert into complaints
                (student_id,category,description,status)
                values(%s,%s,%s,%s)""",
                (student_id,
                 category,
                description,
                "Pending")
            )

            conn.commit()

            return redirect(url_for("my_complaint"))

        except Exception as e:

            if conn:
                conn.rollback()

            print("Complaint Error:",e)

            return "Error while submitting complaint."

        finally:

            if cur:
                cur.close()

            if conn:
                conn.close()


    return render_template("submit.html")


#-------------ADMIN LOGIN SYSTEM-----

@app.route("/admin",methods=["GET","POST"])
def admin_login():

    if request.method=="POST":

        username=request.form.get("username")
        password=request.form.get("password")

        #Temperory Admin Login

        if username=="admin" and password=="admin123":

            session["admin"]=True
            return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin.html",
            error="Invalid username or password"
        )
    
    return render_template("admin.html")

#------------MY ------Complaint

@app.route("/my_complaint")
@student_login_required
def my_complaint():

    if "student_id" not in session:
        return redirect(url_for("student_login"))

    student_id=session["student_id"]

    conn=get_db_connection()
    cur=conn.cursor()

    cur.execute(
        """select complaint_id,category,description,status,created_at from complaints
        where student_id=%s 
        order by created_at desc""",(student_id,)
    )

    complaints=cur.fetchall()

    cur.close()
    conn.close()


    return render_template(
        "my_complaint.html",
        complaints=complaints
    )




#-----------------ADMIN DASHBOARD-----

@app.route("/admin/dashboard")
def admin_dashboard():


    # Check Admin Login

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn=get_db_connection()
    cur=conn.cursor()

    cur.execute(
        """select complaint_id,student_name,roll_number,department,category,description,status,created_at 
        from complaints order by complaint_id asc"""
    )

    complaints=cur.fetchall()


    #Total Complaints

    cur.execute("select count(*) from complaints")
    total=cur.fetchone()[0]


    #Pending Complaints
    cur.execute(
        """select count(*) from complaints
        where status='Pending'
        """
    )
    pending=cur.fetchone()[0]


    #In Progress Complaints
    cur.execute(
        """select count(*) from complaints where status='In Progress'"""
    )
    progress=cur.fetchone()[0]


    #Resolved Complaints
    cur.execute(
        """select count(*) from complaints
        where status='Resolved'
        """
    )
    resolved=cur.fetchone()[0]

    cur.close()
    conn.close()


    return render_template(
        "admin_dashboard.html",
        complaints=complaints,
        total=total,
        pending=pending,
        progress=progress,
        resolved=resolved
    )


#------------UPDATE STATUS---------

@app.route("/admin/update/<int:complaint_id>",methods=["GET","POST"])
def update_status(complaint_id):


    #Check Admin Login
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    status=request.form.get("status")

    conn=get_db_connection()
    cur=conn.cursor()

    cur.execute(
        """update complaints
        set status=%s
        where complaint_id=%s""",(status,complaint_id)
    )

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("admin_dashboard"))



#-----------------DELETE----COMPLAINTS----



@app.route("/admin/delete/<int:complaint_id>",methods=["GET","POST"])
def delete_complaint(complaint_id):

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn=get_db_connection()
    cur=conn.cursor()

    cur.execute(
        """delete from complaints where complaint_id=%s""",(complaint_id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("admin_dashboard"))


#------------STUDENT REGISTRATION------

@app.route("/register",methods=["GET","POST"])
def register():

    if request.method=="POST":

        student_name=request.form.get("student_name")
        roll_number=request.form.get("roll_number")
        email=request.form.get("email")
        department=request.form.get("department")
        passwords=request.form.get("password")
        confirm_password=request.form.get("comfirm_password")

        if passwords !=confirm_password:
            return render_template(
                "register.html",
                error="Password do not match"
            )

        

        conn=None
        cur=None


        try:
            conn=get_db_connection()
            cur=conn.cursor()

            cur.execute(
                """ insert into student(
                student_name,roll_number,email,passwords,department)
                values(%s,%s,%s,%s,%s)""",
                (
                    student_name,
                    roll_number,
                    email,
                    passwords,
                    department
                )
            )

            conn.commit()

        except Exception as e:

            if conn:
                conn.rollback()

            print("Registration error:",e)

            return render_template(
                "register.html",
                error="Roll Number or email may already be registered"
            )

        finally:
            if cur:
                cur.close()

            if conn:
                conn.close()

        return redirect(url_for("student_login"))


    return render_template("register.html")


#---------STUDENT LOGIN-------

@app.route("/student_login", methods=["GET","POST"])
def student_login():

    if request.method=="POST":

        roll_number=request.form.get("roll_number")
        passwords=request.form.get("password")

        conn=get_db_connection()

        cur=conn.cursor()

        cur.execute(
            """select student_id,student_name,roll_number,passwords from student where roll_number=%s and passwords=%s""",
            (roll_number,passwords)
        )

        student=cur.fetchone()

        cur.close()
        conn.close()

        if student:
            session["student_id"]=student[0]
            session["student_name"]=student[1]
            session["roll_number"]=student[2]


            return redirect(url_for("student_dashboard"))

        return render_template(
            "student_login.html",
            error="Invaid roll number or password"
        )

    return render_template("student_login.html")



#---------STUDENT DASHBOARD-------


@app.route("/student_dashboard")
@student_login_required
def student_dashboard():


    if "student_id" not in session:
        return redirect(url_for("student_login"))

    conn=get_db_connection()
    cur=conn.cursor()

    cur.execute(
        """select student_id, student_name,roll_number,email,department from student
        where student_id=%s""",
        (session["student_id"],)
    )

    student=cur.fetchone()

    cur.close()
    conn.close()


    if not student:
        session.clear()
        return redirect(url_for("student_login"))


    return render_template(
        "student_dashboard.html",
        student=student
    )



#-----------Student Logout-------

@app.route("/student/logout")
@student_login_required
def student_logout():


    session.pop("student_id",None)
    session.pop("student_name",None)
    session.pop("roll_number",None)

    return redirect(url_for("student_login"))



#-----------ADMIN LOGOUT-----


@app.route("/admin/logout")
def admin_logout():

    session.pop("admin",None)

    return redirect(url_for("admin_login"))

if __name__=="__main__":
    app.run(debug=True)