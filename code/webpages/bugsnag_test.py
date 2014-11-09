import bugsnag
bugsnag.configure(
    api_key="780ff3a44e2fb9798e2319078059b5a1"
)
bugsnag.notify(Exception("Test Error"))
