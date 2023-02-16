import datetime

from django.test import TestCase
from django.urls import reverse

from blog.models import Writer, BlogInstance, Blog, BlogType


class WriterListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_writers = 13

        for writer_id in range(number_of_writers):
            Writer.objects.create(
                first_name=f'Dominique {writer_id}',
                last_name=f'Surname {writer_id}',
                id='1'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/writer/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('writer'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('writer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/writer_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('writer'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['writer_list']), 10)

    def test_lists_all_writers(self):
        response = self.client.get(reverse('writer') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['writer_list']), 3)

    def test_only_subscribed_blogs_in_list(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-subscribed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check that initially we don't have any blogs in list (none subscribed for)
        self.assertTrue('bloginstance_list' in response.context)
        self.assertEqual(len(response.context['bloginstance_list']), 0)

        # Now change all blogs to be subscribed for
        blogs = BlogInstance.objects.all()[:10]

        for blog in blogs:
            blog.status = 'P'
            blog.save()

        # Check that now we have subscribed blogs in the list
        response = self.client.get(reverse('my-subscribed'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        self.assertTrue('bloginstance_list' in response.context)

        # Confirm all blogs belong to testuser1 and have been subscribed for
        for blogitem in response.context['bloginstance_list']:
            self.assertEqual(response.context['user'], blogitem.borrower)
            self.assertEqual(blogitem.status, 'P')

    def test_pages_ordered_by_due_date(self):
        for blog in BlogInstance.objects.all():
            blog.status = 'P'
            blog.save()

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-subscribed'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        # Confirm that of the items, only 10 are displayed due to pagination.
        self.assertEqual(len(response.context['bloginstance_list']), 10)

        last_date = 0
        for blog in response.context['bloginstance_list']:
            if last_date == 0:
                last_date = blog.due_back
            else:
                self.assertTrue(last_date <= blog.due_back)
                last_date = blog.due_back


import uuid

from django.contrib.auth.models import Permission, User


class RenewBlogInstancesViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Set blog as subscribed')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        test_writer = Writer.objects.create(first_name='John', last_name='Smith')
        test_blog_type = BlogType.objects.create(name='Food')
        test_blog = Blog.objects.create(
            title='Blog Title',
            description='My blog description',
            writer=test_writer,
        )

        blog_type_objects_for_blog = BlogType.objects.all()
        test_blog.blog_type.set(blog_type_objects_for_blog)
        test_blog.save()

        renew_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bloginstance1 = BlogInstance.objects.create(
            blog=test_blog,
            imprint='Unlikely Imprint, 2023',
            due_back=renew_date,
            subscriber=test_user1,
            status='P',
        )

        renew_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bloginstance1 = BlogInstance.objects.create(
            blog=test_blog,
            imprint='Unlikely Imprint, 2023',
            due_back=renew_date,
            subscriber=test_user2,
            status='P',

        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('renew_subscription_staff', kwargs={'pk': self.test_bloginstance1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('renew_subscription_staff', kwargs={'pk': self.test_bloginstance1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_subscribed_blog(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew_subscription_staff', kwargs={'pk': self.test_bloginstance1.pk}))

        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_subscribed_blog(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew_subscription_staff', kwargs={'pk': self.test_bloginstance1.pk}))

        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_blog_if_logged_in(self):
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew_subscription_staff', kwargs={'pk': test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew_subscription_staff', kwargs={'pk': self.test_bloginstance1.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'blog/subscription_renew_staff.html')

    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew_subscription_staff', kwargs={'pk': self.test_bloginstance1.pk}))
        self.assertEqual(response.status_code, 200)

        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(response.context['form'].initial['renewal_date'], date_3_weeks_in_future)

    def test_redirects_to_home_on_success(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
        response = self.client.post(reverse('renew_subscription_staff', kwargs={'pk': self.test_bloginstance1.pk, }),
                                    {'renewal_date': valid_date_in_future}, follow=True)
        self.assertRedirects(response, '/blog/')

    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(reverse('renew_subscription_staff', kwargs={'pk': self.test_bloginstance1.pk}), {'renewal_date': date_in_past})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal in past')

    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        response = self.client.post(reverse('renew_subscription_staff', kwargs={'pk': self.test_bloginstance1.pk}), {'renewal_date': invalid_date_in_future})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal more than 4 weeks ahead')
