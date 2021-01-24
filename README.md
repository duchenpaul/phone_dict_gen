# Generate dictionary based on Chinese phone number

## Usage
Set priority in table `province_priority` to adjust the sequence of the province in dict, priority 0 will not be generated.

`fetch_url.py` fetches all phone number regions from [www.51hao.cc](http://www.51hao.cc)
`load_phone_region.py` loads phone numbers to sqlitedb
`phone_dict_gen.py` will generate the phone dicts


## Docker
Use docker to generate phone dict
```
git pull && docker-compose build && docker image prune -f && docker container prune -f
docker-compose --build up -d
```