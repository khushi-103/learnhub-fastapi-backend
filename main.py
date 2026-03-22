from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

# request models

class EnrollRequest(BaseModel):
    student_name: str = Field(..., min_length=2)
    course_id: int = Field(..., gt=0)
    email: str = Field(..., min_length=5)
    payment_method: str = "card"
    coupon_code: str = ""
    gift_enrollment: bool = False
    recipient_name: str = ""


class NewCourse(BaseModel):
    title: str = Field(..., min_length=2)
    instructor: str = Field(..., min_length=2)
    category: str = Field(..., min_length=2)
    level: str = Field(..., min_length=2)
    price: int = Field(..., ge=0)
    seats_left: int = Field(..., gt=0)


class WishlistEnroll(BaseModel):
    student_name: str
    payment_method: str = "card"


# temporary data (simulating database)

courses = [
    {"id":1,"title":"Python Basics","instructor":"Ravi Sharma","category":"Web Dev","level":"Beginner","price":0,"seats_left":20},
    {"id":2,"title":"React Mastery","instructor":"Anita Kapoor","category":"Web Dev","level":"Intermediate","price":2500,"seats_left":8},
    {"id":3,"title":"Machine Learning","instructor":"Dr. Mehta","category":"Data Science","level":"Advanced","price":5000,"seats_left":5},
    {"id":4,"title":"UI/UX Design","instructor":"Sneha Jain","category":"Design","level":"Beginner","price":1500,"seats_left":10},
    {"id":5,"title":"Docker & Kubernetes","instructor":"Arjun Singh","category":"DevOps","level":"Intermediate","price":3500,"seats_left":7},
    {"id":6,"title":"Data Visualization","instructor":"Priya Nair","category":"Data Science","level":"Beginner","price":2000,"seats_left":15},
]

enrollments = []
enrollment_counter = 1
wishlist = []


# helper functions

def find_course(course_id: int):
    for c in courses:
        if c["id"] == course_id:
            return c
    return None


def calculate_enrollment_fee(price, seats_left, coupon):

    original_price = price
    discount = 0

    if seats_left > 5:
        early_discount = int(price * 0.10)
        discount += early_discount
        price -= early_discount

    if coupon == "STUDENT20":
        coupon_discount = int(price * 0.20)
        discount += coupon_discount
        price -= coupon_discount

    if coupon == "FLAT500":
        discount += 500
        price -= 500

    final_price = max(price, 0)

    return {
        "original_price": original_price,
        "discount": discount,
        "final_fee": final_price
    }


def filter_courses_logic(category=None, level=None, max_price=None, has_seats=None):

    result = courses

    if category is not None:
        result = [c for c in result if c["category"] == category]

    if level is not None:
        result = [c for c in result if c["level"] == level]

    if max_price is not None:
        result = [c for c in result if c["price"] <= max_price]

    if has_seats:
        result = [c for c in result if c["seats_left"] > 0]

    return result


# basic endpoints

@app.get("/")
def home():
    return {"message": "Welcome to LearnHub Online Courses"}


@app.get("/courses")
def get_courses():

    total_seats = sum(c["seats_left"] for c in courses)

    return {
        "courses": courses,
        "total": len(courses),
        "total_seats_available": total_seats
    }


# filter courses

@app.get("/courses/filter")
def filter_courses(
    category: str = Query(None),
    level: str = Query(None),
    max_price: int = Query(None),
    has_seats: bool = Query(None)
):

    result = filter_courses_logic(category, level, max_price, has_seats)

    return {
        "filtered_courses": result,
        "count": len(result)
    }


# search courses

@app.get("/courses/search")
def search_courses(keyword: str = Query(...)):

    keyword = keyword.lower()

    matches = []

    for course in courses:
        if (
            keyword in course["title"].lower()
            or keyword in course["instructor"].lower()
            or keyword in course["category"].lower()
        ):
            matches.append(course)

    return {
        "matches": matches,
        "total_found": len(matches)
    }


