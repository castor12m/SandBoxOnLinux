import yaml

#ref. https://rfriend.tistory.com/540 [R, Python 분석과 프로그래밍의 친구 (by R Friend)]

with open('vegetables.yml') as f:
    vegetables = yaml.load(f, Loader=yaml.FullLoader)
    print(vegetables)
 
#result {'Vegetables': ['Pepper', 'Tomato', 'Garlic']}#


