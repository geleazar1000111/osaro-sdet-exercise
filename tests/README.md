Pizza API 
-
Realized too late that I didn't mock out the actual request responses...but my tests assume that this is always the response:

```[
  {
    "Crust": "NORMAL",
    "Flavor": "BEEF-NORMAL",
    "Order_ID": 1,
    "Size": "M",
    "Table_No": 1,
    "Timestamp": "2019-12-03T18:21:08.669365"
  },
  {
    "Crust": "THIN",
    "Flavor": "CHEESE",
    "Order_ID": 2,
    "Size": "S",
    "Table_No": 5,
    "Timestamp": "2019-12-03T18:21:08.708470"
  },
  {
    "Crust": "NORMAL",
    "Flavor": "CHICKEN-FAJITA",
    "Order_ID": 3,
    "Size": "L",
    "Table_No": 3,
    "Timestamp": "2019-12-03T18:21:08.710006"
  }]
```


Exercise2 Tracker
- 
Didn't have enough time to completely do the Averager Model class, but I added the skeleton anyway.

Other Notes
-
If I had more time I would have used pytest fixtures and a conftest file. I would have also liked to put docstrings and more descriptive comments in the test files. I would have also separate the expected data for the pizza API into another file (like what I had to do for the Geri API tests). And I would definitely make sure the API requests for the pizza API were mocked.
