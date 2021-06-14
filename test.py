import json

# Importing JSON file to get URLs and caps
f = open('./urls.json')
data = json.loads(f.read())
urls = data["urls"]

# Returns first URL to parse build_name
check_url = urls[0]

# Build Name
name = 'https://aac.hatfield.marketing/chimney-services/fireplaces/freestanding-wood-stoves'.strip('https://').split(".")
build_name = name[0]

# Build name
print(build_name)

# Page name
page_names = name[len(name)-1].split('/')
page_name = page_names[len(page_names)-1]

# Calculating page name
print(page_name)
