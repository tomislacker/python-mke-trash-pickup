# When The Hell Is Garbage Day?
That's what I wanted to know.  And no, I didn't want to go look it up because
I'm lazy.

## Usage
### Typical
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
