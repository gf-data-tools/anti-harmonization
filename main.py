
from pathlib import Path
import os
from gf_utils.data_miner import DataMiner
import re

os.chdir(Path(__file__).resolve().parent)

miner = DataMiner(region='ch')
miner.get_stc()
with open(os.path.join(miner.raw_dir,'stc/catchdata.dat'),'rb') as f:
    cipher = f.read()
plain = miner.decode_catchdata(cipher)
src = '{"parameter_name":"naive_damage_switch","parameter_type":"string","parameter_value":"0;1","client_require":"1"},'
tgt = '{"parameter_name":"naive_damage_switch","parameter_type":"string","parameter_value":"1;1","client_require":"1"},'

modified = re.sub(src,tgt,plain)
cipher = miner.encode_catchdata(modified)
with open('catchdata.dat','wb') as f:
    f.write(cipher)