from save_parser import SaveDataGen1

with open('tpp.sav', 'rb') as f:
    d = SaveDataGen1(f.read())

print d.trainer_name
print d.money
print d.rival_name
print d.trainer_id
