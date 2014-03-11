import sure  # noqa
from save_parser import SaveDataGen1

with open('test_save.sav', 'rb') as f:
    save = SaveDataGen1(f.read())

save.money.should.equal(40398)
save.trainer_name.should.equal('RED')
save.trainer_id.should.equal(20152)
save.rival_name.should.equal('BLUE')
save.num_pkmn.should.equal(6)