# sort courses

@app.get("/courses/sort")
def sort_courses(
    sort_by: str = Query("price"),
    order: str = Query("asc")
):

    valid_sort_fields = ["price", "title", "seats_left"]

    if sort_by not in valid_sort_fields:
        return {"error": "Invalid sort_by field"}

    reverse = True if order == "desc" else False

    sorted_courses = sorted(courses, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sorted_by": sort_by,
        "order": order,
        "total_courses": len(sorted_courses),
        "courses": sorted_courses
    }


# pagination

@app.get("/courses/page")
def paginate_courses(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1)
):

    total_courses = len(courses)

    start = (page - 1) * limit
    end = start + limit

    paginated_courses = courses[start:end]

    total_pages = (total_courses + limit - 1) // limit

    return {
        "current_page": page,
        "limit": limit,
        "total_courses": total_courses,
        "total_pages": total_pages,
        "courses": paginated_courses
    }


# summary

@app.get("/courses/summary")
def courses_summary():

    most_expensive = max(courses, key=lambda x: x["price"])

    category_count = {}

    for c in courses:
        category_count[c["category"]] = category_count.get(c["category"], 0) + 1

    return {
        "total_courses": len(courses),
        "free_courses": len([c for c in courses if c["price"] == 0]),
        "most_expensive_course": most_expensive,
        "total_seats": sum(c["seats_left"] for c in courses),
        "category_count": category_count
    }


# advanced browsing (IMPORTANT: must be above /courses/{course_id})

@app.get("/courses/browse")
def browse_courses(
    keyword: str = Query(None),
    category: str = Query(None),
    level: str = Query(None),
    max_price: int = Query(None),
    sort_by: str = Query("price"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1)
):

    result = courses

    if keyword is not None:
        key = keyword.lower()
        result = [
            c for c in result
            if key in c["title"].lower()
            or key in c["instructor"].lower()
            or key in c["category"].lower()
        ]

    if category is not None:
        result = [c for c in result if c["category"] == category]

    if level is not None:
        result = [c for c in result if c["level"] == level]

    if max_price is not None:
        result = [c for c in result if c["price"] <= max_price]

    valid_fields = ["price", "title", "seats_left"]

    if sort_by not in valid_fields:
        return {"error": "Invalid sort field"}

    reverse = True if order == "desc" else False

    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    total_results = len(result)

    start = (page - 1) * limit
    end = start + limit

    paginated = result[start:end]

    total_pages = (total_results + limit - 1) // limit

    return {
        "total_results": total_results,
        "total_pages": total_pages,
        "page": page,
        "limit": limit,
        "courses": paginated
    }


# get single course

@app.get("/courses/{course_id}")
def get_course(course_id: int):

    course = find_course(course_id)

    if not course:
        return {"error": "Course not found"}

    return {"course": course}


# enrollments

@app.get("/enrollments")
def get_enrollments():
    return {"enrollments": enrollments, "total": len(enrollments)}


@app.post("/enrollments")
def enroll(request: EnrollRequest):

    global enrollment_counter

    course = find_course(request.course_id)

    if not course:
        return {"error": "Course not found"}

    if course["seats_left"] <= 0:
        return {"error": "No seats available"}

    if request.gift_enrollment and request.recipient_name == "":
        return {"error": "Recipient name required for gift"}

    fee = calculate_enrollment_fee(course["price"], course["seats_left"], request.coupon_code)

    course["seats_left"] -= 1

    enrollment = {
        "enrollment_id": enrollment_counter,
        "student_name": request.student_name,
        "course_title": course["title"],
        "instructor": course["instructor"],
        "original_price": fee["original_price"],
        "discount": fee["discount"],
        "final_fee": fee["final_fee"],
        "gift_for": request.recipient_name if request.gift_enrollment else None
    }

    enrollments.append(enrollment)
    enrollment_counter += 1

    return {"message": "Enrollment successful", "enrollment": enrollment}