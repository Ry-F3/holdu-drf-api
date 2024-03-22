from django.contrib.auth.models import User
from django.test import TestCase
from profiles.models import Profile, Rating
from django.utils import timezone


class ProfileTypeTest(TestCase):
    def test_profile_type_assignment_admin(self):
        """
        Create an admin user
        """
        admin_user = User.objects.create_user(
            username='admin', email='admin@example.com', password='admin'
        )

        """
        Create a profile for the admin user with profile type 'admin'
        """
        admin_profile = Profile.objects.create(
            owner=admin_user, profile_type='admin'
        )

        """
        Retrieve the profile associated with the admin user
        """
        admin_profile = Profile.objects.get(owner=admin_user)

        """
        Assert that the profile type is correctly assigned as 'admin'
        """
        self.assertEqual(admin_profile.profile_type, 'admin')

    def test_profile_type_assignment_employee(self):
        """
        Create an employee user
        """
        employee_user = User.objects.create_user(
            username='employee', email='employee@example.com', password='employee'
        )

        """
        Create a profile for the employee user with profile type 'employee'
        """
        employee_profile = Profile.objects.create(
            owner=employee_user, profile_type='employee'
        )

        """
        Retrieve the profile associated with the employee user 
        """
        employee_profile = Profile.objects.get(owner=employee_user)

        """
        Assert that the profile type is correctly assigned as 'employee'
        """
        self.assertEqual(employee_profile.profile_type, 'employee')

    def test_profile_type_assignment_employer(self):
        """
        Create an employer user
        """
        employer_user = User.objects.create_user(
            username='employer', email='employer@example.com', password='employer'
        )

        """ 
        Create a profile for the employer user with profile type 'employer'
        """
        employer_profile = Profile.objects.create(
            owner=employer_user, profile_type='employer'
        )

        """
        Retrieve the profile associated with the employer user 
        """
        employer_profile = Profile.objects.get(owner=employer_user)

        """ 
        Assert that the profile type is correctly assigned as 'employer'
        """
        self.assertEqual(employer_profile.profile_type, 'employer')


class RatingTest(TestCase):
    def setUp(self):
        """ 
        Create two users
        """
        self.user1 = User.objects.create_user(
            username='user1', email='user1@example.com', password='password1')
        self.user2 = User.objects.create_user(
            username='user2', email='user2@example.com', password='password2')

    def test_create_rating(self):
        """
        Create a rating instance
        """
        rating = Rating.objects.create(
            rating=4,
            comment='Great experience!',
            rate_user=self.user1,
            created_by=self.user2,
            created_at=timezone.now()
        )

        """
        Retrieve the created rating
        """
        retrieved_rating = Rating.objects.get(id=rating.id)

        """ 
        Check if the rating fields match the provided values
        """
        self.assertEqual(retrieved_rating.rating, 4)
        self.assertEqual(retrieved_rating.comment, 'Great experience!')
        self.assertEqual(retrieved_rating.rate_user, self.user1)
        self.assertEqual(retrieved_rating.created_by, self.user2)
        self.assertAlmostEqual(retrieved_rating.created_at,
                               timezone.now(), delta=timezone.timedelta(seconds=1))

    def test_rating_str_method(self):
        """
        Create a rating instance
        """
        rating = Rating.objects.create(
            rating=5,
            comment='Excellent service!',
            rate_user=self.user1,
            created_by=self.user2,
            created_at=timezone.now()
        )

        """
        Check if the __str__ method returns the expected string representation 
        """
        expected_str = f"Rating: {rating.rating}"
        self.assertEqual(str(rating), expected_str)
