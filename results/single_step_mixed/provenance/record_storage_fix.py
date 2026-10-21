"""One-time provenance record for a storage-only repair during this experiment."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parents[3]
out=root/'results/single_step_mixed'
hashes=json.loads((out/'source_hashes.json').read_text(encoding='utf-8'))
current=(root/'experiment.py').read_text(encoding='utf-8')
previous=current.replace('import uuid\n','')
start=previous.index('def save_checkpoint(')
end=previous.index('def predict(',start)
previous=previous[:start]+previous[end:]
previous=previous.replace('best=rmse; save_checkpoint(path,ck)','best=rmse; torch.save(ck,path)')
previous=previous.replace('save_checkpoint(last,{','torch.save({')
previous=previous.replace("'cuda_rng':torch.cuda.get_rng_state_all() if device=='cuda' else None})",
                          "'cuda_rng':torch.cuda.get_rng_state_all() if device=='cuda' else None},last)")
assert hashlib.sha256(previous.encode('utf-8')).hexdigest()==hashes['experiment.py']
(out/'provenance/experiment_before_atomic.py').write_text(previous,encoding='utf-8',newline='\n')
history=[dict(stage='initial training and first resume',hashes=hashes.copy()),
         dict(stage='storage-only atomic checkpoint fix; resume from single_fm seed33 step12300',
              reason='Native torch Windows path opener intermittently refused checkpoint overwrite; '
                     'Python stream plus atomic replace and short permission retry. '
                     'Loss, model, optimizer, data, source jitter and random sampling are unchanged.',
              hashes={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in hashes})]
(out/'source_hash_history.json').write_text(json.dumps(history,indent=2),encoding='utf-8')
(out/'source_hashes.json').write_text(json.dumps(history[-1]['hashes'],indent=2),encoding='utf-8')
print('Recorded storage-only fix; previous source hash verified exactly.')
