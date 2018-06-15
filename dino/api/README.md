<h1>REST API Tutorial</h1>

**General**

I found [this](https://www.youtube.com/watch?v=Yw7gETuRKjw) wonderful Django REST Framework tutorial on YouTube. The guy explains how to get company data via an api interface. 

The result will look like this in the browser: 

```
[
    {
        "id": 1,
        "ticker": "FB",
        "open": 7.0,
        "close": 10.23,
        "volume": 500
    },
    {
        "id": 2,
        "ticker": "AMZN",
        "open": 123.0,
        "close": 230.0,
        "volume": 700
    },
    {
        "id": 3,
        "ticker": "GOOG",
        "open": 50.0,
        "close": 67.0,
        "volume": 120
    }
]
```

With these basics we can create our own api for the DINO application.



**Problems**

If you started to create an api with the [official website](http://www.django-rest-framework.org/), you may have copied this into your roots settings.py: 

```
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
```

You have to delete it because you get an error when you follow the YouTube tutorial. I got this error and I want you to make it better from the beginning :) 