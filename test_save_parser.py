import sure  # noqa
from save_parser import SaveDataGen1

with open('test_save.sav', 'rb') as f:
    save = SaveDataGen1(f.read())

save.money.should.equal(40398)
save.trainer_name.should.equal('RED')
save.trainer_id.should.equal(20152)
save.rival_name.should.equal('BLUE')
save.num_party.should.equal(6)

len(save.party).should.equal(6)

battery_jesus = save.party[0]
battery_jesus.species.should.equal('Zapdos')
battery_jesus.nickname.should.equal('AA-j')
battery_jesus.trainer_id.should.equal(save.trainer_id)
len(battery_jesus.moves).should.equal(4)
battery_jesus.move_names[3].should.equal('Thunder')
battery_jesus.level.should.equal(81)

bird_jesus = save.party[5]
bird_jesus.species.should.equal('Pidgeot')
bird_jesus.trainer_name.should.equal('RED')
bird_jesus.nickname.should.equal('aaabaaajss')
bird_jesus.exp.should.equal(343472)

lord_helix = save.party[2]
lord_helix.species.should.equal('Omastar')
lord_helix.nickname.should.equal('OMASTAR')
lord_helix.hp_curr.should.equal(0)
lord_helix.hp_max.should.equal(154)
