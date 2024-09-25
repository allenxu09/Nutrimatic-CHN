result="\"ai\" ?? \"neng\" ????"
print(result)
result=result.replace('\"','\\b')
result=result.replace('?', '\S')
print(result+"*****")