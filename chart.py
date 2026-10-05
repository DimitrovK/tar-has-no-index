import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.patches as P
plt.rcParams.update({"figure.facecolor":"#12141a","axes.facecolor":"#12141a","axes.edgecolor":"#3a4050",
 "text.color":"#e6e8ee","axes.labelcolor":"#e6e8ee","xtick.color":"#9aa3b5","ytick.color":"#9aa3b5",
 "font.size":11,"grid.color":"#232733","font.family":"DejaVu Sans"})
fig=plt.figure(figsize=(12.5,9.4))
ax=fig.add_axes([0.04,0.56,0.93,0.41]); ax.set_xlim(-4,516); ax.set_ylim(-0.2,3.4); ax.axis("off")
fields=[(0,100,"name","#4a9eff"),(100,8,"mode",None),(108,8,"uid",None),(116,8,"gid",None),
        (124,12,"size","#e5484d"),(136,12,"mtime","#f5a524"),(148,8,"chksum","#a371f7"),
        (156,1,"type",None),(157,100,"linkname",None),(257,8,"ustar",None),
        (265,64,"uname, gname",None),(329,183,"devmajor, devminor, prefix, padding",None)]
for off,ln,lab,c in fields:
    ax.add_patch(P.Rectangle((off,1.45),ln,0.9,facecolor=c or "#2a2f3c",edgecolor="#12141a",lw=1.4))
    if ln>=60: ax.text(off+ln/2,1.9,lab,ha="center",va="center",fontsize=10,color="#0b0d11" if c else "#c9d1d9")
# narrow fields: staggered callouts above the bar
call=[(104,"mode",2.85),(112,"uid",2.55),(120,"gid",2.85),(130,"size",2.55),
      (142,"mtime",2.85),(152,"chksum",2.55),(261,"ustar",2.6)]
for x,lab,y in call:
    ax.plot([x,x],[2.35,y-0.08],color="#5a6375",lw=0.9)
    ax.text(x,y,lab,ha="center",va="bottom",fontsize=9,color="#c9d1d9")
for x in (0,100,124,136,148,257,512):
    ax.text(x,1.27,str(x),ha="center",va="top",fontsize=8.5,color="#9aa3b5")
ax.text(-4,3.32,"One tar header: 512 bytes, fixed offsets, every number stored as octal text",fontsize=12.5,color="#e6e8ee",va="top")
notes=[("#e5484d","size: 11 octal digits, so 8,589,934,591 bytes at most. ustar refuses anything larger."),
       ("#a371f7","chksum: a plain sum of the 512 header bytes. The file's own data is never checked."),
       ("#f5a524","mtime: the reason tarring identical files twice produces different bytes.")]
for i,(c,t) in enumerate(notes):
    y=0.72-i*0.36
    ax.add_patch(P.Rectangle((-4,y-0.1),8,0.2,facecolor=c,edgecolor="none")); ax.text(10,y,t,va="center",fontsize=10)
ax2=fig.add_axes([0.22,0.07,0.75,0.40])
rows=[("tar, seekable file",3.0,33.6,"#4a9eff"),("zip (has an index)",0.2,3.3,"#3fb950"),
      ("tar.gz, streaming read",100.0,180.1,"#f5a524"),
      ("tar.gz getmember(),\nPython-gzipped",100.0,138.8,"#e58a4d"),
      ("tar.gz getmember(),\ngzip CLI",200.0,318.9,"#e5484d")]
for i,(lab,pct,ms,c) in enumerate(rows):
    ax2.barh(i,pct,color=c,edgecolor="#12141a",lw=1.4,height=.62)
    ax2.text(pct+2.5,i,f"{pct:g}% of the archive, {ms:.0f} ms",va="center",fontsize=10.5)
ax2.set_yticks(range(len(rows))); ax2.set_yticklabels([r[0] for r in rows],fontsize=10.5); ax2.invert_yaxis()
ax2.set_xlim(0,290); ax2.set_xlabel("bytes read to extract the LAST of 2,000 files, as a share of the archive")
ax2.grid(axis="x",alpha=.3,lw=.6)
ax2.set_title("No index: finding one file means walking every header, and compression removes even that shortcut",
              loc="left",fontsize=11.5,pad=10)
fig.savefig("tar.png",dpi=145); print("wrote tar.png")
