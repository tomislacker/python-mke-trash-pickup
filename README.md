# When The Hell Is Garbage Day?
That's what I wanted to know.  And no, I didn't want to go look it up because
I'm lazy.

## Usage
### CloudFormation

```sh
# Create the S3 bucket, build the code, deploy to S3
make s3-bucket ldist s3-deploy

# Create the CloudFormation stack
make cloud \
    ADDRESS_NUM=2727 \
    ADDRESS_DIR=S \
    STREET_NAME=27th \
    STREET_TYPE=ST

# Now you'll have an SNS topic created that you can go subscribe
# to for any updates that occur to your collection schedule.
```

**Other Variables**

| Name | Default | Description |
| `STACK_NAME` | `mke-trash-pickup` | CloudFormation stack name |
| `DEPLOY_BUCKET` | `mke-trash-pickup-12241` | S3 bucket for .zip deployment (Must be changed) |
| `LAMBDA_FREQ` | `12 hours` | How often the the scheduled event will check for changes |

### Typical

```sh
$ python setup.py install
$ mkerefusecheck \
    --address 2727 \
    --direction S \
    --street 27th \
    --street-type st
2016-12-29 12:50:08 - mke-refuse - DEBUG - Parsing arguments
2016-12-29 12:50:08 - mke-refuse - DEBUG - Composing query address
2016-12-29 12:50:08 - mke-refuse - INFO - Executing query...
2016-12-29 12:50:08 - requests.packages.urllib3.connectionpool - DEBUG - Starting new HTTP connection (1): mpw.milwaukee.gov
2016-12-29 12:50:08 - requests.packages.urllib3.connectionpool - DEBUG - http://mpw.milwaukee.gov:80 "POST /services/garbage_day HTTP/1.1" 200 None
2016-12-29 12:50:08 - RefusePickup - DEBUG - Parsing 13813 bytes of HTML
2016-12-29 12:50:08 - RefusePickup - DEBUG - Searching for 'next_pickup_garbage' with 'The next garbage collection pickup for this location is: <strong>(?P<value>[^<]+)</strong>'
2016-12-29 12:50:08 - RefusePickup - DEBUG - Searching for 'route_garbage' with 'garbage pickup route for this location is <strong>(?P<value>[^<]+)</strong>'
2016-12-29 12:50:08 - RefusePickup - DEBUG - Searching for 'next_pickup_recycle_before' with 'The next estimated pickup time is between <strong>(?P<after>[^<]+)</strong> and <strong>(?P<value>[^<]+)</strong>'
2016-12-29 12:50:08 - RefusePickup - DEBUG - Searching for 'route_recycle' with 'recycling pickup route for this location is <strong>(?P<value>[^<]+)</strong>'
2016-12-29 12:50:08 - RefusePickup - DEBUG - Searching for 'next_pickup_recycle_after' with 'The next estimated pickup time is between <strong>(?P<value>[^<]+)</strong> and <strong>(?P<before>[^<]+)</strong>'
2016-12-29 12:50:08 - mke-refuse - INFO - Query returned
{
    "route_recycle": "NR1-2-3",
    "next_pickup_garbage": "THURSDAY JANUARY 5, 2017",
    "route_garbage": "NP1-2A",
    "next_pickup_recycle_before": "THURSDAY JANUARY 5, 2017",
    "next_pickup_recycle_after": "WEDNESDAY JANUARY 4, 2017"
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
**Note:** These xpaths are still listed for historical reasons since parsing
is now done via regex due to issues like
[#5](https://github.com/tomislacker/python-mke-trash-pickup/issues/5).

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
**Note:** These references are still listed for historical reasons since
parsing is now done via regex due to issues like
[#5](https://github.com/tomislacker/python-mke-trash-pickup/issues/5).

- [[azavea.com] Using Python's LXML in Amazon Lambda](https://www.azavea.com/blog/2016/06/27/using-python-lxml-amazon-lambda/)
- [[stackoverflow.com] Use LXML on AWS Lambda](http://stackoverflow.com/questions/36387664/use-lxml-on-aws-lambda)
