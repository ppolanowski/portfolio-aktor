from PIL import Image;import subprocess,json
S='/home/deck/.hermes/cache/scratch/rog/';O='src/img/'
sel=["L1150313", "L1150318", "09", "08", "07", "11", "L1008181", "L1008046", "L1008248", "L1150135", "23", "L1008178", "L1008114", "15", "19", "20", "L1150076", "24", "27", "L1150307", "06", "12", "L1008217", "L1008213", "21", "L1008159", "L1008121", "L1150130", "L1150177", "L1008228", "18", "L1008137", "L1008162", "22", "16"]
out=[]
for n in sel:
  f=S+(f'portfolio-{n}.jpg' if n.isdigit() else n+'.jpg');im=Image.open(f);icc=im.info.get('icc_profile');im=im.convert('RGB')
  r={'n':n,'w':im.width,'h':im.height}
  for w in (480,960):
    x=im.copy();x.thumbnail((w,10000));j=f'{O}p{n}-{w}.jpg'
    x.save(j,quality=78,optimize=True,progressive=True,icc_profile=icc)
    subprocess.run(['exiftool','-q','-overwrite_original','-tagsfromfile',f,'-Artist','-Copyright','-IPTC:all','-XMP-dc:Creator','-XMP-dc:Rights','-XMP-photoshop:Credit','-XMP-xmpRights:Marked',j])
    subprocess.run(['cwebp','-quiet','-q','75','-metadata','all',j,'-o',j[:-3]+'webp'])
    subprocess.run(['avifenc','-q','55','-s','6',j,j[:-3]+'avif'],capture_output=True)
    r[w]=x.size
  out.append(r)
im=Image.open(S+'L1150313.jpg').convert('RGB');w,h=im.size;c=im.crop((0,int(h*.12),w,int(h*.12)+int(w*630/1200))).resize((1200,630));c.save(O+'og.jpg',quality=80)
json.dump(out,open('/home/deck/.hermes/cache/scratch/sizes.json','w'));print([(r['n'],r[480],r[960]) for r in out])
