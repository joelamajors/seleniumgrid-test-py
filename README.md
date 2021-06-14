## Python-Pytest-Selenium

### Summary
This is a tool that's used run automated test in the LambdaTest testing framework. This uses the `urls.json` file to check each URL listed agains the devices lists in the `caps.json` 


### Environment Setup

1. Global Dependencies
    * [Install Python](https://www.python.org/downloads/)
    * Or Install Python with [Homebrew](http://brew.sh/)
    ```
    $ brew install python
    ```
    * Install [pip](https://pip.pypa.io/en/stable/installing/) for package installation

2. LambdaTest Credentials
    * https://www.lambdatest.com/support/docs/using-environment-variables-for-authentication-credentials/
    * In the terminal export your LambdaTest Credentials as environmental variables:
        - For Macos & Linux
            ```
            $ export LT_USERNAME=<your LambdaTest username>
            $ export LT_ACCESS_KEY=<your LambdaTest access key>
            ```
        - Windows
            ```
            $ set LT_USERNAME=<your LambdaTest username>
            $ set LT_ACCESS_KEY=<your LambdaTest access key>
            ```

3. Project
	* The recommended way to run your tests would be in [virtualenv](https://virtualenv.readthedocs.org/en/latest/). It will isolate the build from other setups you may have running and ensure that the tests run with the specified versions of the modules specified in the requirements.txt file.


    * If you do not have virtualenv installed

	```bash
    pip install virtualenv
    ```

	* Create a virtual environment in your project folder the environment name is arbitrary.

	```bash
    virtualenv venv
    ```

	* Activate the environment:

	```bash
    source venv/bin/activate
    ```
	* Install the required packages:

	```bash
    pip install -r requirements.txt
    ```

### Running Tests:  -n option designates number of parallel tests and -s to disable output capture.

* Update the `urls.json` to the list of URLs you want to check

*  Tests in Parallel:

    ```bash
    pytest -s -n 2  tests\lt_sample_todo.py
    ```
* Test one at a time:
    ```bash
    pytest -s tests\lt_sample_todo.py
    ```

To use Pytest with LambdaTest, make sure you have the 2 environment variables LT_USERNAME and LT_ACCESS_KEY set. To obtain a username and access_key, sign up for free [here](https://lambdatest.com)).

#####  Routing traffic through your local machine
- Set tunnel value to `True` in test capabilities
> OS specific instructions to download and setup tunnel binary can be found at the following links.
>    - [Windows](https://www.lambdatest.com/support/docs/display/TD/Local+Testing+For+Windows)
>    - [Mac](https://www.lambdatest.com/support/docs/display/TD/Local+Testing+For+MacOS)
>    - [Linux](https://www.lambdatest.com/support/docs/display/TD/Local+Testing+For+Linux)

### Important Note:
---
- Some Safari & IE browsers, doesn't support automatic resolution of the URL string "localhost". Therefore if you test on URLs like "http://localhost/" or "http://localhost:8080" etc, you would get an error in these browsers. A possible solution is to use "localhost.lambdatest.com" or replace the string "localhost" with machine IP address. For example if you wanted to test "http://localhost/dashboard" or, and your machine IP is 192.168.2.6 you can instead test on "http://192.168.2.6/dashboard" or "http://localhost.lambdatest.com/dashboard".

### Resources

##### [Selenium Documentation](http://www.seleniumhq.org/docs/)
##### [Pytest Documentation](http://pytest.org/latest/contents.html)
