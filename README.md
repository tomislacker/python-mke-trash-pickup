# When The Hell Is Garbage Day?
That's what I wanted to know.  And no, I didn't want to go look it up because
I'm lazy.

## Usage
### Typical

```sh
$ python setup.py install
$ mkerefusecheck \
    --address 2727 \
    --direction S \
    --street 27th \
    --street-type st
2016-04-14 20:23:19 - mke-refuse - DEBUG - Parsing arguments
2016-04-14 20:23:19 - mke-refuse - DEBUG - Composing query address
2016-04-14 20:23:19 - mke-refuse - INFO - Executing query...
2016-04-14 20:23:19 - requests.packages.urllib3.connectionpool - INFO - Starting new HTTP connection (1): mpw.milwaukee.gov
2016-04-14 20:23:19 - requests.packages.urllib3.connectionpool - DEBUG - "POST /services/garbage_day HTTP/1.1" 200 None
2016-04-14 20:23:19 - RefusePickup - INFO - Reading through 14152 bytes for 6 properties...
2016-04-14 20:23:19 - RefusePickup - DEBUG - Searching for 'next_pickup_recycle_after': //*[@id="nConf"]/strong[4]
2016-04-14 20:23:19 - RefusePickup - DEBUG - Searching for 'route_recyle': //*[@id="nConf"]/strong[3]
2016-04-14 20:23:19 - RefusePickup - DEBUG - Searching for 'next_pickup_recycle_before': //*[@id="nConf"]/strong[5]
2016-04-14 20:23:19 - RefusePickup - DEBUG - Searching for 'success_msg': //*[@id="nConf"]/h1
2016-04-14 20:23:19 - RefusePickup - DEBUG - Searching for 'route_garbage': //*[@id="nConf"]/strong[1]
2016-04-14 20:23:19 - RefusePickup - DEBUG - Searching for 'next_pickup_garbage': //*[@id="nConf"]/strong[2]
2016-04-14 20:23:19 - mke-refuse - INFO - Query returned
{
    "next_pickup_recycle_after": "TUESDAY MAY 3, 2016",
    "route_recyle": "SR01-3-07",
    "route_garbage": "SP1-3A",
    "success_msg": "2727 S 27TH ST - Address located!",
    "next_pickup_recycle_before": "May 9th - May 13th",
    "next_pickup_garbage": "TUESDAY APRIL 19, 2016"
}
```

### Advanced
*See [Usage.ipynb](Usage.ipynb)*

### Development Setup

```sh
make dev
venv/bin/pip3 install jupyter
venv/bin/jupyter notebook
```

## Technical Details
### Form Request
- **Form Page:** `GET` http://mpw.milwaukee.gov/services/garbage_day
- **Form Action:** `POST` http://mpw.milwaukee.gov/services/garbage_day
  - **laddr:** House number
  - **sdir:** *(N|S|E|W)*
  - **sname:** Street name *(ex: 27TH)*
  - **stype:** Street type *(AV|BL|CR|CT|DR|LA|PK|PL|RD|SQ|ST|TR|WY)*
  - **Submit:** Submit

### Form Response *(XPaths)*
- **Success Or Note:** `//*[@id="nConf"]/h1`
- **Winter Pickup Route:** `//*[@id="nConf"]/strong[1]`
- **Next Garbage Pickup:** `//*[@id="nConf"]/strong[2]`
- **Winter Recycle Route:** `//*[@id="nConf"]/strong[3]`
- **Next Recycle Pickup (Earliest):** `//*[@id="nConf"]/strong[4]`
- **Next Recycle Pickup (Latest):** `//*[@id="nConf"]/strong[5]`

### Example cURL

```sh
curl \
    -vvXPOST \
    -d 'laddr=2727&sdir=S&sname=27TH&stype=ST&Submit=Submit' \
    http://mpw.milwaukee.gov/services/garbage_day
```

## References
### Building Libraries for Lambda
- [[azavea.com] Using Python's LXML in Amazon Lambda](https://www.azavea.com/blog/2016/06/27/using-python-lxml-amazon-lambda/)
- [[stackoverflow.com] Use LXML on AWS Lambda](http://stackoverflow.com/questions/36387664/use-lxml-on-aws-lambda)
