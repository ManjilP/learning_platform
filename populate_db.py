import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning_platform.settings')
django.setup()

from users.models import User
from courses.models import Course, Lesson
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

def populate():
    # Clean up existing data for a fresh start
    User.objects.all().delete()
    Course.objects.all().delete()

    print("Creating users...")
    instructor = User.objects.create_user(username='instructor1', password='password123', email='instructor@test.com', is_instructor=True, is_student=False)
    student1 = User.objects.create_user(username='student1', password='password123', email='student1@test.com', is_student=True)
    
    from django.conf import settings
    base_dir = settings.BASE_DIR
    dev_img_path = os.path.join(base_dir, 'static', 'images', 'mock', 'mock_course_dev_1773324820284.png')
    design_img_path = os.path.join(base_dir, 'static', 'images', 'mock', 'mock_course_design_1773324839460.png')
    bus_img_path = os.path.join(base_dir, 'static', 'images', 'mock', 'mock_course_business_1773324862892.png')
    
    print("Creating courses...")
    
    courses_data = [
        {
            'title': 'Mastering React and Tailwind',
            'description': 'Learn modern frontend development from scratch. Build beautiful, responsive interfaces with React and style them effortlessly with Tailwind CSS. Includes 10 real-world projects.',
            'price': 599.00,
            'category': 'Development',
            'img_path': dev_img_path,
        },
        {
            'title': 'Advanced Python Programming',
            'description': 'Dive deep into Python. Learn about decorators, generators, metaclasses, and multi-threading to become a Python master. Designed for developers looking to write scalable backends.',
            'price': 1000.00,
            'category': 'Development',
            'img_path': dev_img_path,
        },
        {
            'title': 'UI/UX Design Masterclass',
            'description': 'Design stunning, user-centric interfaces. Master Figma, wireframing, color theory, and micro-animations to wow your users. Go from a complete beginner to a hirable product designer.',
            'price': 899.00,
            'category': 'Design',
            'img_path': design_img_path,
        },
        {
            'title': 'Digital Marketing Growth',
            'description': 'Explode your business growth using modern digital marketing strategies. Master Google Ads, Facebook outreach, automated funnels, and SEO to dominate search algorithms.',
            'price': 1200.00,
            'category': 'Business',
            'img_path': bus_img_path,
        },
        {
            'title': 'Financial Modeling for Startups',
            'description': 'Learn how to model your startup finances, perform valuations, pitch to VC firms, and build comprehensive cap tables. Essential for serious founders.',
            'price': 1500.00,
            'category': 'Business',
            'img_path': bus_img_path,
        },
        {
            'title': 'Data Structures & Algorithms',
            'description': 'Ace your tech interviews by mastering the core concepts. We cover trees, graphs, dynamic programming, and tricky pattern problems common at FAANG companies.',
            'price': 499.00,
            'category': 'Development',
            'img_path': dev_img_path,
        }
    ]
    
    course_objects = []
    
    for i, data in enumerate(courses_data):
        c = Course(
            title=data['title'],
            description=data['description'],
            instructor=instructor,
            price=data['price'],
            category=data['category']
        )
        if os.path.exists(data['img_path']):
            with open(data['img_path'], 'rb') as f:
                c.image.save(f'course_cover_{i}.png', File(f), save=False)
        c.save()
        course_objects.append(c)

    print("Creating lessons...")
    dummy_video = SimpleUploadedFile("dummy.mp4", b"file_content", content_type="video/mp4")
    
    for c in course_objects:
        Lesson.objects.create(course=c, title=f'Introduction to {c.title}', video_file=dummy_video)
        Lesson.objects.create(course=c, title='Core concepts and Deep Dive', video_file=dummy_video)
        Lesson.objects.create(course=c, title='Real World Project Walkthrough', video_file=dummy_video)
        
    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
