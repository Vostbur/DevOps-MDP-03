# Web Interface for the MapQuest Directions API

## 1.3.4.1: Option 1 - Modify the MapQuest API App

Master Skills:

- Build a web interface that users access to interact with the application

---

Written with Django. Command to run `python manage.py runserver`

![](./web-interface-maprequest-api.PNG)

## Get a MapQuest API Key and save it for using as an environment variable

Before building the application, you need to complete the following steps to get a *MapQuest API key*.
- Go to: https://developer.mapquest.com/.
- Click **Sign Up** at the top of the page.
- Fill out the form to create a new account. For **Company**, enter **Cisco Networking Academy Student**.
- After clicking **Sign Me Up**, you are redirected to the **Manage Keys** page. If you are redirected elsewhere, click **Manage Keys** from the list of options on the left.
- Click **Approve All Keys**.
- Expand **My Application**.
- In project directory create a text file named **.env**
- Copy your **Consumer Key** to a text file **.env** like this:

```
MAPQUESTAPI_CONSUMER_KEY=enter_your_key
```

**Note:** MapQuest may change the process for obtaining a key. If the steps above are no longer valid, search the internet for “steps to generate mapquest api key”.