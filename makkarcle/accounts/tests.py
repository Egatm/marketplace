from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from .models import CustomUser
from .forms import CustomUserCreationForm
from .views import SignUpView


# Create your tests here.
class SignupPageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_view_reverse(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")
        self.assertContains(response, "Создать аккаунт")

    def test_signup_form(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "testuser@email.com",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, "testuser")
        self.assertEqual(get_user_model().objects.all()[0].email, "testuser@email.com")

    # test correct form is on the signup page
    def test_signup_form_class(self):
        response = self.client.get(reverse("signup"))
        form = response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(response, 'csrfmiddlewaretoken')

    # test sighnup view resolves with its view class
    def test_signup_view(self):
        view = resolve(reverse('signup'))
        self.assertEqual(
            view.func.__name__,
            SignUpView.as_view().__name__
        )


class UpdateProfileTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('update_profile', kwargs={'pk': self.user.pk})

    def test_update_profile_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_edit.html')

    def test_update_profile(self):
        data = {
            'username': 'newusername',
            'email': 'newemail@test.com',
            'birth_date': '1990-01-01',
            'first_name': 'New',
            'last_name': 'User',
            'address': '123 New Street'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        updated_user = CustomUser.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, 'newusername')
        self.assertEqual(updated_user.email, 'newemail@test.com')
        self.assertEqual(str(updated_user.birth_date), '1990-01-01')
        self.assertEqual(updated_user.first_name, 'New')
        self.assertEqual(updated_user.last_name, 'User')
        self.assertEqual(updated_user.address, '123 New Street')


class LoginPageTests(TestCase):
    # check login url status code
    def test_login_page_status_code_by_url(self):
        responce = self.client.get('/account/login/')
        self.assertEqual(responce.status_code, 200)

    # reverse responce setup
    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test",
            email="test@example.com",
            password="testpass123",
        )
        self.url = reverse('login')
        self.responce = self.client.get(self.url)
    # check login page status code via reverse

    def test_login_page_status_code_by_reverse(self):
        self.assertEqual(self.responce.status_code, 200)

    # check login page template name via reverse
    def test_login_page_template_by_reverse(self):
        self.assertTemplateUsed(self.responce, 'registration/login.html')

    # check that page contains correct html
    def test_login_page_contains_correct_html(self):
        self.assertContains(self.responce, 'Войти')
        self.assertNotContains(self.responce, 'Django administration')

    # check that user can log in
    def test_user_can_login(self):
        responce = self.client.post(self.url, data={
            "username": "test",
            "password": "testpass123",
        })
        self.assertEqual(responce.status_code, 302)
        self.assertEqual(responce.url, reverse('home'))


# test custom user model
class CustomUserTests(TestCase):
    # test to test custom user model for a regular non-admin user
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test",
            email="test@example.com",
            password="testpass123",
        )
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    # test to test admin user creation in the database
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="admintest123",
        )
        self.assertEqual(admin_user.username, "admin")
        self.assertEqual(admin_user.email, "admin@test.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


# test password reset
class PasswordResetTests(TestCase):
    # set up function
    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test",
            email="test@example.com",
            password="testpass123",
        )
        self.url = reverse('password_reset')
        self.responce = self.client.get(self.url)

    # test password reset view by url
    def test_view_by_url(self):
        responce = self.client.get('/account/password_reset/')
        self.assertEqual(responce.status_code, 200)

    # test password reset page
    def test_view(self):
        self.assertEqual(self.responce.status_code, 200)
        self.assertTemplateUsed(self.responce, 'registration/password_reset_form.html')
        self.assertContains(self.responce, 'Сбросить пароль')
        self.assertNotContains(self.responce, 'Email был отослан')

    # test password reset view post request
    def test_password_reset_post(self):
        responce = self.client.post(self.url, data={
            'email': "test@example.com",
        })
        self.assertEqual(responce.status_code, 302)
        self.assertEqual(responce.url, reverse("password_reset_done"))
