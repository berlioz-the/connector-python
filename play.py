# import requests

# r = requests.get('http://127.0.0.1:50002')
# print(r)
# print(r.status_code)
# print(r.text)

# import boto3

if __name__ == '__main__':
    import berlioz
else:
    from . import berlioz

print(berlioz.metadata.VERSION)
