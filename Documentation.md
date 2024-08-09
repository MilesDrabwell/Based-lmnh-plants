

## Testing 
`test_fetch_data.py` - used to test `fetch_data.py`
What we considered testing for in this file: 
- If `get_plant_data` (our main function that will extract all the plant data) is actually getting called and if it's getting called exactly once.
- If it's returning the amount of elements expected
- If an exception is raised when an id is inserted that isn't a number (integer technically).
<br>We decided not to test the actual integer as even though we have 50 plants right now, this number may change.
<br>We also checked the coverage and it gave 95% which we are happy with so moved on.

|Name|Stmts|Miss|Cover|
|----|----|----|----|
|extract.py|34|9|74%|
|test_extract.py|39|2|95%|
|**TOTAL**|73|11|**85%**|



