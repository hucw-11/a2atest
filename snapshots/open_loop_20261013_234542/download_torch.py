"""Download a public wheel in verified byte ranges when a full transfer stalls."""
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse
from pathlib import Path
import hashlib
import json
import time
import urllib.request

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--package',default='torch'); parser.add_argument('--version',default='2.5.1')
    args=parser.parse_args()
    meta=json.load(urllib.request.urlopen(f'https://pypi.org/pypi/{args.package}/{args.version}/json',timeout=30))
    item=next(x for x in meta['urls'] if x['filename'].endswith('cp312-cp312-win_amd64.whl'))
    root=Path('downloads') if args.package=='torch' else Path('downloads')/f'{args.package}-{args.version}'
    root.mkdir(parents=True,exist_ok=True)
    size=item['size']; chunk=2*1024*1024
    def get(i):
        start=i*chunk; end=min(size,start+chunk)-1
        path=root/f'torch.part{i:04d}'
        if path.exists() and path.stat().st_size==end-start+1: return i
        for attempt in range(4):
            try:
                req=urllib.request.Request(item['url'],headers={'Range':f'bytes={start}-{end}'})
                with urllib.request.urlopen(req,timeout=45) as r:
                    if r.status!=206: raise ValueError('Server ignored byte range')
                    data=r.read()
                if len(data)!=end-start+1: raise ValueError('Short range')
                path.write_bytes(data); return i
            except Exception:
                if attempt==3: raise
                time.sleep(2)
    n=(size+chunk-1)//chunk
    with ThreadPoolExecutor(max_workers=6) as pool:
        for done,f in enumerate(as_completed([pool.submit(get,i) for i in range(n)]),1):
            f.result()
            if done%10==0 or done==n: print(f'Wheel chunks {done}/{n}',flush=True)
    target=root/item['filename']; digest=hashlib.sha256()
    with target.open('wb') as f:
        for i in range(n):
            data=(root/f'torch.part{i:04d}').read_bytes(); digest.update(data); f.write(data)
    if digest.hexdigest()!=item['digests']['sha256']: raise ValueError('SHA256 mismatch')
    print(f'VERIFIED {target} sha256={digest.hexdigest()}',flush=True)

if __name__=='__main__': main()
