# smart_pension
Test task for DE position

Current version of code can download data for 1 specific day. There is an option to use the same functionality over the Time-Series endpoint, but API Access Key from professional subscription plan will be required (currently used from "Basic").

- Automated unit tests: done as a subclass of unittest.TesCase. Could be developed further.
- Error handling if the API returns error codes: done
- Handling of API rate limiting: possible to increase with non-functional way (update subscription plan). Possible to limit the output of currencies with "symbols" keyword.
- How to handle API keys/secrets if the API were to require such things: use privat class attributes (self.__api_key)
- Consideration for how the code would perform with much higher volumes of data (e.g. 100,000 company records): as we unpack JSON structure with native Pandas methods should be a problem with 100K records. 
