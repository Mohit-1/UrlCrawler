from rest_framework.test import APIRequestFactory, APITestCase
from .views import ListURLDetails

url_list = ["https://www.tutorialspoint.com",
            "https://www.stackoverflow.com",
            "https://www.medium.com"]
view = ListURLDetails.as_view()


class APITest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def testDetails(self):
        for url in url_list:
            print("\nTesting for - " + url)
            request = self.factory.get('api/checkjquery?url=' + url)
            response = view(request)
            print(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(response.data['success'], [True, False])
            self.assertIn(response.data['uses_jquery'], ['yes', 'no', 'maybe'])

            print("\nTesting for version now")
            request = self.factory.get('api/checkjquery?getversion=yes&url=' +
                                       url)
            response = view(request)
            print(response.data)

            print("\nTesting for line of jQuery now")
            request = self.factory.get('api/checkjquery?verbose=yes&url=' +
                                       url)
            response = view(request)
            print(response.data)
