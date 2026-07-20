import numpy as np
def analyze_student_scores(seed, num_students, num_courses):
    np.random.seed(seed)
    scores = np.random.uniform(50, 100, (num_students, num_courses))

    total_scores = np.sum(scores, axis=1)
    average_scores = np.mean(scores, axis=1)

    average_course_scores = np.mean(scores, axis=0)
    std_course_scores = np.std(scores, axis=0)

    lowest_scores = np.min(scores, axis=1)

    total_students = num_students
    excellent_count = np.sum(scores >= 90)
    good_count = np.sum((scores >= 70) & (scores < 90))
    pass_count = np.sum((scores >= 60) & (scores < 70))
    fail_count = np.sum(scores < 60)

    excellent_ratio = (excellent_count / (total_students * num_courses)) * 100
    good_ratio = (good_count / (total_students * num_courses)) * 100
    pass_ratio = (pass_count / (total_students * num_courses)) * 100
    fail_ratio = (fail_count / (total_students * num_courses)) * 100

    print("\n每个学生的总成绩和平均成绩：")
    for i in range(num_students):
        print(f"学生{i + 1}：总成绩={total_scores[i]:.2f}，平均成绩={average_scores[i]:.2f}")

    print("\n每门课程的平均分和标准差：")
    for j in range(num_courses):
        print(f"课程{j + 1}：平均分={average_course_scores[j]:.2f}，标准差={std_course_scores[j]:.2f}")

    print("\n每个学生的最差成绩：")
    for i in range(num_students):
        print(f"学生{i + 1}：最低分={lowest_scores[i]:.2f}")

    print("\n成绩分布情况：")
    print(f"优秀比例={excellent_ratio:.2f}%")
    print(f"良好比例={good_ratio:.2f}%")
    print(f"及格比例={pass_ratio:.2f}%")
    print(f"不及格比例={fail_ratio:.2f}%")


seed = int(input())
num_students = int(input())
num_courses = int(input())
analyze_student_scores(seed, num_students, num_courses)
