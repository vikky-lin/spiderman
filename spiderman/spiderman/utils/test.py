import uuid

table_name = 'table'
params = {1:1,'d':'d'}
keys = {'s':'s'}
exec_part = '{0[0]}=%s {1}'
for item in list(params.items()):
    exec_part = exec_part.format(item,',{0[0]}=%s {1}')
exec_part = exec_part.replace(',{0[0]}=%s {1}','')
print(exec_part)
# condition_part = '{0[0]}={0[1]}{1}'
# for item in list(keys.items()):
#     condition_part = condition_part.format(item,',{0[0]}={0[1]}{1}')
# condition_part = condition_part.replace(',{0[0]}={0[1]}{1}','')
# sql = 'update {} set {} where {}'.format(table_name,exec_part,condition_part)
# print(sql)

print([1]+[1])